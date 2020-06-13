import sys
import json
import getpass
import argparse
from pathlib import Path
from colorama import init, Fore
from hpass.hpass_cli import cli_start
from hpass.encryption import random_password, hmac_sha256_digest

init(autoreset=True)


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--cli')
    parser = argparse.ArgumentParser(description='Hello Password')
    parser.add_argument('-v', '--version', help='View version information', action='version', version='%(prog)s v0.2.0')
    parser.add_argument('-r', '--random_password',
                        help='Randomly generate passwords containing uppercase and lowercase letters/numbers/symbols',
                        action='store', dest='password_length')
    parser.add_argument('-i', '--initialization',
                        help='Create or specify a password storage file in the current directory', action='store_true',
                        dest='init_switch')
    parser.add_argument('-c', '--cli', help='Start CLI Workbench', action='store_true', dest='cli_switch')
    args = parser.parse_args()

    if args.init_switch:
        _primary_password = getpass.getpass("Your primary password: ")
        _primary_password_repeat = getpass.getpass("Enter your primary password again: ")
        if _primary_password != _primary_password_repeat:
            print(Fore.RED + 'The password entered twice is different')
            return
        _primary = hmac_sha256_digest(value=_primary_password).decode('utf-8')
        config_dir = Path(__file__).resolve().parents[0] / 'config.json'
        hello_password_data_dir = str(Path.cwd() / 'helloPasswordData.json')
        config_json = {'primary': _primary, 'hello_password_data_dir': hello_password_data_dir}
        if Path(hello_password_data_dir).is_file():
            print(Fore.CYAN + 'Find the password storage file in the current directory')
        else:
            hello_password_data_json = {'gradual': 10, 'account': {}}
            with open(hello_password_data_dir, 'w', encoding='utf-8') as f:
                json.dump(hello_password_data_json, f, indent=4, ensure_ascii=False)
        with open(str(config_dir), 'w', encoding='utf-8') as f:
            json.dump(config_json, f, indent=4, ensure_ascii=False)
        print(Fore.GREEN + 'Password storage file initialized successfully')

    if args.password_length:
        try:
            _password_length = int(args.password_length)
            rp = random_password(length=_password_length)
            print(Fore.GREEN + rp)
        except ValueError:
            print(Fore.RED + 'The parameter `password_length` requires a number ' + Fore.RESET + '(E.g hpass -r 16)')

    if args.cli_switch:
        config_dir = Path(__file__).resolve().parents[0] / 'config.json'
        if config_dir.is_file():
            _primary_password = getpass.getpass("Your primary password: ")
            _primary = hmac_sha256_digest(value=_primary_password).decode('utf-8')
            with open(str(config_dir), 'r', encoding='utf-8') as f:
                config_json = json.load(f)
                if _primary != config_json['primary']:
                    print(Fore.RED + 'Primary password is incorrect')
                    return
            cli_start(primary=_primary_password, hello_password_data_dir=config_json['hello_password_data_dir'])
        else:
            print(Fore.GREEN + 'Hello Password is a simple password management tool')
            print(Fore.YELLOW + '  I need a new password storage file')
            print(Fore.CYAN + '    $ cd [Password storage file directory]')
            print(Fore.CYAN + '    $ hpass -i')
            print(Fore.CYAN + '    $ [Your primary password]')
            print(Fore.CYAN + '    $ [Enter your primary password again]')
            print(Fore.YELLOW + '  I already have a password storage file')
            print(Fore.CYAN + '    $ cd [Existing password storage file directory]')
            print(Fore.CYAN + '    $ hpass -i')
            print(Fore.CYAN + '    $ [Your primary password]')
            print(Fore.CYAN + '    $ [Enter your primary password again]')


if __name__ == '__main__':
    main()
