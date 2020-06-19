#! /usr/bin/python3.6
import os

root_dir = 'v5automation_files-r25'

for root, dirs, files in os.walk(root_dir):

    files = [f for f in files if f.endswith(".htm")]

    for d in dirs:
        for file in files:
            print(root, d, file)
