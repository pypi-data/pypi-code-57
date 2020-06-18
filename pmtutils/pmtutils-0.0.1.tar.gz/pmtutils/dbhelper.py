#!/usr/bin/env python3

'''
Author: Ben Lambert

Helper class to construct indexed database of reads. Reads files must be all fasta, all fastq, or bgzipped.
'''

import subprocess
import os
from glob import glob
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
import logging

logging.basicConfig(filename='db.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class DBBuilder:

    @staticmethod
    def generate_alignment(input_fasta):
        clustal_path = r"/home/ben/clustalw-2.1-linux-x86_64-libcppstatic/clustalw2"
        clustalw_cline = ClustalwCommandline(clustal_path, infile=input_fasta)
        stdout, stderr = clustalw_cline()
        #Untested logging.
        logging.INFO(str(stdout))
        logging.INFO(str(stderr))


    @staticmethod
    def calculate_distance_matrix(aln_file):
        aln = AlignIO.read(open(aln_file), 'clustal')
        calculator = DistanceCalculator('blosum62')
        dm = calculator.get_distance(aln)
        with open(os.path.splitext(aln_file)[0] + ".dist") as f:
            f.write(dm)
    
    # Implement sed run to loop through pe reads and prepend id.
    @staticmethod
    def add_read_id(db_dir):
        pass

    @staticmethod
    def index_reads(db_dir, filetype='fq'):

        if filetype == 'fa':
            file_list = glob(f"{db_dir}/*fasta*")
            file_list.extend(glob(f"{db_dir}/*fa*"))
            print(file_list)
            for file in file_list:
                command = f"samtools faidx {file}"
                subprocess.check_call(command, shell=True)

        else:
            file_list = glob(f"{db_dir}/*fastq*")
            file_list.extend(glob(f"{db_dir}/*fq*"))
            for file in file_list:
                command = f"samtools fqidx {file}"
                subprocess.check_call(command, shell=True)
