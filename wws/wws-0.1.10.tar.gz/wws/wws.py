#! env python3
import sys
import os
from pprint import pprint
from funcy import merge
from wws.commands import utils

def agent(args):
    """  
        Synchronization agent command dispatcher
    """
    from wws.commands import agent
    if ['verbose']:
        print("agent command invoked")
    cmd = agent.Agent()
    cmd.process(args)

def cmd_agent(subparsers):
    subcommand = 'cmd_agent'
    cmd_parser = subparsers.add_parser('agent', help='Workspace synchronization agent management')
    action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    action_cmd_parser.add_argument('-s','--start',     action='store_const', const='start', dest=subcommand, help='Start the synchronization agent')
    action_cmd_parser.add_argument('-p','--stop',      action='store_const', const='stop', dest=subcommand, help='Stop the synchronization agent')
    action_cmd_parser.add_argument('-r','--reload',    action='store_const', const='reload', dest=subcommand, help='Reload the synchronization agent')
    action_cmd_parser.add_argument('-c','--configure', action='store_const', const='configure', dest=subcommand, help='Configure the synchronization agent')
    action_cmd_parser.add_argument('-u','--status', action='store_const', const='status', dest=subcommand, help='Configure the synchronization agent')
    cmd_parser.add_argument("--timer", "-t", default=1200, type=int  ,required=False)

# --------------------- --------------------- --------------------- --------------------- ---------------------

def ls(args):
    """  
        List workspace command dispatcher
    """
    from wws.commands import ls
    if ['verbose']:
        print("ls command invoked")
    cmd = ls.Ls()
    cmd.process(args)
 
def cmd_ls(subparsers):
    # ls command
    subcommand = 'cmd_ls'
    cmd_parser = subparsers.add_parser('ls', help='List synchronized workspaces')
    cmd_parser.add_argument("-a","--alias", nargs='+', required=False, help='specify the item or items to list')
    cmd_parser.add_argument("-o","--with-options", action = 'store_true', required=False, help='print detailed options')

    action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=False)
    action_cmd_parser.add_argument('-e','--tree', action='store_const', const = "tree", default = 'tree', dest='format', help='print output in tree format')
    action_cmd_parser.add_argument('-t','--table', action='store_const', const = "table", dest='format', help='print output in table format')

# --------------------- --------------------- --------------------- --------------------- ---------------------
def add(args):
    """  
        Add workspace command dispatcher
    """

    from wws.commands import add
    if ['verbose']:
        print("Add command invoked")
    cmd = add.Add()
    cmd.process(args)
 
def cmd_add(subparsers):
    # add command
    cmd_parser = subparsers.add_parser('add', help='Add synchronized workspaces')
    cmd_parser.add_argument("-a","--alias", type=str, required=False, help='Specify an alias for the warp point')
    cmd_parser.add_argument("-s","--src", "--source", type=str, required=True, help='Specify source path')
    cmd_parser.add_argument("-d","--dst", "--destination", nargs='+', required=True, help='Specify destination path')


# --------------------- --------------------- --------------------- --------------------- ---------------------
def rm(args):
    """  
        Remove workspace command dispatcher
    """
    from wws.commands import rm
    if ['verbose']:
        print("rm command invoked")
    cmd = rm.Rm()
    cmd.process(args)
 
def cmd_rm(subparsers):
    # ls command
    subcommand = 'cmd_rm'
    cmd_parser = subparsers.add_parser('rm', help='Remove synchronized workspaces')
    cmd_parser.add_argument("-a","--alias", nargs="+", required=True, help='Specify an alias for the warp point')
    # cmd_parser.add_argument("-s","--src", "--source", type=str, required=False, help='Specify source path')
    # cmd_parser.add_argument("-d","--dst", "--destination", nargs='+', required=False, help='Specify destination path')

# --------------------- --------------------- --------------------- --------------------- ---------------------
def sync(args):
    """  
        Sync workspace command dispatcher
    """
    from wws.commands import sync
    if ['verbose']:
        print("Sync command invoked")
    cmd = sync.Sync()
    cmd.process(args)
    
 
def cmd_sync(subparsers):
    # sync command
    subcommand = 'cmd_sync'
    cmd_parser = subparsers.add_parser('sync', help='Sync command to force  operations on workspaces')
    cmd_parser.add_argument("--dry-run", action='store_true', required=False, help='Non destructive operation, don\'t actually copies anything')
    cmd_parser.add_argument("-a","--alias", nargs='+', required=False, help='specify the item or items to selective sync')
    cmd_parser.add_argument('--force', action='store_true', help='force synchronize operations creating dirs when necessary')
    action_cmd_parser = cmd_parser.add_mutually_exclusive_group(required=True)
    action_cmd_parser.add_argument('--up', action='store_const', const='up', dest=subcommand, help='Copy data from local to remote')
    action_cmd_parser.add_argument('--down', action='store_const', const='down', dest=subcommand, help='Copy data from remote to local')


# --------------------- --------------------- --------------------- --------------------- ---------------------

def main():
    """ Workspace warp and sync utility. 
    This application helps you to keep local directories in synch with
    remote locations, usually cloud drives.
    """
    import argparse
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('-v', '--verbose', action = 'store_true', help = "Make the command verbose")
    main_parser.add_argument( "-c", "--config", default = "~/.wws/settings.yaml", help = "Set the configuration file", type=str  ,required=False)
    main_parser.add_argument( "-w", "--warp-database", default = "~/.wws/data.yaml", dest='workspace_warp_database', help = "Set workspace warp file", type=str  ,required=False)
    main_parser.add_argument( "-g", "--debug", dest='debug', action='store_true', required=False)

    # define commands 
    subparsers = main_parser.add_subparsers(dest='cmd_main', help="Available Workspace Warp and Sync commands")
    subparsers.required = True
    cmd_add(subparsers)
    cmd_rm(subparsers)
    cmd_ls(subparsers)
    cmd_sync(subparsers)
    cmd_agent(subparsers)

    # flatten arguments and invoke command dispatcher
    args = vars(main_parser.parse_args())
    
    # initialize settings
    args['config'] = os.path.expanduser(args['config'])
    # if the file exists
    if not os.path.exists(args['config']):
        if not utils._confirm(f"Workspace Warp settings not found, initialize an empty one at {args['config']}?"):
            print("Database initialization aborted. WWS was not configured.")
            exit()
        # if the directory of the file exists
        if not os.path.exists(os.path.dirname(args['config'])):
            if args['debug']:
                print("Creating configuration directory: %s " ,os.path.dirname(args['config']))
            # create the dir
            os.mkdir(os.path.dirname(args['config']))
        # create the file
        utils.init(args['config'])

    # load settings
    settings = utils.load_settings(args['config'])
    
    # coalesce a list of dicts into a single dict
    default_options = dict()
    for conf in settings:
        default_options =  merge(default_options, conf)
    # join settings overriding the default for command line  
    args = merge(default_options, args)
    
    args['workspace_warp_database'] = os.path.expanduser(args['workspace_warp_database'])
    if not os.path.exists(args['workspace_warp_database']):
        if not utils._confirm(f"Warp database not found, initialize an empty one at {args['workspace_warp_database']}?"):
            print("Database initialization aborted")
            exit()

        if not os.path.exists(os.path.dirname(args['workspace_warp_database'])):
            if args['debug']:
                print("Creating configuration directory: %s " ,os.path.dirname(args['workspace_warp_database']))
            # create the dir
            os.mkdir(os.path.dirname(args['workspace_warp_database']))
        # just create an emtpy file
        with open(args['workspace_warp_database'],'w+') as f:
            pass

    if args['debug'] or args['verbose']:
        pprint(args)

    # make sure binaries we use exists (rsync and rclone in the future)

    # invoke command
    getattr(sys.modules[__name__], args['cmd_main'])(args)
# --------------------- --------------------- --------------------- --------------------- ---------------------


if __name__ == '__main__':
    main()
