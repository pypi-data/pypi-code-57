from pprint import pprint
from os.path import basename, normpath, abspath
import yaml
class Add:
    def __init__(self):
        super().__init__()

    def process(self, args):
        """ edits the warp database  """
        if args['debug']:
            pprint(args)
        with open(args['workspace_warp_database'],'r+') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not data:
                data = []
        
            # expand 
            args['local'] = abspath(args['local'])
            args['remote'] = [ abspath(a) for a in args['remote'] ]

            if not args['alias']:
                # add the last dir name as default
                args['alias'] = basename(normpath(args['local'])).lower()
                print(f"Since alias was not informed, suggesting one based on the source dir: {args['alias']}")

            if args['alias'] in [ a['alias'] for a in data ]:
                print("Alias already used. Choose another or remove it first")
                exit()

            entry = {
                "alias": args['alias'],
                "local": args['local'],
                "remote": args['remote'],
                "driver": "rsync",
                "opts": ["-avh", "--no-links" ,"--delete-after"],
            }
            data.append(entry)
            f.seek(0)
            f.truncate()
            yaml.dump(data, f, default_flow_style=False)
            # pprint(text)
            # f.write(text)

