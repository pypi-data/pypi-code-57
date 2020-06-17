# -*- coding: utf-8 -*-
"""
detection module for objects
"""

import cv2
import grpc

from sail_utils import LOGGER
from sail_utils.cv.base import (
    _Detector,
    _Mapper
)
from sail_utils.cv.object.config import (
    DEFAULT_TIME_OUT,
    DST_SIZE,
    THRESHOLD
)
from sail_utils.cv.object.protobuf import (
    inference_pb2,
    inference_pb2_grpc
)


def _unary_detect(stub, img, time_out=None):
    request = inference_pb2.ObjectDetectionRequest(request_info=__name__,
                                                   model_version=0)
    img_encode = cv2.imencode('.jpg', img)[1]
    request.image_data = img_encode.tobytes()
    response_f = stub.DetectKeyObject.future(request)
    try:
        response = response_f.result(timeout=time_out)
    except grpc.FutureTimeoutError as exception:
        LOGGER.warning(f"grpc <{exception.__str__()}>. just skip")
        rtn_value = []
    else:
        rtn_value = response.objects
    return rtn_value


def _format(resp, epoch: int, threshold: float, calibrator: _Mapper):
    results = []
    for res in resp:
        if res.score >= threshold:
            box = res.box
            xmin = box.xmin
            ymin = box.ymin
            xmax = box.xmax
            ymax = box.ymax

            results.append(
                dict(
                    location=calibrator([int(xmin), int(ymin), int(xmax), int(ymax)]),
                    time_stamp=epoch,
                    score=res.score,
                    label=res.label
                )
            )
    return sorted(results, key=lambda x: x['time_stamp'])


class KeyObjectDetector(_Detector):
    """
    class for key object detection
    """

    def __init__(self,
                 server: str,
                 src_size: int,
                 dst_size: int = DST_SIZE,
                 threshold: float = THRESHOLD,
                 timeout: float = DEFAULT_TIME_OUT):
        super().__init__(server, src_size, dst_size, threshold, timeout)

    def detect(self, img, epoch) -> list:
        """
        detect key object on one image
        :param img:
        :param epoch:
        :return:
        """
        img = self._mapper.resize(img)
        with grpc.insecure_channel(self._server) as channel:
            stub = inference_pb2_grpc.KeyObjectDetectionStub(channel)
            resp = _unary_detect(stub, img, self._timeout)
            return _format(resp, epoch, self._threshold, self._mapper)
