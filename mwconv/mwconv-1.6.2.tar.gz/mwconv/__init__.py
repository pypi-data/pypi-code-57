# coding=utf-8
#
# Copyright © 2016, Itinken Limited
#
# All rights reserved. Any redistribution or reproduction of part or
# all of the contents in any form is prohibited.
#
from __future__ import print_function
from __future__ import unicode_literals

import io
import sys
import argparse

from mwconv.wiki_parse import WikiParse
from mwconv.writer import *

html_header = '''<!DOCTYPE html>
<head>
<meta charset="utf-8">
<title>document</title>
<style type="text/css">
body {
font-size: 16px;
font-family: Verdana, Arial, sans-serif;
margin: 0 40px;
max-width: 700px;
}
h1 { font-size: 20px; }
h2 { font-size: 18px; }
pre {
border-left: 2px solid #a44;
padding-left: 20px;
background-color: #fff;
}
.hll { background-color: #ffffcc }
.c { color: #408080; font-style: italic } /* Comment */
.err { border: 1px solid #FF0000 } /* Error */
.k { color: #008000; font-weight: bold } /* Keyword */
.o { color: #666666 } /* Operator */
.ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.cm { color: #408080; font-style: italic } /* Comment.Multiline */
.cp { color: #BC7A00 } /* Comment.Preproc */
.cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.c1 { color: #408080; font-style: italic } /* Comment.Single */
.cs { color: #408080; font-style: italic } /* Comment.Special */
.gd { color: #A00000 } /* Generic.Deleted */
.ge { font-style: italic } /* Generic.Emph */
.gr { color: #FF0000 } /* Generic.Error */
.gh { color: #000080; font-weight: bold } /* Generic.Heading */
.gi { color: #00A000 } /* Generic.Inserted */
.go { color: #888888 } /* Generic.Output */
.gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.gs { font-weight: bold } /* Generic.Strong */
.gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.gt { color: #0044DD } /* Generic.Traceback */
.kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.kp { color: #008000 } /* Keyword.Pseudo */
.kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.kt { color: #B00040 } /* Keyword.Type */
.m { color: #666666 } /* Literal.Number */
.s { color: #BA2121 } /* Literal.String */
.na { color: #7D9029 } /* Name.Attribute */
.nb { color: #008000 } /* Name.Builtin */
.nc { color: #0000FF; font-weight: bold } /* Name.Class */
.no { color: #880000 } /* Name.Constant */
.nd { color: #AA22FF } /* Name.Decorator */
.ni { color: #999999; font-weight: bold } /* Name.Entity */
.ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.nf { color: #0000FF } /* Name.Function */
.nl { color: #A0A000 } /* Name.Label */
.nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.nt { color: #008000; font-weight: bold } /* Name.Tag */
.nv { color: #19177C } /* Name.Variable */
.ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.w { color: #bbbbbb } /* Text.Whitespace */
.mb { color: #666666 } /* Literal.Number.Bin */
.mf { color: #666666 } /* Literal.Number.Float */
.mh { color: #666666 } /* Literal.Number.Hex */
.mi { color: #666666 } /* Literal.Number.Integer */
.mo { color: #666666 } /* Literal.Number.Oct */
.sb { color: #BA2121 } /* Literal.String.Backtick */
.sc { color: #BA2121 } /* Literal.String.Char */
.sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.s2 { color: #BA2121 } /* Literal.String.Double */
.se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.sh { color: #BA2121 } /* Literal.String.Heredoc */
.si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.sx { color: #008000 } /* Literal.String.Other */
.sr { color: #BB6688 } /* Literal.String.Regex */
.s1 { color: #BA2121 } /* Literal.String.Single */
.ss { color: #19177C } /* Literal.String.Symbol */
.bp { color: #008000 } /* Name.Builtin.Pseudo */
.vc { color: #19177C } /* Name.Variable.Class */
.vg { color: #19177C } /* Name.Variable.Global */
.vi { color: #19177C } /* Name.Variable.Instance */
.il { color: #666666 } /* Literal.Number.Integer.Long */
</style>
</head>
<body>
'''

out_types = {
    'html': {'pre': html_header, 'writer': HtmlWriter},
    'text': {'pre': '', 'writer': TextWriter},
    'mw': {'pre': '', 'writer': MwikiWriter},
    'md': {'pre': '', 'writer': MdWriter},
    'md_safe': {'pre': '', 'writer': MdSafeWriter},
}


def main():
    ap = argparse.ArgumentParser('mwconv')
    ap.add_argument('-o', dest='output_file',
                          help="write to this file (default stdout)",
                          default=None, metavar="FILE")
    ap.add_argument('-t', '--type', dest='output_type',
                          help="select output type", default='html',
                          metavar="TYPE")
    ap.add_argument('-l', '--first-level', dest='first_level',
                          help="set the level of the first heading in the output",
                          default=None, metavar="NUMBER")
    ap.add_argument('files', nargs='+', help='input files to process')

    opts = ap.parse_args()

    # Get the output file
    if opts.output_file:
        out = io.open(opts.output_file, 'wt')
    else:
        out = io.open(1, 'wt')

    out_type = out_types[opts.output_type]

    # Any initial header part to the file
    out.write(out_type['pre'])

    try:
        for filename in opts.files:
            with io.open(filename, 'rt') as f:
                writer = out_type['writer'](out)
                parser = WikiParse(first_level=opts.first_level)
                parser.parse(f, writer)
    finally:
        out.close()
