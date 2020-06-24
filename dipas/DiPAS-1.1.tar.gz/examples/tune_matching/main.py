import functools
import itertools as it
import os

import matplotlib.pyplot as plt
import pandas as pd
import torch

from dipas.build import create_script, from_script
import dipas.compute as compute
from dipas.elements import Kicker, Quadrupole, Parameter
from dipas.madx import run_script


print = functools.partial(print, end='\n\n')

with open('example.madx') as fh:
    script = fh.read()

result = run_script(
    script,
    {'twiss': True, 'twiss_error': True, 'twiss_matched': True, 'errors': False},
    madx=os.path.expanduser('~/bin/madx')
)
twiss = result['twiss']
twiss_error = result['twiss_error']
twiss_matched = result['twiss_matched']
errors = result['errors']

print('Tune values:')
print(f' - original: {        twiss[1]["Q1"]:.3f}, {        twiss[1]["Q2"]:.3f}')
print(f' - shifted : {  twiss_error[1]["Q1"]:.3f}, {  twiss_error[1]["Q2"]:.3f}')
print(f' - matched : {twiss_matched[1]["Q1"]:.3f}, {twiss_matched[1]["Q2"]:.3f}')

lattice = from_script(script, errors=errors).makethin({Kicker: 2}, style={Kicker: 'edge'})
h_quadrupoles = [q for q in lattice[Quadrupole] if q.k1 > 0]
for q in h_quadrupoles:
    q.k1 = Parameter(q.k1)
    q.update_transfer_map()

targets = {'Q1': torch.tensor(twiss[1]['Q1']), 'Q2': torch.tensor(twiss[1]['Q2'])}
optimizer = torch.optim.LBFGS(lattice.parameters())
cost_fn = torch.nn.MSELoss()

for step in it.count():
    def closure():
        optimizer.zero_grad()
        data = compute.twiss(lattice)
        Q1, Q2 = data['Q1'], data['Q2']
        cost = cost_fn(Q1, targets['Q1']) + cost_fn(Q2, targets['Q2'])
        print(f'Step {step:03d}: Q1 = {Q1:.3f}, Q2 = {Q2:.3f}, cost = {cost:.2e}')
        if cost < 1e-6:
            raise RuntimeError
        cost.backward(retain_graph=True)
        return cost

    try:
        optimizer.step(closure)
    except RuntimeError:
        break

    for q in h_quadrupoles:
        q.update_transfer_map()

twiss_check = run_script(
    create_script(sequence=lattice, errors=True, beam={'particle': 'proton', 'energy': 1}),
    twiss=True,
    madx=os.path.expanduser('~/bin/madx')
)['twiss']
print(f'Tune values (crosscheck with MADX): {twiss_check[1]["Q1"]:.3f}, {twiss_check[1]["Q2"]:.3f}')

q_names = [q.label.upper() for q in h_quadrupoles]
results = twiss_matched[0].set_index('NAME').loc[q_names, ['K1L']]
results = results.assign(DP=pd.Series([q.k1.item()*q.l.item() for q in h_quadrupoles], index=q_names))
results.columns = ['K1L_MADX', 'K1L_PF']
print(results)

ax = results.plot(kind='bar', figsize=(9, 4))
ax.set_ylabel('K1L [1/m]')
ax.plot([0, len(results)], [0.5086546699]*2, '--', color='red', label='initial')
ax.legend()
plt.show()
