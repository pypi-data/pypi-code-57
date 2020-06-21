#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright 2018-2019 New York University Abu Dhabi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The CAMeL Tools Arabic cleaning utility.

Usage:
    camel_arclean [-o OUTPUT | --output=OUTPUT]
                  [-E INPUT_ENCODING | --input-encoding=INPUT_ENCODING]
                  [-O OUTPUT_ENCODING | --output-encoding=OUTPUT_ENCODING]
                  [FILE]
    camel_arclean (-v | --version)
    camel_arclean (-h | --help)

Options:
  -E INPUT_ENCODING --input-encoding=INPUT_ENCODING
        The encoding of the input file. Defaults to "utf-8".
  -o OUTPUT --output=OUTPUT
        Output file. If not specified, output will be printed to stdout.
  -O OUTPUT_ENCODING --output-encoding=OUTPUT_ENCODING
        The encoding of the output file. Defaults to "utf-8".
  -h --help
        Show this screen.
  -v --version
        Show version.
"""


import sys

from docopt import docopt

import camel_tools
from camel_tools.utils.charmap import CharMapper


__version__ = camel_tools.__version__


def _open_files(finpath, foutpath, input_enc, output_enc):
    if finpath is None:
        fin = sys.stdin
    else:
        try:
            fin = open(finpath, 'r', encoding=input_enc)
        except UnicodeDecodeError:
            sys.stderr.write('Error: Incorrect encoding for input file {}.'
                             '\n'.format(repr(finpath)))
            sys.exit(1)
        except LookupError:
            sys.stderr.write('Error: Invalid encoding {}.'
                             '\n'.format(repr(input_enc)))
            sys.exit(1)
        except Exception:
            sys.stderr.write('Error: Couldn\'t open input file {}.'
                             '\n'.format(repr(finpath)))
            sys.exit(1)

    if foutpath is None:
        fout = sys.stdout
    else:
        try:
            fout = open(foutpath, 'w', encoding=output_enc)
        except LookupError:
            sys.stderr.write('Error: Invalid encoding {}.'
                             '\n'.format(repr(output_enc)))
            sys.exit(1)
        except Exception:
            sys.stderr.write('Error: Couldn\'t open output file {}.'
                             '\n'.format(repr(foutpath)))
            if finpath is not None:
                fin.close()
            sys.exit(1)

    return fin, fout


def _arclean(mapper, fin, fout):
    for line in fin:
        fout.write(mapper.map_string(line))
    fout.flush()


def main():  # pragma: no cover
    try:
        version = ('CAMeL Tools v{}'.format(__version__))
        arguments = docopt(__doc__, version=version)

        # Open files (or just use stdin and stdout)
        fin, fout = _open_files(arguments['FILE'],
                                arguments['--output'],
                                arguments['--input-encoding'],
                                arguments['--output-encoding'])

        try:
            mapper = CharMapper.builtin_mapper('arclean')
            _arclean(mapper, fin, fout)

        # If everything worked so far, this shouldn't happen
        except Exception:
            sys.stderr.write('Error: An error occured during cleaning.\n')
            fin.close()
            fout.close()
            sys.exit(1)

            # Cleanup
            if arguments['FILE'] is not None:
                fin.close()
            if arguments['--output'] is not None:
                fout.close()

        sys.exit(0)
    except KeyboardInterrupt:
        sys.stderr.write('Exiting...\n')
        sys.exit(1)
    except Exception:
        sys.stderr.write('Error: An unknown error occurred.\n')
        sys.exit(1)


if __name__ == '__main__':  # pragma: no cover
    main()
