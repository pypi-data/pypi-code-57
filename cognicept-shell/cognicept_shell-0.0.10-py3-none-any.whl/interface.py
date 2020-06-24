# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Main executable file to handle input arguments

import argparse
import os
import sys
import pkg_resources
sys.path.append("/home/jakub/code/cognicept-shell")

from cogniceptshell.configuration import Configuration
from cogniceptshell.agent_life_cycle import AgentLifeCycle



def main():

    # Create the parser
    parser = argparse.ArgumentParser(description='Shell utility to configure Cognicept tools.')

    parser.add_argument('--version', action='version', version=pkg_resources.require("cognicept-shell")[0].version)

    subparsers = parser.add_subparsers(help='', title="Commands")

    parser_config = subparsers.add_parser('config', help='Configure Cognicept tools')
    parser_status = subparsers.add_parser('status', help='Get status of Cognicept agents')
    parser_update = subparsers.add_parser('update', help='Update Cognicept tools')
    parser_restart = subparsers.add_parser('restart', help='Restart Cognicept agents')
    parser_stop = subparsers.add_parser('stop', help='Stops Cognicept agents')
    parser_orbitty = subparsers.add_parser('orbitty', help='Run Orbitty')

    local_cfg = Configuration()
    DEFAULT_PATH = "~/.cognicept/"
    parser_config.set_defaults(func=local_cfg.configure)
    parser_config.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_config.add_argument('--add',  help='Add new environmental variable in config file', action='store_true')
    parser_config.add_argument('--read',  help='Prints Cognicept configuration', action='store_true')

    agent_lifetime = AgentLifeCycle()
    parser_status.set_defaults(func=agent_lifetime.get_status)
    parser_status.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_restart.set_defaults(func=agent_lifetime.restart)
    parser_restart.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_stop.set_defaults(func=agent_lifetime.remove_agents)
    parser_stop.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_update.set_defaults(func=agent_lifetime.update)
    parser_update.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_orbitty.set_defaults(func=agent_lifetime.run_orbitty)
    parser_orbitty.add_argument('--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    # Add the arguments
    args = parser.parse_args()
    args.config = local_cfg
    
    if(hasattr(args,'func')):
        args.func(args)



if __name__ == "__main__":
    main()