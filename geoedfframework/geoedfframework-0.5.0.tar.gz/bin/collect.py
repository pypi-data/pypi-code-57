#!/usr/bin/env python

import os,sys

run_dir = os.getcwd()
workflow_stage = sys.argv[1]
target_dir = str(sys.argv[2])

out_file = "%s/results_%s.txt" % (run_dir,workflow_stage)

with open(out_file,'w') as output:
    for file_or_dir in os.listdir(target_dir):
        full_path = '%s/%s' % (target_dir,file_or_dir)
        if os.path.isfile(full_path):
            output.write('%s\n' % full_path)
