"""Covert SAS syntax to CSV"""
import argparse
import csv
import glob
import json
import os
import re
import sys

metadata = {"classifications":{},"variables":{}}


def get_line_indent(line):
    return len(re.match(r"\s*", line).group())

def is_empty_line(line):
    return len(line.strip()) == 0

def is_not_empty_line(line):
    return len(line.strip()) != 0

def parse_proc_format_values(sasfile, line):
    global metadata
    tokens = line.split()
    name = tokens[1]
    print("START PROC FORMAT VALUES "+name)
    classification = {"id":name}
    codes = {}
    classification["codes"]=codes
    while line:
        line = sasfile.readline()
        if is_empty_line(line): continue
        if get_line_indent(line) == 0: break
        line = line.strip()
        tokens = line.split("=",1)
        if len(tokens) == 2:
            value = tokens[0].strip().strip('"')
            label = tokens[1].strip().strip('"')
            print(value, "|", label)
            code = {"value":value, "label":label}
            codes[str(value)]=code
        if line.endswith(";"): break
    metadata["classifications"][name]=classification
    print("END PROC FORMAT VALUES "+name)
    return line

def parse_proc_format(sasfile, line):
    print("START PROC FORMAT")
    while line:
        line = sasfile.readline()
        if is_empty_line(line): continue
        if get_line_indent(line) == 0: break
        line = line.strip()
        print(line)
        if line.startswith('VALUE'):
            parse_proc_format_values(sasfile, line)
    print("END PROC FORMAT")
    return line

def parse(sasfile):
    line = True
    while line:
        line = sasfile.readline()
        if is_empty_line(line): continue
        line = line.strip()
        if line.startswith("PROC FORMAT"):
            line = parse_proc_format(sasfile, line)

def save_classifications(basename, bank=None):
    global metadata
    if len(metadata["classifications"]):
        with open(basename+"classifications.csv","w") as csvfile:
            fieldnames = ['bank', 'id', 'name']
            csvwriter = csv.writer(csvfile, fieldnames)
            rows = []
            for (_,classification) in metadata["classifications"].items():
                rows.append([bank, classification["id"], classification["id"]])
            csvwriter.writerow(fieldnames)
            csvwriter.writerows(rows)
        with open(basename+"code.csv","w") as csvfile:
            fieldnames = ['classification', 'codde', 'name']
            csvwriter = csv.writer(csvfile, fieldnames)
            rows = []
            for (_,classification) in metadata["classifications"].items():
                for (_,code) in classification["codes"].items():
                    rows.append([classification["id"], code["value"], code["label"]])
            csvwriter.writerow(fieldnames)
            csvwriter.writerows(rows)
# MAIN
if __name__ == '__main__':
    """Main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",nargs='+')
    args = parser.parse_args()

    print(args)

    for f in args.infile:
        sasfile = open(f,'r')
        parse(sasfile)
        #print(json.dumps(metadata,indent=3))
        save_classifications(f)


