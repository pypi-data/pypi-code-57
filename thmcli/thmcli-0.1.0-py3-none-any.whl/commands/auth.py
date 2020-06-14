from getpass import getpass
from os.path import expanduser, exists
from os import remove
from thmapi import THM


def login():
    if exists(expanduser('~') + '/.thmcookie'):
        print("You're already logged in. Do you want to logout first?")
        choice = input("[y/N]") or 'n'

        if choice == 'y':
            print('logout')
            remove(expanduser('~') + '/.thmcookie')
        else:
            return

    print("Please enter your username/password")
    username = input("Username: ")
    password = getpass("Password: ")

    api = THM(credentials={
        'username': username,
        'password': password
    })

    f = open(expanduser('~') + '/.thmcookie', 'w+')
    f.write(api.session.cookies.get('connect.sid'))
    f.close()


def logout():
    print("Do you want to logout?")
    choice = input("[y/N]") or 'n'

    if choice == 'y':
        print('logout')
        remove(expanduser('~') + '/.thmcookie')
    else:
        return
