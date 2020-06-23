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
            args['src'] = abspath(args['src'])
            args['dst'] = [ abspath(a) for a in args['dst'] ]

            if not args['alias']:
                # add the last dir name as default
                args['alias'] = basename(normpath(args['src'])).lower()
                print(f"Since alias was not informed, suggesting one based on the source dir: {args['alias']}")

            if args['alias'] in [ a['alias'] for a in data ]:
                print("Alias already used. Choose another or remove it first")
                exit()

            entry = {
                "alias": args['alias'],
                "src": args['src'],
                "dst": args['dst'],
                "driver": "rsync",
                "opts": ["-avh", "--no-links" ,"--delete-after"],
            }
            data.append(entry)
            f.seek(0)
            f.truncate()
            yaml.dump(data, f, default_flow_style=False)
            # pprint(text)
            # f.write(text)

