import yaml
from os import path
from os.path import expanduser
import pathlib
from plumbum import local, FG, BG, TF, RETCODE
from plumbum.cmd import rsync
from pprint import pprint
from funcy import project
from wws.commands import utils
import time
class Sync:
    def __init__(self):
        super().__init__()

    def process(self, args):
        getattr(self, args['cmd_sync'])(args)

    def up(self, args):
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not data:
                data = []


        # filter only the selected aliases
        if args['alias']:
            data = [ d for d in data if any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ])]

        start = time.time()
        # synchronize warp points
        for item in data:

            if not path.exists(item['src']):
                if args['debug'] or args['verbose']:
                    print(f"Source path '{item['src']}' does not exits, skipping.")
                    continue

            if args['debug'] or args['verbose']:
                print(f"synchronizing {item['src']}")

            for dst in item['dst']:
                # this approach need rework for remote locations (rsync over ssh)...
                if not path.exists(dst): 
                    if args['force']:
                        print("Force creating remote directory")
                        if not args['dry_run']:
                            pathlib.Path(dst).mkdir(parents=True, exist_ok=True)    
                    else:
                        if args['debug'] or args['verbose']:
                            print(f"Destination path '{dst}' does not exits, skipping.")
                        continue

                params = []
                if args["dry_run"]:
                    params.append("--dry-run")

                # include global patterns
                for ex in args['exclude_patterns']:
                    params.append(f"--exclude={ex}")

                # include per workspace options
                if item['opts']:
                    params.extend(item['opts'])

                # fix source and destination
                if item['src'][-1] is not '/':
                    item['src'] += '/'
                if dst[-1] is not '/':
                    dst += '/'
                

                # finish with source -> dest
                params.append(item['src'])
                params.append(dst)
                if args['debug']:
                    pprint(params)

                if args["verbose"]: # for safety always dry run
                    print(f"\tto: {dst}")
                
                out = rsync[params].run() 
                if args["debug"] or args['dry_run']: 
                    pprint(out) 
        
        end = time.time()
        from plumbum.cmd import osascript
        osascript['-e',f'display notification "[WWS] Workspace synchronized in {int(end - start)} seconds!"'].run()


 


    def down(self, args):
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not data:
                data = []


        # filter only the selected aliases
        if args['alias']:
            data = [ d for d in data if any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ])]

        start = time.time()
        # synchronize warp points
        for item in data:

            if not path.exists(item['src']):
                if args['force']:
                    print("Force creating local directory")
                    if not args['dry_run']:
                        pathlib.Path(item['src']).mkdir(parents=True, exist_ok=True)    
                else:
                    if args['debug'] or args['verbose']:
                        print(f"Local path '{item['src']}' does not exits, skipping.")
                    continue


            if args['debug'] or args['verbose']:
                print(f"synchronizing {item['src']}")

            # select the first remote path
            dst = item['dst'][0]

            # this approach need rework for remote locations (rsync over ssh)...
            if not path.exists(dst): 
                if args['debug'] or args['verbose']:
                    print(f"Remote path '{dst}' does not exits, skipping.")
                continue

            params = []
            if args["dry_run"]:
                params.append("--dry-run")

            # include global patterns
            for ex in args['exclude_patterns']:
                params.append(f"--exclude={ex}")

            # include per workspace options
            if item['opts']:
                params.extend(item['opts'])

            # fix source and destination
            if item['src'][-1] is not '/':
                item['src'] += '/'
            if dst[-1] is not '/':
                dst += '/'
            

            # finish with reversing direction remote -> local
            params.append(dst)
            params.append(item['src'])
            if args['debug']:
                pprint(params)

            if args["verbose"]: # for safety always dry run
                print(f"\tto: {dst}")
            
            out = rsync[params].run() 
            if args["debug"] or args['dry_run']: 
                pprint(out) 

        end = time.time()
        from plumbum.cmd import osascript
        osascript['-e',f'display notification "[WWS] Workspace synchronized in {int(end - start)} seconds!"'].run()
