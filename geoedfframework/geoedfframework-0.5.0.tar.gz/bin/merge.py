#!/usr/bin/env python

import os,sys

num_args = len(sys.argv)
out_dir = os.getcwd() #sys.argv[1]
workflow_stage = sys.argv[2]
filter_var = str(sys.argv[3])

out_file = "%s/results_%s_%s.txt" % (out_dir,workflow_stage,filter_var)

with open(out_file,'w') as output:
    for i in range(4,num_args):
        with open(str(sys.argv[i]),'r') as in_file:
            for line in in_file:
                output.write(line)
