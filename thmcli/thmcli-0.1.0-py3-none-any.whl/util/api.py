from os.path import expanduser, exists
from thmapi import THM


def get_api():
    if not exists(expanduser('~') + '/.thmcookie'):
        print("Please login first")
        exit()

    try:
        cookie = open(expanduser('~') + '/.thmcookie').read().strip()

        api = THM(credentials={'cookie': cookie})

        return api
    except:
        print("err, relog")
