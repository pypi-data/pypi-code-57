from __future__ import absolute_import, division, print_function

import sys, argparse
from analysis.shared.metadata import Metadata, MetadataFactory

def run(inputs, unique_identifier):
    metadatas = [Metadata.parse_metadatafile(input_json, unique_identifier) for input_json in inputs]
    print(str(sum(metadatas, MetadataFactory.empty(unique_identifier))))
