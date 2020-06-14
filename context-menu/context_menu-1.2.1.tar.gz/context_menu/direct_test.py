def command(*args, **kwargs):
    print(args)
    print(kwargs)
    input()

#
if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.abspath('.'))
    import menus

    menus.FastCommand('test', type='FILES', python=command).compile()
