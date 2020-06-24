from collections import deque
import itertools as it
import logging
import math
import os
import statistics
import numpy as np
import pandas as pd
from dipas.build import from_file, create_script, sequence_script, track_script
import dipas.elements as elements
from dipas.madx import run_script
import torch

logging.basicConfig(level=logging.INFO)

optimization_targets = dict(
    target_rms_x=500e-6,  # Spot size at target.
    target_rms_y=500e-6,
    dump_rms_x=12e-3,     # Spot size at beam dump.
    dump_rms_y=12e-3,
    loss=0.01             # Fractional loss along beamline.
)

lattice = from_file('example.seq')
lattice = lattice[:'dump']
quadrupoles = lattice[elements.Quadrupole]

QPL_limit = 11.1 / 14.62
QPK_limit = 6.88 / 14.62
QPK_magnets = {'gte1qd11', 'gte1qd12', 'ghadqd31', 'ghadqd32', 'ghadqd41', 'ghadqd42'}
polarity = {  # +1.0 means horizontally focusing.
    'gte1qd11':  1.0,
    'gte1qd12': -1.0,

    'gte2qt11':  1.0,
    'gte2qt12': -1.0,
    'gte2qt13':  1.0,

    'gth1qd11':  1.0,
    'gth1qd12': -1.0,

    'gth2qd11':  1.0,
    'gth2qd12': -1.0,
    'gth2qd21': -1.0,
    'gth2qd22':  1.0,

    'ghadqd11': -1.0,
    'ghadqd12':  1.0,
    'ghadqd21': -1.0,
    'ghadqd22':  1.0,

    'ghadqd31': -1.0,
    'ghadqd32':  1.0,
    'ghadqd41':  1.0,
    'ghadqd42': -1.0,

    'ghadqt51':  1.0,
    'ghadqt52': -1.0,
}
k1_bounds = {
    q.label: sorted([  # Lower bound must come first.
        polarity[q.label] * 1e-6,  # Variable strength quadrupoles must not be zero to retain their polarity.
        polarity[q.label] * (QPK_limit if q.label in QPK_magnets else QPL_limit)
    ]) for q in quadrupoles
}

for q in quadrupoles:
    # Using `k1.data` for updating the Parameter's value; using `+=` because it also works with `float` (`=` would
    # require the r.h.s to be a `torch.Tensor`).
    q.k1.data += math.copysign(1e-6, k1_bounds[q.label][0])

particles = pd.read_csv('particles.csv', index_col=0)
particles = torch.from_numpy(particles.values.T)

x, history, loss = lattice.linear(particles, observe=['target', 'dump'], recloss='accumulate')

learning_rates = it.cycle(np.logspace(-3, -6, 5))
optimizer = torch.optim.Adam(lattice.parameters(), lr=next(learning_rates))

cost_history = deque(maxlen=40)  # "maxlen" is the patience.
cost_history_running_avg = deque(maxlen=cost_history.maxlen)
cost_improvement_threshold = 0.001

for p in lattice.parameters():  # Clipping gradients helps stability during optimization (consider learning rate).
    p.register_hook(lambda grad: torch.clamp(grad, -1, 1))  # Max. update per step: clip_value * learning_rate.

for epoch in it.count(1):
    __, history, loss = lattice.linear(particles, observe=['target', 'dump'],
                                       recloss='sum',      # Sum the loss per element and per particle.
                                       exact_drift=False)  # Linear drifts speed up the computation.
    particles_lost = 1.0 - history['dump'].shape[1] / particles.shape[1]
    if particles_lost > optimization_targets['loss']:
        cost = (loss / particles.shape[1]) / optimization_targets['loss']  # Average loss per particle / target loss.
    else:
        cost = 0.  # Target fractional loss was reached, no need to optimize for that (at the current iteration).

    log_dict = dict(epoch=epoch, particles_lost=f'{particles_lost:.2f}')

    for place in ('target', 'dump'):
        # Only compare spot sizes to targeted ones if no more than 50% of the particles were lost.
        if history[place].shape[1] > particles.shape[1] // 2:
            x, y = history[place][[0, 2]]
            rms_x = x.std()
            rms_y = y.std()
            cost = (cost + torch.nn.functional.relu(rms_x / optimization_targets[f'{place}_rms_x'] - 1.0)
                    + torch.nn.functional.relu(rms_y / optimization_targets[f'{place}_rms_y'] - 1.0))
            log_dict.update({f'{place}_rms_x': f'{rms_x.data:.6f}', f'{place}_rms_y': f'{rms_y:.6f}'})
        else:
            log_dict.update({f'{place}_rms_x': 'n.a.', f'{place}_rms_y': 'n.a.'})
    log_dict['cost_to_optimize'] = cost.data
    logging.info(f'\t{log_dict}\n')

    if cost == 0:  # All optimization targets reached.
        break

    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    with torch.no_grad():
        for q in quadrupoles:
            q.k1.data.clamp_(*k1_bounds[q.label])  # Squeeze k1-values back into bounds if necessary.

    # Escape local minima by tracking the cost history and the running average thereof. If either stagnates, then
    # perform a cold restart of the optimizer and cycle through the learning rates.
    cost_history.append(cost.detach().item())
    if len(cost_history) == cost_history.maxlen:
        cost_history_running_avg.append(statistics.mean(cost_history))
        indicators = [max(cost_history) / min(cost_history) - 1.0,
                      list(cost_history)[0] / list(cost_history)[-1] - 1.0]
        if len(cost_history_running_avg) == cost_history_running_avg.maxlen:
            indicators.extend([max(cost_history_running_avg) / min(cost_history_running_avg) - 1.0,
                               list(cost_history_running_avg)[0] / list(cost_history_running_avg)[-1] - 1.0])
        if any(x < cost_improvement_threshold for x in indicators):
            optimizer = torch.optim.Adam(lattice.parameters(), lr=next(learning_rates))
            cost_history.clear()
            cost_history_running_avg.clear()
            logging.info('Cold restart of the optimizer')

madx_script = create_script(
    dict(charge=6, mass=11.1779291448, energy=28.5779291448),
    sequence=sequence_script(lattice),
    track=track_script(particles, observe=['target', 'dump'], maxaper=[100]*6)  # Aperture is already on the elements.
)
with open('result.madx', 'w') as fh:
    fh.write(madx_script)

results = run_script(madx_script, ['trackone', 'trackloss'], madx=os.path.expanduser('~/bin/madx'))
print('\nCrosscheck with MADX:')
print('\tFraction of particles lost:', len(results['trackloss'])/particles.shape[1])
print('\tBeam spot size at target:', results['trackone'].loc['target', ['X', 'Y']].values.std(axis=0))
print('\tBeam spot size at beam dump:', results['trackone'].loc['dump', ['X', 'Y']].values.std(axis=0))
