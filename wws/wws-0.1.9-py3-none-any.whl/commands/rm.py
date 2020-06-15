from pprint import pprint
import yaml
from tabulate import tabulate
from funcy import project
from wws.commands import utils

class Rm:
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

        
            remove_entries = dict()
            keep_entries = dict()
        
            remove_entries = [ d for d in data if any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ]  )  ]
            keep_entries = [ d for d in data if not any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ]  )  ]


            
            if not args['verbose']:
                data = [ project(d,['alias', 'src', 'dst' ]) for d in remove_entries] 
            else:
                data = remove_entries

            if not data:
                print("Nothing to remove.")
                exit()
            
            print("Entries to remove:")
            print(tabulate(data, headers="keys", tablefmt = "psql"))
            rm = utils._confirm("Are you sure to remove these entries?")

            if rm:
                f.seek(0)
                f.truncate()
                yaml.dump(keep_entries, f, default_flow_style=False)

            print("Aliases were removed but data remain untouched. Please remove the listed source directories.")


            