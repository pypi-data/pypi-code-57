# -*- coding: utf-8 -*-


"""
Munter Time Calculation
Alexander Vasarab
Wylark Mountaineering LLC

A rudimentary program which implements the Munter time calculation.
"""

import sys
import argparse

class InvalidUnitsException(Exception):
    pass

rates = {
    'uphill': { 'rate': 4, 'direction': '↑' },
    'flat': { 'rate': 6, 'direction': '→' }, # or downhill on foot
    'downhill': { 'rate': 10, 'direction': '↓' },
    'bushwhacking': { 'rate': 2, 'direction': '↹' },
}

unit_choices = ['metric', 'imperial']
travel_mode_choices = rates.keys()

def time_calc(distance, elevation, rate, units):
    retval = {}

    if units not in unit_choices:
        raise InvalidUnitsException

    unit_count = 0

    if 'imperial' == units:
        # convert to metric
        distance = (distance * 1.609) # mi to km
        elevation = (elevation * .305) # ft to m

    unit_count = distance + (elevation / 100.0)

    retval['time'] = (distance + (elevation / 100.0)) / rates[rate]['rate']
    retval['unit_count'] = unit_count
    retval['direction'] = rates[rate]['direction']
    retval['pace'] = rates[rate]['rate']

    return retval

def print_ugly_estimate(est):
    hours = int(est['time'])
    minutes = int((est['time'] - hours) * 60)
    print("{human_time}".format(
            human_time="{hours} hours {minutes} minutes".format(
                hours=hours,
                minutes=minutes)))

def print_pretty_estimate(est):
    hours = int(est['time'])
    minutes = int((est['time'] - hours) * 60)

    # NOTE: Below, the line with the unicode up arrow uses an alignment
    #       value of 31. In the future, consider using e.g. wcwidth
    #       library so that this is more elegant.
    print("\n\t╒═══════════════════════════════╕")
    print("\t╎▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╎╮")
    print("\t╎▒{:^29}▒╎│".format(''))
    print("\t╎▒{pace_readable:^31}▒╎│".format(
            pace_readable="{units} {direction} @ {pace}".format(
                units=round(est['unit_count']),
                direction=est['direction'],
                pace=est['pace'])))
    print("\t╎▒{human_time:^29}▒╎│".format(
            human_time="{hours} hours {minutes} minutes".format(
                hours=hours,
                minutes=minutes)))
    print("\t╎▒{:^29}▒╎│".format(''))
    print("\t╎▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╎│")
    print("\t╘═══════════════════════════════╛│")
    print("\t └───────────────────────────────┘\n")

def get_parser():
    parser = argparse.ArgumentParser(description='Munter Time Calculation')

    parser.add_argument('--distance',
        '-d',
        type=float,
        required=True,
        help='Distance (in km, by default)')

    parser.add_argument('--elevation',
        '-e',
        type=float,
        required=True,
        help='Elevation change (in m, by default)')

    parser.add_argument('--travel-mode',
        '-t',
        type=str,
        default='uphill',
        choices=travel_mode_choices, required=False,
        help='Travel mode (flat, by default)')

    parser.add_argument('--units',
        '-u',
        type=str,
        default='imperial',
        required=False,
        choices=unit_choices,
        help='Units of input values')

    parser.add_argument('--pretty',
        '-p',
        action='store_true',
        default=False,
        required=False);

    return parser

def main():
    parser = get_parser()
    opts = parser.parse_args()

    distance = opts.distance
    elevation = opts.elevation
    units = opts.units
    travel_mode = opts.travel_mode

    time_estimate = time_calc(distance, elevation, travel_mode, units=units)

    if opts.pretty:
        print_pretty_estimate(time_estimate)
    else:
        print_ugly_estimate(time_estimate)

    return 0

if __name__ == "__main__":
    sys.exit(main())
