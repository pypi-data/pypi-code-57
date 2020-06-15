"""Metassheet Command Line Utility"""
import argparse
import glob
import sys

from .util import repository
from .util.serializers import bq
from .util.serializers import ddi
from .util.serializers import mockaroo
from .util.serializers import mysql
from .util.serializers import rds
from .util.serializers import rml
from .util.serializers import sts
from .util.serializers import vertica

def main(args=None):
    """Main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",nargs='+')
    parser.add_argument("-c", "--config", help="The configuration file to use (overrides default)")
    parser.add_argument("-a", "--all", action='store_true', help="Generates all outputs")
    parser.add_argument("-bq", action='store_true', help="Generates output for BigQuery")
    parser.add_argument("-ddi", help="Generates output for DDI Codebook")
    parser.add_argument("--dump", help="Resources to dump")
    parser.add_argument("-pandas", action='store_true', help="Generates output for Python Pandas")
    parser.add_argument("-mock", "--mockaroo", action='store_true', help="Generates output for Mockaroo")
    parser.add_argument("-mockopts", "--mockaroo-options", action='append', dest="mockaroo_options", default=[],
                        help="Mockaroo serializer option(s)")
    parser.add_argument("-mysql", action='store_true', help="Generates output for MySql")
    parser.add_argument("-rds", action='store_true',
                        help="Generates output for MTNA Rich Data Services")
    parser.add_argument("-rml", action='store_true',
                        help="Generates output for MTNA Resource Modeling Language")
    parser.add_argument("-rmlopts", "--rml_option", action='append', dest="rml_options", default=[],
                        help="RML serializer option(s)")
    parser.add_argument("-sts", action='store_true', help="Generates output for Stat/Transfer")
    parser.add_argument("-save", help="Save workspace to pickle file", nargs='?', const="workspace.p", type=str)
    parser.add_argument("-load", help="Load workspace from pickle file",  nargs='?', const="workspace.p", type=str)
    parser.add_argument("-o","--out", help="Output base name", nargs='?', default="metasheet", type=str)
    parser.add_argument("-vertica", action='store_true', help="Generates output for Vertica SQL")
    args = parser.parse_args()
    print(args)

    # base output filename
    base_path = args.out

    # LOAD
    if args.load:
        repository.load(args.load)
    else: 
        files = []
        for entry in args.infile:
            for file in glob.glob(entry):
                files.append(file)
            if len(files)>0:
                repository.parseFiles(files)
            else:
                print("No matching input file(s) found....")
                exit(1)
        pass
    workspace = repository.getWorkspace()

    # dump workspace
    if args.dump:
        if "class" in args.dump:
            workspace.dump(type="classification")
        if "code" in args.dump:
            workspace.dump(type="code")
        if "rec" in args.dump:
            workspace.dump(type="record")
        if "lay" in args.dump:
            workspace.dump(type="layout")
        if "var" in args.dump:
            workspace.dump(type="variable")

    # Workspace stats
    print()
    workspace.stats()

    if args.save:
        repository.save(args.save)

    # Outputs
    print(base_path)

    if args.bq or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.bq.json', 'w')
            try:
                bq.generateRecordLayout(resource, workspace, format="fixed", file=outfile)
            except:
                print("*** Unexpected error:", sys.exc_info()[0])
            outfile.close()

    if args.ddi or args.all:
        print()
        if args.ddi:
            version = args.ddi
        else:
            version = "2.5"
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.ddi.xml', 'w')
            ddi.generateRecordLayout(resource, workspace, version=version, file=outfile)
            outfile.close()

    if args.mockaroo or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.mockaroo.json', 'w')
            mockaroo.generateRecordLayout(resource, workspace, file=outfile, options=args.mockaroo_options)
            outfile.close()

    if args.mysql or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.mysql.sql', 'w')
            mysql.generateRecordLayout(resource, workspace, file=outfile)
            outfile.close()

    if args.rds or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path + '.' + resource.getId() + '.rds.json', 'w')
            rds.generateRecordLayout(resource, workspace, file=outfile)
            outfile.close()

    if args.rml or args.all:
        print()

        if workspace.getResources(type="classification"):
            outfile = open(base_path+'.classifications.rml', 'w')
            rml.generateClassifications(workspace, file=outfile, options=args.rml_options)
            outfile.close()

        if workspace.getResources(type="variable"):
            outfile = open(base_path+'.variables.rml', 'w')
            rml.generateVariables(workspace, file=outfile, options=args.rml_options)
            outfile.close()

        if workspace.getResources(type="record"):
            outfile = open(base_path+'.record_layouts.rml', 'w')
            rml.generateRecordLayouts(workspace, file=outfile, options=args.rml_options)
            outfile.close()

        if workspace.getResources(type="rule"):
            outfile = open(base_path+'.rules.rml', 'w')
            rml.generateRules(workspace, file=outfile, options=args.rml_options)
            outfile.close()

    if args.sts or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.sts', 'w')
            sts.generateRecordLayout(resource, workspace, format="fixed", file=outfile)
            outfile.close()

    if args.vertica or args.all:
        print()
        for resource in workspace.getResources(type="record"):
            outfile = open(base_path+'.'+resource.getId()+'.vertica.sql', 'w')
            vertica.generateRecordLayout(resource, workspace, file=outfile)
            outfile.close()


if __name__ == '__main__':
    main()

    
