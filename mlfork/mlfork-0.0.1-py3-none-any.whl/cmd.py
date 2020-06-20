import argparse
import sys
import mlfork
import os

execname = 'mlfork'
getenv = lambda x: os.environ[x] if x in os.environ.keys() else None
key_id = os.environ['MLFORK_KEY_ID'] if 'MLFORK_KEY_ID' in os.environ.keys() else None
secret = getenv('MLFORK_SECRET')

def pull():
    parser = argparse.ArgumentParser(description='Pull a model from MLFork',
        usage=execname + ''' pull <runtime> <id>
        ''')
    parser.add_argument('runtime', help="Target Runtime")
    parser.add_argument('id', help="Model ID")
    args = parser.parse_args(sys.argv[2:])
    cli = mlfork.Client(api_key_id=key_id, api_secret=secret)
    fname = cli.get_model(args.id+'/'+args.runtime)
    print('Downloaded model: '+fname)

def push():
    parser = argparse.ArgumentParser(description='Push a model to MLFork',
        usage=execname + ''' push <path> [<id>]
        ''')
    parser.add_argument('path', help="Model path")
    parser.add_argument('id', help="Model ID", default=None, nargs='?')
    args = parser.parse_args(sys.argv[2:])
    cli = mlfork.Client(api_key_id=key_id, api_secret=secret)
    id = cli.push_model(args.path, args.id)
    print("Uploaded model: "+id)

def main():
    cmds = {
        'push': push,
        'pull': pull
    }
    parser = argparse.ArgumentParser(description='MLFork CLI Tool',
        usage=execname + ''' <command> [<args>]

Command list:
    push        Push trained model to MLFork
    pull        Pull a model from MLFork
''')
    parser.add_argument('command', help='Subcommand to execute', choices=cmds.keys())

    args = parser.parse_args(sys.argv[1:2])
    if args.command not in cmds:
        print('Unknown command')
        parser.print_help()
        exit(1)
    else:
        cmds[args.command]()
