# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score images from model produced by another run."""

from azureml.contrib.automl.dnn.vision.object_detection.writers.score import score
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import ScoringParameters, FasterRCNNParameters
import argparse


def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', help='run id of the experiment that generated the model')
    parser.add_argument('--experiment_name', help='experiment that ran the run which generated the model')
    parser.add_argument('--output_file', help='path to output file')
    parser.add_argument('--root_dir', help='path to root dir for files listed in image_list_file')
    parser.add_argument('--image_list_file', help='image object detection files list')
    parser.add_argument("--batch_size", type=int, help="batch size for inference",
                        default=ScoringParameters.DEFAULT_SCORING_BATCH_SIZE)
    parser.add_argument('--output_dataset_target_path', help='datastore target path for output dataset files')
    parser.add_argument('--input_dataset_id', help='input dataset id')

    # Faster-rcnn Settings
    parser.add_argument("--min_size", type=int,
                        help="minimum size of the image to be rescaled before feeding it to the backbone",
                        default=FasterRCNNParameters.DEFAULT_MIN_SIZE)
    parser.add_argument("--box_score_thresh", type=float,
                        help="during inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=FasterRCNNParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument("--box_nms_thresh", type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=FasterRCNNParameters.DEFAULT_BOX_NMS_THRESH)
    parser.add_argument("--box_detections_per_img", type=int,
                        help="maximum number of detections per image, for all classes.",
                        default=FasterRCNNParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    args = parser.parse_args()

    fasterrcnn_settings = {'min_size': args.min_size,
                           'box_score_thresh': args.box_score_thresh,
                           'box_nms_thresh': args.box_nms_thresh,
                           'box_detections_per_img': args.box_detections_per_img}

    score(args.run_id, experiment_name=args.experiment_name, output_file=args.output_file,
          root_dir=args.root_dir, image_list_file=args.image_list_file, batch_size=args.batch_size,
          output_dataset_target_path=args.output_dataset_target_path,
          input_dataset_id=args.input_dataset_id, **fasterrcnn_settings)


if __name__ == "__main__":
    # execute only if run as a script
    main()
