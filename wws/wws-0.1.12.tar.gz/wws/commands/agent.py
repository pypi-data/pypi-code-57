import platform
import os
from os.path import expanduser
from pprint import pprint
from wws.commands.utils  import *
import re
from plumbum.cmd import launchctl

OSX_AGENT_CONF_PATH = '~/Library/LaunchAgents/com.porto.wws.plist'
OSX_AGENT_PROCESS_NAME = 'com.porto.wws'

class Agent:
    def __init__(self):
        super().__init__()

    def process(self, args):
        """ process the top level parameters and invoke subcommands 
        :param: args command line arguments
        :raise: Environment error when the os is not supported """
        getattr(self, args['cmd_agent'])(args)



    def configure(self, args):
        if args['verbose']:
            print("Command agent configure was called.")

        if args['verbose']:
            print(f"Configuring agent to fire at every {args['timer']} seconds.")

        if 'Darwin' in platform.system():
            _configure_osx_timer(args)
        elif 'Linux' in platform.system():
            _configure_linux_timer(args)
        else:
            raise EnvironmentError("Unsupported operating system")


    def start(self, args):
        global OSX_AGENT_CONF_PATH

        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        OSX_AGENT_CONF_PATH = expanduser(OSX_AGENT_CONF_PATH)
        if not os.path.exists(OSX_AGENT_CONF_PATH):
            print("Agent is not configured, aborting")
            exit()


        if args['verbose']: 
            print("Deploying new agent")

        out = launchctl['load', '-w', OSX_AGENT_CONF_PATH].run()
        
        if any('already' in l for l in map(str,out)):
            print("Agent is already loaded.")
        else:
            print("Agent started.")



    def stop(self, args):
        global OSX_AGENT_CONF_PATH
        OSX_AGENT_CONF_PATH = expanduser(OSX_AGENT_CONF_PATH)

        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        if not os.path.exists(OSX_AGENT_CONF_PATH):
            print("Agent is not configured, aborting")
            exit()

        if args['verbose']:
            print("Command agent stop was called.")
            print("Undeploying old agent")

        out = launchctl['unload', '-w', OSX_AGENT_CONF_PATH].run()
        if any('not find' in l for l in map(str,out)):
            print("Agent is already stopped.")
        else:
            print("Agent stopped.")



    def reload(self, args):
        if args['verbose']:
            print("Command agent reload was called.")
        self.stop(args)
        self.start(args)
        

    def status(self, args):
        global OSX_AGENT_CONF_PATH
        osxagent_file_path = expanduser(OSX_AGENT_CONF_PATH)


        if 'Darwin' not in platform.system():
            raise EnvironmentError("Unsupported operating system - only Mac OSX is supported right now")

        if args['verbose']:
            print("Command agent status was called.")

        out = launchctl['list'].run() 
        processes = [ i.split('\t')[2] for i in out[1].split('\n') if len(i.split('\t')) == 3 ]
        if OSX_AGENT_PROCESS_NAME in processes:
            print("Agent is running.")
            these_regex="<integer>(.+?)</integer>"
            pattern=re.compile(these_regex)

            with open(osxagent_file_path, 'r') as f:
                content = f.readlines()
                timerline = [ l for l in content if 'integer' in l ]
                timerline = re.findall(pattern, timerline[0])[0]
                print(f"It will fire periodically every {timerline} seconds.")

        else:
            print("Agent is not running.")




def _configure_osx_timer(args):
    global OSX_AGENT_CONF_PATH
    global OSX_AGENT_PROCESS_NAME

    pprint(args)
    script_path = get_script_path()
    configuration_file_path = expanduser(args['config'])
    database_file_path = expanduser(args['workspace_warp_database'])
    osxagent_file_path = expanduser(OSX_AGENT_CONF_PATH)

    seconds = int(args['timer'])

    text = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>{OSX_AGENT_PROCESS_NAME}</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/bin/python3</string>
            <string>{script_path}</string>
            <string>-c</string>
            <string>{configuration_file_path}</string>
            <string>-w</string>
            <string>{database_file_path}</string>
            <string>sync</string>
            <string>--up</string>
        </array>
        <key>StandardErrorPath</key>
        <string>/tmp/wws.err</string>
        <key>StandardOutPath</key>
        <string>/tmp/wws.log</string>
        <key>StartInterval</key>
        <integer>{seconds}</integer>
    </dict>
    </plist>    """
        
    with open(osxagent_file_path, "+w") as f:
        f.writelines(text)
    print("Agent configured.")

def _configure_linux_timer(args):
    raise EnvironmentError("Unsupported OS")