#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. See LICENSE file for license details

"""
Import a rosbag with images from several camera and position associated to the images recorded.
Works by default with the RealSense T265 camera.
Must have ROS installed, as well as rosbag module.
"""

from collections import OrderedDict
from enum import Enum, unique
import logging
import os
import os.path as path
import sys
from typing import Dict, List, Optional, Union
import numpy as np
import PIL.Image as PILImage
import quaternion
from tqdm import tqdm
# ros
import geometry_msgs.msg as rosmsg
import rosbag
import rospy.rostime
from rospy.rostime import Duration
# kapture
import kapture
import kapture.io.csv as kcsv
import kapture.io.structure
from kapture.io.records import get_image_fullpath
from kapture.utils.Collections import LimitedDictionary
from kapture.utils.paths import path_secure


rotation_cam_kapture_from_cam_ros = np.array([
    [0, -1, 0],
    [0, 0, -1],
    [1, 0, 0]
])

pose_kapture_from_ros = kapture.PoseTransform(r=quaternion.from_rotation_matrix(rotation_cam_kapture_from_cam_ros))
pose_ros_from_kapture = pose_kapture_from_ros.inverse()


class ImageInfo:
    """
    Image info found in the Rosbag
    """
    def __init__(self,
                 filename: str,
                 timestamp: rospy.rostime.Time,
                 camera_name: str):
        self.filename = filename
        self.timestamp = timestamp
        self.camera_name = camera_name


class PositionInfo:
    """
    Position info found in the Rosbag
    """
    def __init__(self,
                 timestamp: rospy.rostime.Time,
                 pose6d: rosmsg.Pose):
        self.timestamp = timestamp
        self.pose6d = pose6d


class RosBagImporter:
    """
    A importer of ROS bags with multi cam images data and odometry.
    The join between the two types of data is made on their data timestamps.
    """
    def __init__(self,
                 rosbag_path: str,
                 rig_sensors_kapture_path: str,
                 kapture_path: str,
                 force_overwrite_existing: bool = False) -> None:
        """

        :param rosbag_path: full path to the rosbag file
        :param rig_sensors_kapture_path: full path to a minimal kapture directory containing the rig and sensors of the
         multi-cam used to capture the data (images and odometry)
        :param kapture_path: full path to the top kapture directory to save
        :param force_overwrite_existing: silently overwrite kapture files if already exists
        """
        self._rig_sensors_kapture_path = path.abspath(rig_sensors_kapture_path)
        kapture_data = kcsv.kapture_from_dir(rig_sensors_kapture_path)
        if kapture_data.rigs is None or len(kapture_data.rigs) == 0:
            raise ValueError(f'Rig definition is empty in {rig_sensors_kapture_path}')
        self._rigs = kapture_data.rigs
        # Check we have only one rig_id defined
        rig_id = None
        for r_id in self._rigs.keys():
            if rig_id is None:
                rig_id = r_id
            elif r_id != rig_id:
                raise ValueError(f'Found rig_id {r_id} and {rig_id}:'
                                 f' there should be only one rig_id defined in {kapture_path}')
        if rig_id is None:
            raise ValueError(f'No rig defined in {kapture_data}')
        self._rig_id = rig_id
        if kapture_data.cameras is None or len(kapture_data.cameras) == 0:
            raise ValueError(f'Cameras definition is empty in {rig_sensors_kapture_path}')
        self.cameras = kapture_data.cameras
        self._sensors = kapture_data.sensors
        if not path.isfile(rosbag_path):
            raise ValueError(f'Rosbag file {rosbag_path} does not exist')
        self._rosbag_path = rosbag_path
        self._kapture_path = kapture_path
        self.logger = logging.getLogger('rosbag')
        self.logger.info(f'Reading rosbag file {rosbag_path} and exporting as Kapture format into {kapture_path}')
        os.makedirs(kapture_path, exist_ok=True)
        kapture.io.structure.delete_existing_kapture_files(kapture_path, force_overwrite_existing)
        self._images_full_path = get_image_fullpath(kapture_path)
        # Keys = timestamp, values odometer poses
        self._last_poses = LimitedDictionary(20)
        self.images_info = list()  # Of ImageInfo: type annotation is not supported in 3.6
        self.poses_info = list()  # Of PositionInfo

    def _save_image(self,
                    image_bitmap: np.ndarray,
                    image_directory_path: str,
                    image_number: int,
                    timestamp: rospy.rostime.Time) -> str:
        """
        Save the image.

        :param image_bitmap: the image bytes
        :param image_directory_path: directory where to save the image, under the top kapture directory
        :param image_number: image sequence number
        :param timestamp: image time stamp to set to the file
        :return: relative path (to the kapture path) of the file
        """
        # Define image file path
        image_path = os.path.join(image_directory_path, f'frame_{image_number:09d}.jpg')
        img = PILImage.fromarray(image_bitmap)
        img.save(image_path)
        # Set the capture time to the file saved
        taken_time = timestamp.to_sec()
        os.utime(image_path, (taken_time, taken_time))
        return path.relpath(image_path, self._images_full_path)

    def _find_pose(self, image_stamp: rospy.rostime.Time) -> Optional[rosmsg.Pose]:
        """
        Find the pose that has the smallest time difference with the image timestamp

        :param image_stamp: an image time stamp
        :return: a rosmsg pose if found, none otherwise
        """
        if len(self._last_poses) == 0:
            return None
        chosen_stamp = None
        smallest_delta = Duration(sys.maxsize)  # Very big delta
        for stamp in self._last_poses.keys():
            delta = abs(image_stamp-stamp)
            if delta < smallest_delta:
                smallest_delta = delta
                chosen_stamp = stamp
        return self._last_poses[chosen_stamp].pose

    def import_multi_camera(self, odometry_topic: str,
                            image_topics: Union[str, List[str]],
                            camera_identifiers: Union[str, List[str]],
                            percent: int = 100):
        """
        Import the rosbag data. Save the images on disk.
        The image topics list and camera identifiers list must be matching lists.

        :param odometry_topic: the odometry topic to use to compute the trajectory.
        :param image_topics: image topic(s) to import
        :param camera_identifiers: camera identifier(s) corresponding to the image topic(s)
        :param percent: percentage of images to keep.
        """

        # The image messages have the following structure:
        #
        # std_msgs/Header header
        # uint32 height
        # uint32 width
        # string encoding
        # uint8 is_bigendian
        # uint32 step
        # uint8[] data
        #

        # Check that we have an odometry topic
        if odometry_topic is None or len(odometry_topic) == 0:
            self.logger.fatal('Please provide an odometry topic')
            raise ValueError('Missing odometry topic')
        # Check that we have image topics
        if isinstance(image_topics, str):
            image_topics = [image_topics]
        if image_topics is None or len(image_topics) == 0:
            self.logger.fatal('Please provide image topics')
            raise ValueError('Missing image topic')
        # Check that we have as many camera identifiers as image topics
        if isinstance(camera_identifiers, str):
            camera_identifiers = [camera_identifiers]
        nb_image_topics = len(image_topics)
        if nb_image_topics != len(camera_identifiers):
            self.logger.fatal(f'Please provide an equal number of image topics and camera identifiers:'
                              f' {len(camera_identifiers)} cameras for {nb_image_topics} image topics.')
            raise ValueError('Unequal number of image topics and camera identifiers')

        # Make sure the camera identifiers are defined in the rigs kapture
        for camera_id in camera_identifiers:
            if self.cameras.get(camera_id) is None:
                raise ValueError(f'Camera identifier {camera_id} is not defined in {self._rig_sensors_kapture_path}')
        # Create images directories
        image_directory_path = OrderedDict()  # Should be OrderedDict[str, str]
        image_topic_to_cam_id = dict()
        for (image_topic, camera_id) in zip(image_topics, camera_identifiers):
            image_topic_to_cam_id[image_topic] = camera_id
            self.logger.info(f'images from {image_topic} mapped to camera {camera_id}')
            dir_path = path.join(self._images_full_path, camera_id)
            image_directory_path[image_topic] = dir_path
            os.makedirs(dir_path, exist_ok=True)
        self.logger.info(f'Saving images into {" ".join(dir_path for dir_path in image_directory_path.values())}')
        with rosbag.Bag(self._rosbag_path) as bag:
            bag_info = bag.get_type_and_topic_info()
            all_topics = list(bag_info[1].keys())
            self.logger.debug(f'Topics found {all_topics}')
            # Check topics
            if odometry_topic not in all_topics:
                raise ValueError(f'Missing topic {odometry_topic} in Rosbag')
            for image_topic in image_topics:
                if image_topic not in all_topics:
                    raise ValueError(f'Missing image topic {image_topic} in Rosbag')
            message_count = bag.get_message_count()
            self.logger.info(f"{message_count} messages in total")
            image_count_per_camera = -1
            for topic in all_topics:
                stats = bag_info[1][topic]
                count = stats[1]
                self.logger.info(f'In topic {topic:30s} {count:#10d} messages of type {stats[0]}')
                # Make sure we have the same number of images for all camera
                if topic in image_topics:
                    if image_count_per_camera >= 0:
                        assert count == image_count_per_camera, "All cameras have the same number of images"
                    image_count_per_camera = count

            # Read the messages
            num_msgs = 1
            image_number = 1
            saved_number = 0
            images_stamp = {}  # images time stamp of type rospy.rostime.Time per topic
            images_buffer = {}  # the images read as byte array per topic : Dict[str, np.ndarray]
            dir_last_image_time = {}  # image directory -> time of the last image written : Dict[str, float]
            count_to_skip = int(100 / percent) if percent < 100 else 1
            self.logger.info(f'Reading {image_count_per_camera} images per camera')
            if percent < 100:
                self.logger.info(f' Keeping {percent}% of the images')
            if not self.logger.isEnabledFor(logging.DEBUG):
                progress_bar = tqdm(total=image_count_per_camera)
            else:
                progress_bar = None
            topics_to_import = image_topics.copy()
            topics_to_import.append(odometry_topic)
            for topic, msg, t in bag.read_messages(topics=topics_to_import):
                # Consider the data timestamp, not the recording timestamp t
                stamp = msg.header.stamp
                if odometry_topic == topic:
                    self.logger.debug(f"{num_msgs:5d} ODOM STAMP='{stamp.secs}.{stamp.nsecs}'"
                                      f" msg.poseX='{msg.pose.pose.position.x}'")
                    self._last_poses[stamp] = msg.pose
                elif topic in image_topics:
                    self.logger.debug(f"{num_msgs:5d} {topic} STAMP='{stamp.secs}.{stamp.nsecs}'"
                                      f" HxW={msg.height}x{msg.width}")
                    images_stamp[topic] = stamp
                    img_buf = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width)
                    images_buffer[topic] = img_buf
                else:
                    self.logger.debug(f"{num_msgs:5d} Ignoring message of topic '{topic}'")
                # If we have all images, save them on disk
                if len(images_stamp) == nb_image_topics:
                    # The images are taken every 0.033 second
                    # Check all images have the same time stamp modulo epsilon
                    for topic1, stamp1 in images_stamp.items():
                        for topic2, stamp2 in images_stamp.items():
                            delta = (stamp1-stamp2).to_sec()
                            assert (abs(delta) < 0.001), "{topic1} and {topic2} images must have the same timestamp"
                    # Find the pose
                    pose6d = self._find_pose(stamp)
                    if pose6d:
                        self.poses_info.append(PositionInfo(stamp, pose6d))
                        # Save only some images
                        if ((image_number-1) % count_to_skip) == 0:
                            for image_topic in image_topics:
                                img = images_buffer[image_topic]
                                image_directory = image_directory_path[image_topic]
                                stamp = images_stamp[image_topic]
                                img_name = path_secure(self._save_image(img, image_directory, image_number, stamp))
                                dir_last_image_time[image_directory] = stamp.to_sec()
                                saved_number += 1
                                self.images_info.append(ImageInfo(img_name, stamp, image_topic_to_cam_id[image_topic]))
                        else:
                            self.logger.debug(f'    Skipping image number {image_number}')
                        image_number += 1
                        images_stamp.clear()
                        images_buffer.clear()
                        progress_bar and progress_bar.update(1)
                    # Else wait until we have the first pose
                num_msgs += 1
            progress_bar and progress_bar.close()
            for image_directory, dir_time in dir_last_image_time.items():
                os.utime(image_directory, (dir_time, dir_time))
            self.logger.info(f'Saved {saved_number} images')

    def save_to_kapture(self) -> None:
        """
        Save the data in kapture format.
        """
        # Convert pose info to trajectories
        trajectories = kapture.Trajectories()
        for pose_info in self.poses_info:
            t = pose_info.timestamp.to_nsec()
            ros_translation = pose_info.pose6d.position
            translation = [ros_translation.x,
                           ros_translation.y,
                           ros_translation.z]
            ros_rotation = pose_info.pose6d.orientation
            rotation = np.quaternion(ros_rotation.w,
                                     ros_rotation.x,
                                     ros_rotation.y,
                                     ros_rotation.z)
            # Transform the pose from the ROS body coordinate system defined here
            # https://www.ros.org/reps/rep-0103.html#axis-orientation
            # to the Kapture coordinate system

            # ros pose seems to be the inverse of the extrinsic matrix
            # i.e world position and rig orientation with respect to the world axis
            pose6d = kapture.PoseTransform.compose([pose_kapture_from_ros,
                                                    kapture.PoseTransform(rotation, translation).inverse(),
                                                    pose_ros_from_kapture])
            trajectories[(t, self._rig_id)] = pose6d
        # Convert image info to kapture image
        records_camera = kapture.RecordsCamera()
        for image_info in self.images_info:
            t = image_info.timestamp.to_nsec()
            records_camera[(t, image_info.camera_name)] = image_info.filename

        kapture_data = kapture.Kapture(rigs=self._rigs, sensors=self._sensors,
                                       records_camera=records_camera, trajectories=trajectories)
        self.logger.info(f'Saving to kapture {self._kapture_path}')
        kcsv.kapture_to_dir(self._kapture_path, kapture_data)
        self.logger.info('Done')
