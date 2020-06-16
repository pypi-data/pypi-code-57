import argparse
import pprint
import json

from elexon import Elexon

def main():
    """Provide a simple CLI interface to the Elexon BMRS API"""
    parser = argparse.ArgumentParser(description="Query the Elexon BMRS API.")

    parser.add_argument('key', help='Elexon BMRS API Key')
    parser.add_argument('method', help='Elexon BMRS API Key')

    args = parser.parse_args()

    api = Elexon(args.key)

    data = api.request(args.method, SettlementDate = '2020-01-01', Period = '5')
    # generation = api.Transparency.B1620(SettlementDate = '2020-01-01', Period = '5')

    # data = api.Transparency.B1620(SettlementDate = '2020-01-01', Period = '5')
    # data = api.Legacy.PHYBMDATA(SettlementDate='2018-06-19',SettlementPeriod='1')
    # data = api.Transparency.B1720(SettlementDate='2019-12-04', Period='*')

    pprint.pprint(data)

if __name__ == "__main__":
    main()
