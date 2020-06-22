# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Featurize images from model produced by another run."""

from azureml.contrib.automl.dnn.vision.classification.inference.score import featurize
import argparse


def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', help='run id of the experiment that generated the model')
    parser.add_argument('--experiment_name', help='experiment that ran the run which generated the model')
    parser.add_argument('--output_file', help='path to output file')
    parser.add_argument('--root_dir', help='path to root dir for files listed in image_list_file')
    parser.add_argument('--image_list_file', help='image files list')
    parser.add_argument('--input_dataset_id', help='input dataset id')

    args = parser.parse_args()

    featurize(args.run_id, experiment_name=args.experiment_name, output_file=args.output_file,
              root_dir=args.root_dir, image_list_file=args.image_list_file,
              input_dataset_id=args.input_dataset_id)


if __name__ == "__main__":
    # execute only if run as a script
    main()
