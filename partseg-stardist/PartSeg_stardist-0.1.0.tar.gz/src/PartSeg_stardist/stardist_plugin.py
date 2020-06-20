from copy import deepcopy
from typing import Callable, List, Union, Tuple

import numpy as np
from csbdeep.utils import Path, normalize
from stardist.models import StarDist2D, StarDist3D
from stardist.models.base import StarDistBase
from stardist.models.pretrained import get_registered_models


from PartSegCore.algorithm_describe_base import SegmentationProfile, AlgorithmProperty, AlgorithmDescribeBase
from PartSegCore.channel_class import Channel
from PartSegCore.segmentation.algorithm_base import SegmentationResult, AdditionalLayerDescription, \
    SegmentationLimitException
from PartSegCore.segmentation.noise_filtering import noise_filtering_dict
from PartSegCore.segmentation.segmentation_algorithm import StackAlgorithm


class StardistSegmentation(StackAlgorithm):
    def __init__(self):
        super().__init__()
        self.parameters = {}

    @classmethod
    def get_name(cls) -> str:
        return "StarDist 2D"

    def get_info_text(self):
        return ""

    @classmethod
    def get_fields(cls) -> List[Union[AlgorithmProperty, str]]:
        models = cls.get_model_list()
        return [
            AlgorithmProperty("channel", "Channel", 0, property_type=Channel),
            AlgorithmProperty(
                "noise_filtering",
                "Filter",
                next(iter(noise_filtering_dict.keys())),
                possible_values=noise_filtering_dict,
                property_type=AlgorithmDescribeBase,
            ),
            AlgorithmProperty("model", "Model", models[0], possible_values=models, property_type=list),
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

    def get_model(self) -> StarDistBase:
        return StarDist2D.from_pretrained(self.parameters["model"])

    @classmethod
    def get_model_list(cls):
        res = list(get_registered_models(StarDist2D)[0])
        try:
            res.remove("2D_versatile_he")
        except:
            pass
        return res

    def check_limitations(self):
        if not self.image.is_2d:
            raise SegmentationLimitException("only support 2D images")

    def calculation_run(self, report_fun: Callable[[str, int], None]) -> SegmentationResult:
        self.check_limitations()
        denoised =  noise_filtering_dict[self.parameters["noise_filtering"]["name"]].noise_filter(
                self.image.get_channel(self.parameters["channel"]),
                self.image.spacing,
                self.parameters["noise_filtering"]["values"],
            )
        model = self.get_model()
        normalized = normalize(denoised, 1, 99.8, )
        segmentation, details = model.predict_instances(normalized, axes=self.image.return_order.replace("C", ""))
        return SegmentationResult(segmentation, self.get_segmentation_profile(), additional_layers={
            "description": AdditionalLayerDescription(details, layer_type="image"),
            "segmentation": AdditionalLayerDescription(segmentation, layer_type="labels")
        })


class StardistSegmentation3D(StardistSegmentation):
    def check_limitations(self):
        if self.image.is_2d or self.image.is_time:
            raise SegmentationLimitException("only support 3D images")

    @classmethod
    def get_name(cls) -> str:
        return "StarDist 3D"

    def get_model(self) -> StarDistBase:
        return StarDist3D.from_pretrained(self.parameters["model"])

    @classmethod
    def get_model_list(cls):
        return list(get_registered_models(StarDist3D)[0])