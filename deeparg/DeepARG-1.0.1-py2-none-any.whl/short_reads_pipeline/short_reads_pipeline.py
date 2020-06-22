import argparse
from pipeline import pairedEndPipelineClass
import sys
import os
import time
import base64
import json
sys.path.insert(0, '/deeparg/short_reads_pipeline/')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forward_pe_file", type=str, required=True,
                        help="forward mate from paired end library",)
    parser.add_argument("--reverse_pe_file", type=str, required=True,
                        help="reverse mate from paired end library",)
    parser.add_argument("--output_file", type=str, required=True,
                        help="save results to this file prefix",)

    parser.add_argument("--deeparg_identity", type=float, default=80,
                        help="minimum identity for ARG alignments [default 80]",)
    parser.add_argument("--deeparg_probability", type=float, default=0.8,
                        help="minimum probability for considering a reads as ARG-like [default 0.8]",)
    parser.add_argument("--deeparg_evalue", type=float, default=1e-10,
                        help="minimum e-value for ARG alignments [default 1e-10]",)
    parser.add_argument("--gene_coverage", type=float, default=1,
                        help="minimum coverage required for considering a full gene in percentage. This parameter looks at the full gene and all hits that align to the gene. If the overlap of all hits is below the threshold the gene is discarded. Use with caution [default 1]",)
    parser.add_argument("--bowtie_16s_identity", type=float, default=0.8,
                        help="minimum identity a read as a 16s rRNA gene [default 0.8]",)

    parser.add_argument("--path_to_executables", type=str, default="/deeparg/short_reads_pipeline/bin/",
                        help="path to ./bin/ under short_reads_pipeline",)
    parser.add_argument("--path_to_deeparg", type=str, default="/deeparg/",
                        help="path where the deepARG program is installed",)

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    deep_arg_parameters = dict(
        identity=args.deeparg_identity,
        probability=args.deeparg_probability,
        evalue=args.deeparg_evalue,
        path=args.path_to_deeparg
    )

    parameters = dict(
        coverage=args.gene_coverage,
        identity_16s_alignment=args.bowtie_16s_identity
    )

    data = dict(
        pairedR1File=args.forward_pe_file,
        pairedR2File=args.reverse_pe_file,
        programs=args.path_to_executables,
        deep_arg_parameters=deep_arg_parameters,
        sample_output_file=args.output_file,
        parameters=parameters
    )

    pipe = pairedEndPipelineClass.PairedEnd(data)
    pipe.run()
