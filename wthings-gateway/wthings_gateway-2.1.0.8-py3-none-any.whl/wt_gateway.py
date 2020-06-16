from wthings_gateway.gateway.wt_gateway_service import TBGatewayService
import argparse
parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--token', '-t', help='token，The corresponding access token on the WThings platform')
parser.add_argument('--config', '-c', help='config dir')
parser.add_argument('--log', '-l', help='log dir')
args = parser.parse_args()


def main():
    TBGatewayService(args.config, args.log, args.token)

if __name__ == '__main__':
    main()
