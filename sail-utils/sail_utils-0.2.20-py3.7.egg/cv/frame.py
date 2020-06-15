# -*- coding: utf-8 -*-
"""
module for reading in stream
"""

from dataclasses import dataclass
import glob
import subprocess as sp
import time

import cv2
import numpy as np

from sail_utils.cv.base import _Streamer


class LiveStreamer(_Streamer):
    """
    class for read from a live feed
    """

    def __init__(self, source: str, rate: float, max_errors: int = 3600):
        super().__init__(source, rate)
        self._stream = cv2.VideoCapture(self.source)
        self._fps = self._stream.get(cv2.CAP_PROP_FPS)
        self._need_to_wait = 1. / rate
        self._last_time = - 1. / rate
        self._error_frames = 0
        self._max_errors = max_errors

    @property
    def max_errors_allowed(self) -> int:
        """
        get number of max errors allowed
        :return:
        """
        return self._max_errors

    @property
    def fps(self) -> int:
        """
        get stream fps
        :return:
        """
        return self._fps

    def __iter__(self):
        return self

    def __next__(self):
        while self._stream.isOpened():
            ret, frame = self._stream.read()
            if ret:
                current_time = time.time()
                need_to_wait = self._last_time + self._need_to_wait - current_time
                self._error_frames = 0

                if need_to_wait < 0:
                    self._last_time = current_time
                    return frame, current_time
                time.sleep(need_to_wait * 0.30)
            else:
                self._error_frames += 1
                if self._error_frames >= self._max_errors:
                    self._error_frames = 0
                    raise StopIteration(f"# of error {self._error_frames} "
                                        f"is greater than allowed. stop stream")
        else:
            raise ValueError(f"<{self._stream}> is closed. please reconnect")

    def __del__(self):
        self._stream.release()


class ImageFileStreamer(_Streamer):
    """
    class for read from a folders file
    """

    def __init__(self, source, suffix: str = 'jpg', rate: int = 1):
        super().__init__(source, rate)
        self._stream = glob.glob((self._source / ("**" + suffix)).as_posix(), recursive=True)
        self._stream = sorted(self._stream, key=lambda x: (len(x), x))
        self._rate = rate
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._start >= len(self._stream):
            raise StopIteration()

        file_loc = self._stream[self._start]
        self._start += self._rate
        img = cv2.imread(file_loc, cv2.IMREAD_COLOR)
        return img, file_loc


class VideoFileStreamer(_Streamer):
    """
    class for read frame from a video file
    """

    def __init__(self, source: str, rate: int = 1):
        super().__init__(source, rate)
        self._rate = rate
        self._stream = cv2.VideoCapture(self.source)
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            ret, img = self._stream.read()
            if not ret:
                raise StopIteration

            self._start += 1
            if self._start % self._rate == 0:
                return img, None


class LivePusher:
    """
    class for live stream writer
    """

    def __init__(self, url: str, width: int, height: int, fps: int):
        """
        use subprocess pipe to interact with ffmpeg to send video frame
        :param url: video server url
        :param width: video width
        :param height: video height
        :param fps: video fps
        """
        self._fps = fps
        self._command = ['ffmpeg',
                         '-y',
                         '-f', 'rawvideo',
                         '-pix_fmt', 'bgr24',
                         '-s', "{}x{}".format(width, height),
                         '-r', str(self._fps),
                         '-i', '-',
                         '-c:v', 'libx264',
                         '-pix_fmt', 'yuv420p',
                         '-g', '10',
                         '-preset', 'ultrafast',
                         '-tune', 'zerolatency',
                         '-f', 'flv',
                         url]

        self._process = sp.Popen(self._command, bufsize=0, stdin=sp.PIPE)

    def write(self, frame: np.ndarray):
        """
        send out one frame to video stream server
        :param frame: frame to send
        :return:
        """
        self._process.stdin.write(frame.tostring())

    @property
    def fps(self) -> int:
        """
        get fps setting
        :return:
        """
        return self._fps

    def __del__(self):
        """
        close the subprocess pipe
        :return:
        """
        self._process.kill()


@dataclass
class VideoSetting:
    """
    conf for video base settings
    """
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    font = cv2.FONT_HERSHEY_SIMPLEX


class VideoRecorder:
    """
    class to record imaga into a .avi video file
    """

    def __init__(self, source: str, width: int, height: int, fps: int):
        self._writer = cv2.VideoWriter(source,
                                       VideoSetting.fourcc,
                                       fps,
                                       (width, height))

    def write(self, frame: np.ndarray):
        """
        write one image into video
        :param frame:
        :return:
        """
        self._writer.write(frame)

    def __del__(self):
        self._writer.release()


class Annotator:
    """
    class to annotate a specific image
    """

    def __init__(self, style_map: dict):
        self._style_map = style_map

    @property
    def style_map(self) -> dict:
        """
        get the style map data
        :return:
        """
        return self._style_map

    def annotate(self,
                 category: str,
                 frame: np.ndarray,
                 detection: dict,
                 caption: str = None):
        """
        annotate one image with a specific object detection
        :param category:
        :param frame:
        :param detection:
        :param caption:
        :return:
        """
        location = detection['location']
        cv2.rectangle(frame,
                      tuple(location[:2]),
                      tuple(location[2:]),
                      color=self._style_map[category],
                      thickness=2)
        if caption:
            cv2.putText(frame,
                        caption,
                        (location[0], location[1] - 5),
                        VideoSetting.font,
                        0.5,
                        color=self._style_map[category],
                        thickness=2)
