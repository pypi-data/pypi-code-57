from argparse import ArgumentParser, FileType
from ._run import run

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='alicorn',
        description="The python grpc server and framework",
    )
    parser.add_argument('app', type=str, nargs=1, help='Path to the alicorn app to launch')

    parser.add_argument('--host', default='localhost', type=str, help='Listen on the given host')
    parser.add_argument('--port', default=9000, type=int, help='Listen on the given port')
    parser.add_argument(
        '--ssl',
        nargs=2,
        metavar='PRIVATE_KEY CERTIFICATE_CHAIN',
        help='Creates the secure port with the given private key and certificate chain. Can be called multiple times',
        action='append'
    )
    parser.add_argument(
        '--root-certificate', default=None, type=FileType('r'), help='A root certificate to verify clients against'
    )
    parser.add_argument(
        '--client-auth', action='store_true', help='Require client authentication, requires --root-certificate'
    )

    parser.add_argument('--debug', store='store_true', help='Enable debugging mode')
    run(parser.parse_args())
