import json
import time
from colorama import init, Fore, Back
from prettytable import PrettyTable
from hpass.encryption import random_password, encryption_rc4, decrypt_rc4

init(autoreset=True)


class HPassCli:
    def __init__(self, primary, hello_password_data_dir):
        self.__primary = primary
        self.hello_password_data_dir = hello_password_data_dir
        with open(hello_password_data_dir, 'r', encoding='utf-8') as f:
            password_data_json = json.load(f)
        self.__password_data_json = password_data_json

    def save_data_file(self):
        with open(self.hello_password_data_dir, 'w', encoding='utf-8') as f:
            json.dump(self.__password_data_json, f, indent=4, ensure_ascii=False)
        return

    @staticmethod
    def get_random_password(length):
        try:
            _password_length = int(length)
            print(Fore.GREEN + random_password(length=_password_length))
        except ValueError:
            print(Fore.RED + 'The parameter `Length` requires a number ' + Fore.RESET + '(E.g random 16)')
        return

    def get_password_all(self):
        pt_able = PrettyTable('ID Website Notes'.split(' '))
        for k, v in self.__password_data_json['account'].items():
            _data = decrypt_rc4(key=self.__primary, message=v)
            _data_dict = json.loads(_data)
            _data_list = [_data_dict['id'], _data_dict['website'], _data_dict['notes']]
            pt_able.add_row(_data_list)
        print(pt_able)
        return

    def get_password_search(self, search):
        pt_able = PrettyTable('ID Website Notes'.split(' '))
        for k, v in self.__password_data_json['account'].items():
            _data = decrypt_rc4(key=self.__primary, message=v)
            _data_dict = json.loads(_data)
            if search in _data_dict['website'] or search in _data_dict['notes']:
                _data_list = [_data_dict['id'], _data_dict['website'], _data_dict['notes']]
                pt_able.add_row(_data_list)
        print(pt_able)
        return

    def del_password(self, key):
        try:
            _message = self.__password_data_json['account'][key]
            print(Fore.WHITE + Back.RED + 'Please confirm that the operation target is this print content. Press Y/N')
            _data = decrypt_rc4(key=self.__primary, message=_message)
            _data_dict = json.loads(_data)
            print(Fore.CYAN + _data_dict['website'])
            print(Fore.CYAN + _data_dict['notes'])
            user_input = input('please enter: ')
            if user_input == 'Y' or user_input == 'y':
                del self.__password_data_json['account'][key]
                print(Fore.GREEN + 'Password successfully deleted !')
                self.save_data_file()
        except KeyError:
            print(Fore.RED + 'Password data not found')
        return

    def get_password(self, key):
        try:
            _message = self.__password_data_json['account'][key]
            _data = decrypt_rc4(key=self.__primary, message=_message)
            _data_dict = json.loads(_data)
            print('website = ' + _data_dict['website'])
            print('notes = ' + _data_dict['notes'])
            print('username = ' + _data_dict['username'])
            print('email = ' + _data_dict['email'])
            print('phone = ' + _data_dict['phone'])
            print('password = ' + Fore.GREEN + _data_dict['password'])
        except KeyError:
            print(Fore.RED + 'Password data not found')
        return

    def set_password(self, key, set_key):
        try:
            _message = self.__password_data_json['account'][key]
            _data = decrypt_rc4(key=self.__primary, message=_message)
            _data_dict = json.loads(_data)
            if set_key in _data_dict.keys():
                print(Fore.CYAN + 'Original ' + set_key + ' = ' + _data_dict[set_key])
                set_value_input = input('Now ' + set_key + ' = ')
                _data_dict[set_key] = set_value_input
                _now_password_str = json.dumps(_data_dict)
                _now_password_encryption = encryption_rc4(key=self.__primary, message=_now_password_str)
                self.__password_data_json['account'][key] = _now_password_encryption
                self.save_data_file()
                print(Fore.GREEN + 'Password value modified successfully!')
            else:
                print(Fore.RED + 'Password data does not have this value')
        except KeyError:
            print(Fore.RED + 'Password data not found')
        return

    def add_password(self):
        print(Fore.CYAN + 'The following is the information required for the new password :')
        website_input = input('Website = ')
        notes_input = input('Notes = ')
        username_input = input('Username = ')
        email_input = input('Email = ')
        phone_input = input('Phone = ')
        password_input = input('Password = ')
        new_password_dict = {
            'id': self.__password_data_json['gradual'],
            'website': website_input.strip(),
            'notes': notes_input.strip(),
            'username': username_input.strip(),
            'email': email_input.strip(),
            'phone': phone_input.strip(),
            'password': password_input.strip(),
            'time': time.time()
        }
        self.__password_data_json['gradual'] += 1
        _new_password_str = json.dumps(new_password_dict)
        _new_password_encryption = encryption_rc4(key=self.__primary, message=_new_password_str)
        self.__password_data_json['account'][new_password_dict['id']] = _new_password_encryption
        print(Fore.GREEN + 'The new password has been successfully added!')
        self.save_data_file()
        return


def cli_start(primary, hello_password_data_dir):
    h_pass_cli = HPassCli(primary=primary, hello_password_data_dir=hello_password_data_dir)
    while True:
        user_input = input('H-Pass> ')
        if user_input == 'exit' or user_input == 'quit':
            break
        else:
            if user_input == 'filepath':
                print(h_pass_cli.hello_password_data_dir)
            elif user_input == 'all':
                h_pass_cli.get_password_all()
            elif user_input == 'add':
                h_pass_cli.add_password()
            elif 'random' in user_input:
                user_input_list = user_input.split(' ')
                if len(user_input_list) != 2:
                    print('You may have to enter: ' + Fore.CYAN + 'random 16')
                    continue
                _length = user_input_list[1]
                if _length == '':
                    print(Fore.RED + 'Missing parameter `Length` ' + Fore.RESET + '(E.g random 16)')
                else:
                    h_pass_cli.get_random_password(length=_length)
            elif 'search' in user_input:
                user_input_list = user_input.split(' ')
                if len(user_input_list) != 2:
                    print('You may have to enter: ' + Fore.CYAN + 'search google')
                    continue
                _search = user_input_list[1]
                if _search == '':
                    print(Fore.RED + 'Missing parameter `Keyword` ' + Fore.RESET + '(E.g search google)')
                else:
                    h_pass_cli.get_password_search(search=_search)
            elif 'get' in user_input:
                user_input_list = user_input.split(' ')
                if len(user_input_list) != 2:
                    print('You may have to enter: ' + Fore.CYAN + 'get 10')
                    continue
                _key = user_input_list[1]
                if _key == '':
                    print(Fore.RED + 'Missing parameter `ID` ' + Fore.RESET + '(E.g get 10)')
                else:
                    h_pass_cli.get_password(key=_key)
            elif 'del' in user_input:
                user_input_list = user_input.split(' ')
                if len(user_input_list) != 2:
                    print('You may have to enter: ' + Fore.CYAN + 'del 10')
                    continue
                _key = user_input_list[1]
                if _key == '':
                    print(Fore.RED + 'Missing parameter `ID` ' + Fore.RESET + '(E.g del 10)')
                else:
                    h_pass_cli.del_password(key=_key)
            elif 'set' in user_input:
                user_input_list = user_input.split(' ')
                if len(user_input_list) != 3:
                    print('You may have to enter: ' + Fore.CYAN + 'set 10 notes')
                    continue
                _set = user_input_list[2]
                _key = user_input_list[1]
                if _key == '' or _set == '':
                    print(Fore.RED + 'Missing parameter `ID` ' + Fore.RESET + '(E.g set 10 notes)')
                else:
                    h_pass_cli.set_password(key=_key, set_key=_set)
            elif user_input == 'help':
                width = 18
                print('filepath'.ljust(width, ' '), '- Print the absolute path of the password storage file')
                print('all'.ljust(width, ' '), '- View the basic information of all password data')
                print('add'.ljust(width, ' '), '- Enter a new password data')
                print('search <keyword>'.ljust(width, ' '), '- Find password data by keyword')
                print('random <length>'.ljust(width, ' '), '- Generate a secure password of specified length')
                print('get <id>'.ljust(width, ' '), '- View the password data of the specified id')
                print('del <id>'.ljust(width, ' '), '- Delete the password data of the specified id')
                print('set <id> <key>'.ljust(width, ' '), '- Modify the key value of the password data of specified id')
            else:
                print(Fore.YELLOW + 'Is the instruction correct?')
