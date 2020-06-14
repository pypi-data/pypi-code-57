# -----------------------------------------------------------------------------
# Created: Sun 14 Jun 2020 16:54:06 IST
# Last-Updated: Sun 14 Jun 2020 17:23:48 IST
#
# main.py is part of random-readme-badges
# URL: https://gitlab.com/justinekizhak/random-readme-badges
# Description: Main
#
# Copyright (c) 2020, Justine Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------


"""Main"""

import random
import click
from random_readme_badges import models as m


@click.group()
def main():
    """Main entrypoint function. Everything in this run before any of the
    subcommand
    """
    pass


@main.command()
@click.option(
    "-n",
    "--number_of_badges",
    "number_of_badges",
    default=3,
    help="Number of badges you want",
)
def get(number_of_badges):
    """Print out random badges from the list"""
    data = random.sample(m.badge_list, number_of_badges)
    print(*data, sep=", \n")


if __name__ == "__main__":
    main()
