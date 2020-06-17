# encoding=utf-8

import argparse
import sys
import textwrap

import pkg_resources

from ._prometheus import render
from ._zypper import get_applicable_patches, get_lifecycle_info, get_services_needing_restart, check_needs_reboot

LICENSE_TEXT = textwrap.dedent("""\
    Copyright (C) 2017 Matthias Bach

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.\
""")


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='Export patch status in Prometheus-compatible format..',
    )
    parser.add_argument(
        '--license', action='store_true', default=False,
        help='Show license information'
    )
    parser.add_argument('--version', action='version', version=str(
        pkg_resources.get_distribution('zypper-patch-status-collector').version
    ),)

    parsed_args = parser.parse_args(args)
    if parsed_args.license:
        print(LICENSE_TEXT)
        return

    run()


def run():
    try:
        patches = get_applicable_patches()
    except Exception as e:
        # in case of error, carry on
        print('Failed to query zypper: {}'.format(e), file=sys.stderr)
        patches = None

    try:
        services_needing_restart = get_services_needing_restart()
    except Exception as e:
        # in case of error, carry on
        print('Failed to query zypper: {}'.format(e), file=sys.stderr)
        services_needing_restart = None

    try:
        needs_reboot = check_needs_reboot()
    except Exception as e:
        # in case of error, carry on
        print('Failed to query zypper: {}'.format(e), file=sys.stderr)
        needs_reboot = False

    try:
        products = get_lifecycle_info()
    except Exception as e:
        # in case of error, carry on
        print('Failed to query zypper: {}'.format(e), file=sys.stderr)
        products = None

    metrics = render(patches, services_needing_restart, needs_reboot, products)
    print(metrics)

    if patches is None or products is None:
        sys.exit(1)
