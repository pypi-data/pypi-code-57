#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import argparse
from transfer._coredir import *

# handy default files

def getOpts():
    
    parser = argparse.ArgumentParser( 
        formatter_class = argparse.RawDescriptionHelpFormatter, 
        description = '''
                        Transfer directories between clusters
                        ''')
    parser.add_argument('-f', '--file',
                        metavar  = "",
                        type     = str,
                        required = True,
                        help     = '[Required] File with list of directories')
    parser.add_argument('-p', '--params',
                        metavar  = "",
                        type     = str,
                        required = True,
                        help     = '[Required] File with transfer parameters')    
    parser.add_argument('-g', '--glob',
                        metavar  = "",
                        type     = str,
                        default  = None,
                        help     = '[Optional] File with glob patterns [Default = None]')
    return parser.parse_args()

def main():
    args = getOpts()
    
    frc, toc  = str_gather(args.params)
    dirs      = open(args.file   , "r").readlines()
    glob_patt = open(args.glob, "r").readlines() if args.glob else None

    rest_out  = "rest_" + args.file
    done      = []

    m1 = "      ,       : %s\r"
    m2 = "Pulled,       : %s\r"
    m3 = "Pulled, Pushed: %s\r"

    for d in dirs:
        tmp  = d.strip()
        
        # down
        sys.stdout.write("\n")
        sys.stdout.write(m1 % tmp)
        sys.stdout.flush()

        run_downlist(
            glob_patt = glob_patt,
            frc       = frc,
            directory = tmp
        )
        sys.stdout.write(m2 % tmp)
        sys.stdout.flush()

        # up
        run_string( 
            toc.format( d = tmp ) 
        )
        sys.stdout.write(m3 % tmp)
        sys.stdout.flush()

        shutil.rmtree(tmp)

        done += [d]
        write_rest(dirs, rest_out, done)
        
    sys.stdout.write("\n\n")
    os.remove(rest_out)
  
if __name__ == "__main__":
    main()
