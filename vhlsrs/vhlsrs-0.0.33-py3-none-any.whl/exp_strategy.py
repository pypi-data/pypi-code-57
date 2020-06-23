"""
Define how to iterate over synthesis
"""

import logging
from pathlib import Path

from . import vivado_exp


class CSVHandler:
    def __init__(self, filename):
        self.file = Path(filename).resolve()
        with self.file.open("w") as f:
            f.write("version, cycles, II, estimated_period, "
                    "real_period, LUT, FF, DSP, BRAM, SRL\n")

    def handle(self, record):
        syn = record["syn"]
        impl = record["impl"]
        with self.file.open('a') as f:
            f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(
                syn['Vivado_HLS_Version'],
                syn['worst_case_latency'],
                syn['II'],
                syn['estimated_period'],
                impl['timing'],
                impl['LUT'],
                impl['FF'],
                impl['DSP'],
                impl['BRAM'],
                impl['SRL'])
            )


def minimize_latency(exp_settings: vivado_exp.Experiment, handlers):
    logger = logging.getLogger("vrs_log")
    handler = logging.FileHandler("{}.log".format(exp_settings.name), "w")
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info(f"Launching experiment {exp_settings.name}")
    logger.info("Starting without latency constraint")
    ret = exp_settings.run_exp(suffix = "_base").get_results()

    constraint = float(exp_settings.clock_period)

    for h in handlers:
        h.handle(ret)

    timing = float(ret['impl']['timing'])
    cycles = int(ret['syn']['worst_case_latency'])
    old_cycle = cycles + 1
    logger.info(f"Baseline result : {cycles} cycles at a clock period of {timing}ns")
    timings = {cycles: timing}
    up = cycles
    cur_best_timing = timing
    low = 1
    while up > low + 1 and cycles != old_cycle:
        old_cycle = cycles
        if cur_best_timing > constraint:
            mid = 2 * up
            up = 4 * up
        else:
            mid = low + (up - low) // 2
        logger.info(f"Running the experiment with a pipeline depth constraint of {mid}")
        ret = exp_settings.run_exp(
            depth_constraint=mid,
            suffix = f"_{mid}"
        ).get_results()

        for h in handlers:
            h.handle(ret)
        timing = float(ret['impl']['timing'])
        cycles = int(ret['syn']['worst_case_latency'])
        timings[cycles] = timing
        logger.info(f"Result : {cycles} cycles of {timing} ns")
        mid = cycles
        if timing <= constraint:
            up = mid
            cur_best_timing = timing
        else:
            low = mid
        logger.info(f"New interval : [{low},{up}]")
    logger.removeHandler(handler)

    best = up if (low == 1 or timings[low] > constraint) else low
    best_timing = timings[best]

    return best, best_timing
