from pprint import pprint
import yaml
from tabulate import tabulate
from funcy import project
import emoji
import os
import textwrap
class Ls:
    def __init__(self):
        super().__init__()

    def process(self, args):
        """ opens the warp database and print its content """
        with open(args['workspace_warp_database'],'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not data:
                data = []


        # when ls, verify which dir exists and mark import emoji

        if args['alias']:
            data = [ d for d in data if any( [ a for a in args['alias'] if a.upper() in d['alias'].upper() ]  )    ]


        if not args['verbose']:
            data = [ project(d,['alias', 'src', 'dst' ]) for d in data] 

        for item in data:

            # mark items that doesnt exists
            # src
            if not os.path.exists(item['src']):
                if args['debug']: 
                    print(f"Source path '{item['src']}'' does not exist yet, use 'sync fetch' to get it.")
                item['src'] = emoji.emojize(item['src'] + ":boom:", use_aliases = True)
            # break long paths into lines
            # item['src'] = '\n\t'.join(textwrap.wrap(text = item['src'], width = 40))

            # dst
            for i in range(len(item['dst'])):
                d = item['dst'][i]
                if not os.path.exists(d):
                    if args['debug']: 
                        print(f"Destination path '{d}'' does not exist yet, use 'sync push' to create.")
                    d = emoji.emojize(d + ":boom:", use_aliases = True)
                # d = '\n\t'.join(textwrap.wrap(text= d, width=40))
                item['dst'][i] = d
        
            # flatten list to better print it
            item['dst'] = '\n'.join(item['dst'])


        if 'table' in args['format']:
            print(tabulate(data, headers="keys", tablefmt = "grid"))
        elif 'tree' in args['format']:
            for item in data:
                print(item['alias'])
                print(f"    src: {item['src']}")
                print(f"    dst: {item['dst']}")
        else:
            raise Exception("Unknown format")
        
   
   