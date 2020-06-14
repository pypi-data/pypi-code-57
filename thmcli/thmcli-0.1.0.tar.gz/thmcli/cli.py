from thmcli.commands import *
import argh


def main():
    p = argh.ArghParser()
    p.add_commands([
        login,
        logout,

        roominfo
    ])
    p.dispatch()


if __name__ == '__main__':
    main()
