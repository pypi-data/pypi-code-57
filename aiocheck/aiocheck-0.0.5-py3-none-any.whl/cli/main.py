"""
    Entrypoint for running the CLI script

    Example:
    ```
    aiocheck.cli.main()
    ```
"""

import aiocheck

import os
import sys
import asyncio
import argparse


def main(addresses = []):
    """
        Entrypoint for running the CLI script

        Example:
        ```
        aiocheck.cli.main()
        ```
    """

    parser = argparse.ArgumentParser(description='Healthcheck')
    parser.add_argument(
        'addresses', metavar='address', type=str, default=[], nargs='*',
        help='one or more addresses to ping',
    )
    args = parser.parse_args()

    db = aiocheck.Database()
    if len(addresses) == 0:
        addresses = set(args.addresses)
    clear_console = lambda: os.system('cls' if os.name=='nt' else 'clear')

    def get_header(text):
        def wrap():
            result = ''
            for _ in range(len(text) + 4):
                result += '#'
            return result
        
        return f"{wrap()}\n# {text} #\n{wrap()}\n\nAddresses: {list(addresses)}\n"
    
    if len(addresses) == 0:
        select = ''
        while select != '0':
            inner_select = ''
            clear_console()
            print(f"{get_header('Menu')}\n[1] - Run\n[2] - Add Address\n[0] - Exit\n")
            select = input()
            
            if select == '0':
                sys.exit(0)
            
            if select == '1':
                if len(addresses) == 0:
                    input('No Address Provided ')
                else:
                    break
            
            if select == '2':
                clear_console()
                print(f"{get_header('Add Address')}")
                inner_select = input('Enter an Address: ')
                if len(inner_select) > 0:
                    addresses.add(inner_select)

    clear_console()
    sys.stdout.write(f"{get_header('Running')}\nPress CTRL+C to exit ")

    for address in addresses:
        db.insert(aiocheck.Host(address, db))

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
