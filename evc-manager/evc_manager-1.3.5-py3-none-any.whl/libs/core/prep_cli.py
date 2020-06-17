""" Get CLI function to parse parameters provided via list
(not command line)"""


from ...libs.core.cli import CliOptions, create_parser


def get_cli(values):
    """ Prepare CLI """
    parser = create_parser()
    args = parser.parse_args(values)
    return CliOptions(parser, args)
