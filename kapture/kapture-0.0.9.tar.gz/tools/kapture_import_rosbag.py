#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. See LICENSE file for license details

"""
Script to import a rosbag with images from several camera and position associated to the images recorded.
Works by default with the RealSense T265 camera.
"""

import argparse
import logging
import sys
# kapture
import path_to_kapture  # enables import kapture
import kapture.utils.logging

# rosbag
try:
    import rosbag
    from kapture.converter.ros_tools.import_rosbag import RosBagImporter

    has_rosbag = True
except ModuleNotFoundError:
    has_rosbag = False

logger = logging.getLogger('rosbag')  # Using global logger

# Default ROS topics: RealSense T265 camera
TOPIC_ODOMETRY = '/camera/odom/sample'
TOPIC_CAMERA_LEFT = '/camera/fisheye1/image_raw'
TOPIC_CAMERA_RIGHT = '/camera/fisheye2/image_raw'
DEFAULT_IMAGE_TOPICS = [TOPIC_CAMERA_LEFT, TOPIC_CAMERA_RIGHT]


def import_rosbag(args) -> None:
    """
    Import the rosbag with the parameters.

    :param args: arguments to use
    """
    # Read parameters
    importer = RosBagImporter(args.bag_file, args.kapture_rig, args.kapture_output, args.force)
    image_topics = args.image_topics
    if not image_topics:
        image_topics = DEFAULT_IMAGE_TOPICS
    importer.import_multi_camera(args.odometry_topic, image_topics, args.camera_identifiers, args.percent)
    importer.save_to_kapture()


def import_rosbag_command_line() -> None:
    """
    Do the rosbag to kapture import using the command line parameters provided by the user.
    """
    parser = argparse.ArgumentParser(description='Imports ROS bag file to kapture format.')
    parser_verbosity = parser.add_mutually_exclusive_group()
    parser_verbosity.add_argument('-v', '--verbose', nargs='?', default=logging.WARNING, const=logging.INFO,
                                  action=kapture.utils.logging.VerbosityParser,
                                  help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
    parser_verbosity.add_argument('-q', '--silent', '--quiet', action='store_const', dest='verbose',
                                  const=logging.CRITICAL)
    parser.add_argument('-y', '--force', action='store_true', default=False,
                        help='silently delete kapture data if already exists.')
    # create the parser for the import command #########################################################################
    parser.add_argument('-b', '--bag_file', default='input.bag',
                        help='bag file path', required=False)
    parser.add_argument('-r', '--kapture_rig',
                        help='kapture with rig and sensors definitions for the capturing equipment '
                             'corresponding to the ROS bag', required=True)
    parser.add_argument('-o', '--odometry_topic', default=TOPIC_ODOMETRY,
                        help=f'odometry topic to import, defaults to {TOPIC_ODOMETRY}', required=False)
    parser.add_argument('-i', '--image_topics', nargs="*",
                        help=f'list of image topics to import, defaults to {DEFAULT_IMAGE_TOPICS}',
                        required=False)
    parser.add_argument('-c', '--camera_identifiers', nargs="*",
                        help='list of camera identifiers as defined in the sensors file of the kapture rig'
                             ' and corresponding to the image topics in the same order;',
                        required=True)
    parser.add_argument('-p', '--percent', type=int, default=100,
                        help='percentage of images to keep', required=False)
    parser.add_argument('-k', '--kapture_output', required=True,
                        help='directory where to save Kapture files.')
    ####################################################################################################################
    args = parser.parse_args()

    logger.setLevel(args.verbose)
    if args.verbose <= logging.DEBUG:
        # for debug, let kapture express itself.
        kapture.utils.logging.getLogger().setLevel(args.verbose)
    logger.debug(f'{sys.argv[0]} \\\n' + '  \\\n'.join(
        '--{:20} {:100}'.format(k, str(v))
        for k, v in vars(args).items()))

    import_rosbag(args)


if __name__ == '__main__':
    if not has_rosbag:
        logger.fatal(f"You don't have ROS or import_rosbag installed")
        sys.exit(-1)
    try:
        import_rosbag_command_line()
    except (AssertionError, OSError, ValueError) as any_ex:
        logger.fatal(f'Fatal error: {any_ex}')
