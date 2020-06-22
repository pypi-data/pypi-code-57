#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. See LICENSE file for license details

"""
Virtual gallery training data import.
"""

from collections import OrderedDict
import logging
import quaternion
from typing import Iterable, List
# kapture
import kapture
# local
from .virtual_gallery_constants import virtual_gallery_camera_model, virtual_gallery_width, virtual_gallery_height


logger = logging.getLogger('virtual_gallery')


class VirtualGalleryTrainingIntrinsic:
    """
    virtual gallery training intrinsics
    """

    def __init__(self, camera_id: int, intrinsics: list):
        self.camera_id = camera_id
        self.intrinsics = intrinsics

    def __hash__(self):
        return hash((self.camera_id, tuple(self.intrinsics)))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.camera_id == other.camera_id and self.intrinsics == other.intrinsics


class VirtualGalleryTrainingExtrinsic:
    """
    virtual gallery training extrinsics
    """

    def __init__(self, frame_id: int, light_id: int, loop_id: int, camera_id: int, extrinsics: list):
        self.light_id = light_id
        self.loop_id = loop_id
        self.camera_id = camera_id
        self.extrinsics = extrinsics
        self.frame_id = frame_id

    def __hash__(self):
        return hash((self.light_id, self.loop_id, self.camera_id, tuple(self.extrinsics), self.frame_id))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.light_id == other.light_id and
                self.loop_id == other.loop_id and
                self.camera_id == other.camera_id and
                self.extrinsics == other.extrinsics and
                self.frame_id == other.frame_id)


def import_training_intrinsics(input_root: str,
                               light_range: list,
                               loop_range: list,
                               camera_range: set) -> Iterable[VirtualGalleryTrainingIntrinsic]:
    """
    Import training intrinsics

    # format of intrinsic.txt is
    # frame cameraID K[0,0] K[1,1] K[0,2] K[1,2]
    # 0 0 1371.022 1371.022 959.5 539.5

    :param input_root:
    :param light_range:
    :param loop_range:
    :param camera_range:
    :return: intrinsics
    """
    # assert that all intrinsics are identical for one camera and take any
    intrinsics = []
    for light_id in light_range:
        for loop_id in loop_range:
            with open(f'{input_root}/training/gallery_light{light_id}'
                      f'_loop{loop_id}/intrinsic.txt', 'r') as file:
                lines = file.readlines()
                for split in map(lambda x: x.split(), lines):
                    if split[0].isdigit() and int(split[1]) in camera_range:
                        intrinsic = VirtualGalleryTrainingIntrinsic(
                            int(split[1]),
                            [float(split[2]), float(split[3]), float(split[4]), float(split[5])]
                        )
                        intrinsics.append(intrinsic)
    return OrderedDict.fromkeys(intrinsics).keys()


def import_training_extrinsics(input_root: str,
                               light_range: list,
                               loop_range: list,
                               camera_range: set) -> List[VirtualGalleryTrainingExtrinsic]:
    """
    Import training extrinsics.

    # format of extrinsic.txt is
    # frame cameraID r1,1 r1,2 r1,3 t1 r2,1 r2,2 r2,3 t2 r3,1 r3,2 r3,3 t3 0 0
    # 0 1
    # 0 0 0.929348 0 0.3692049 2.798107 0 1 0 1.65 -0.3692049 0 0.929348
    # 1.618328 0 0 0 1

    :param input_root:
    :param light_range:
    :param loop_range:
    :param camera_range:
    :return: extrinsics
    """
    extrinsics = []
    for light_id in light_range:
        for loop_id in loop_range:
            with open(f'{input_root}/training/gallery_light{light_id}'
                      f'_loop{loop_id}/extrinsic.txt', 'r') as file:
                lines = file.readlines()
                for split in map(lambda x: x.split(), lines):
                    if split[0].isdigit() and int(split[1]) in camera_range:
                        extrinsic = VirtualGalleryTrainingExtrinsic(
                            int(split[0]), light_id, loop_id, int(split[1]),
                            [float(value) for value in split[2:]]
                        )
                        extrinsics.append(extrinsic)
    return extrinsics


def _get_training_camera_name(camera_id: int) -> str:
    return f'training_camera_{camera_id}'


def convert_training_intrinsics(training_intrinsics: Iterable[VirtualGalleryTrainingIntrinsic],
                                sensors: kapture.Sensors) -> None:
    """
    Import all training intrinsics into the sensors definitions.

    :param training_intrinsics: training intrinsics to import
    :param sensors: list of sensor definitions where to add the new definitions
    """
    logger.info("Converting training cameras...")
    for intrinsic in training_intrinsics:
        camera_device_id = _get_training_camera_name(intrinsic.camera_id)
        camera = kapture.Camera(virtual_gallery_camera_model,
                                [virtual_gallery_width, virtual_gallery_height] + intrinsic.intrinsics)
        sensors[camera_device_id] = camera


def convert_training_extrinsics(offset: int, training_extrinsics: Iterable[VirtualGalleryTrainingExtrinsic],
                                images: kapture.RecordsCamera, trajectories: kapture.Trajectories) -> None:
    """
    Import all training extrinsics into the images and trajectories.

    :param offset:
    :param training_extrinsics: training extrinsics to import
    :param images: image list to add to
    :param trajectories: trajectories to add to
    """
    # Map (light_id, loop_id, frame_id) to a unique timestamp
    training_frames_tuples = ((extrinsic.light_id, extrinsic.loop_id, extrinsic.frame_id)
                              for extrinsic in training_extrinsics)
    training_frames_tuples = OrderedDict.fromkeys(training_frames_tuples).keys()
    training_frame_mapping = {v: n + offset for n, v in enumerate(training_frames_tuples)}

    # Export images and trajectories
    logger.info("Converting training images and trajectories...")
    for extrinsic in training_extrinsics:
        rotation_matrix = [extrinsic.extrinsics[0:3], extrinsic.extrinsics[4:7], extrinsic.extrinsics[8:11]]
        rotation = quaternion.from_rotation_matrix(rotation_matrix)
        timestamp = training_frame_mapping[(extrinsic.light_id, extrinsic.loop_id, extrinsic.frame_id)]
        camera_device_id = _get_training_camera_name(extrinsic.camera_id)
        translation_vector = [extrinsic.extrinsics[3], extrinsic.extrinsics[7], extrinsic.extrinsics[11]]
        images[(timestamp, camera_device_id)] = (f'training/gallery_light{extrinsic.light_id}_loop'
                                                 f'{extrinsic.loop_id}/frames/rgb/camera_{extrinsic.camera_id}'
                                                 f'/rgb_{extrinsic.frame_id:05}.jpg')
        trajectories[(timestamp, camera_device_id)] = kapture.PoseTransform(rotation, translation_vector)
