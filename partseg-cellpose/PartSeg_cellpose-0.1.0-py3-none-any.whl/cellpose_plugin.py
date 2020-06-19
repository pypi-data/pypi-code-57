from abc import ABC
from copy import deepcopy
from enum import Enum
from typing import Callable, List, Union, Tuple

import numpy as np

from PartSegCore.algorithm_describe_base import SegmentationProfile, AlgorithmProperty, AlgorithmDescribeBase
from PartSegCore.channel_class import Channel
from PartSegCore.class_generator import enum_register
from PartSegCore.segmentation.algorithm_base import SegmentationResult, AdditionalLayerDescription
from PartSegCore.segmentation.noise_filtering import noise_filtering_dict
from PartSegCore.segmentation.segmentation_algorithm import StackAlgorithm

from cellpose import models


class CellposeModels(Enum):
    cyto = 0
    nuclei = 1

    def __str__(self):
        return self.name


enum_register.register_class(CellposeModels)

model = models.Cellpose(gpu=False, model_type="cyto")


class CellPoseBase(StackAlgorithm, ABC):
    def __init__(self):
        super().__init__()
        self.parameters = {}
        self.base_info = {}

    @classmethod
    def get_fields(cls) -> List[Union[AlgorithmProperty, str]]:
        return [
            AlgorithmProperty("nucleus_channel", "Nucleus", 0, property_type=Channel),
            AlgorithmProperty(
                "noise_filtering_nucleus",
                "Filter nucleus channel",
                next(iter(noise_filtering_dict.keys())),
                possible_values=noise_filtering_dict,
                property_type=AlgorithmDescribeBase,
            ),
            AlgorithmProperty("diameter", "Diameter", 30, options_range=(0, 10000)),
        ]

    def get_segmentation_profile(self) -> SegmentationProfile:
        return SegmentationProfile("", self.get_name(), deepcopy(self.parameters))

    def set_parameters(self, **kwargs):
        base_names = [x.name for x in self.get_fields() if isinstance(x, AlgorithmProperty)]
        if set(base_names) != set(kwargs.keys()):
            missed_arguments = ", ".join(set(base_names).difference(set(kwargs.keys())))
            additional_arguments = ", ".join(set(kwargs.keys()).difference(set(base_names)))
            raise ValueError(f"Missed arguments {missed_arguments}; Additional arguments: {additional_arguments}")
        self.parameters = deepcopy(kwargs)

    def get_data(self) -> Tuple[np.ndarray, Tuple[int, int]]:
        raise NotImplementedError()

    def calculation_run(self, report_fun: Callable[[str, int], None]) -> SegmentationResult:
        data, channels = self.get_data()
        masks, flows, styles, diams = model.eval(data, diameter=self.parameters["diameter"], channels=channels)
        add = {f"flows {i}": AdditionalLayerDescription(flow, layer_type="image") for i, flow in enumerate(flows)}
        add["mask"] = AdditionalLayerDescription(masks, layer_type="image")
        self.base_info["diams"] = diams
        self.base_info["styles"] = styles
        print(diams)
        return SegmentationResult(masks, self.get_segmentation_profile(), additional_layers=add)


class CellposeCytoSegmentation(CellPoseBase):
    def get_data(self) -> Tuple[np.ndarray, List[int]]:
        cell_channel = np.squeeze(
            noise_filtering_dict[self.parameters["noise_filtering_cells"]["name"]].noise_filter(
                self.image.get_channel(self.parameters["cell_channel"]),
                self.image.spacing,
                self.parameters["noise_filtering_cells"]["values"],
            )
        )
        nucleus_channel = np.squeeze(
            noise_filtering_dict[self.parameters["noise_filtering_nucleus"]["name"]].noise_filter(
                self.image.get_channel(self.parameters["nucleus_channel"]),
                self.image.spacing,
                self.parameters["noise_filtering_nucleus"]["values"],
            )
        )

        channel_shape = nucleus_channel.shape + (1,)
        zeros = np.zeros(channel_shape, dtype=cell_channel.dtype)
        res = np.concatenate(
            [cell_channel.reshape(channel_shape), nucleus_channel.reshape(channel_shape), zeros],
            axis=len(channel_shape) - 1,
        )
        return res, [1, 2]

    def get_info_text(self):
        return f"Estimated cell radius: {self.base_info['diams']}"

    @classmethod
    def get_name(cls):
        return "Cellpose cyto"

    @classmethod
    def get_fields(cls) -> List[Union[AlgorithmProperty, str]]:
        fields = super().get_fields()
        fields.insert(0, AlgorithmProperty("cell_channel", "Cells", 0, property_type=Channel))
        fields.insert(
            1,
            AlgorithmProperty(
                "noise_filtering_cells",
                "Filter cells channel",
                next(iter(noise_filtering_dict.keys())),
                possible_values=noise_filtering_dict,
                property_type=AlgorithmDescribeBase,
            ),
        )

        return fields


class CellposeNucleiSegmentation(CellPoseBase):
    def __init__(self):
        super().__init__()
        self.model = models.Cellpose(gpu=False, model_type="nuclei")

    def get_info_text(self):
        return ""

    @classmethod
    def get_name(cls):
        return "Cellpose nuclei"
