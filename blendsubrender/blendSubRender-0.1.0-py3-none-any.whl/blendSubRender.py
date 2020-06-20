import subprocess
from datetime import datetime
import time
import os


class BlendSubRender:
    def __init__(self, blender_path, blender_file_path, max_frame, start_frame=1, subproccess=2):
        self._blender_path = blender_path
        self._blender_file_path = blender_file_path
        self._max_frame = max_frame
        self._start_frame = start_frame
        self._sub = subproccess
        self._script_path = f"{os.path.dirname(__file__)}/Render.py"

    def sub_render(self):
        """
        Construct a list containing the start and end frames for each subprocess then start use the subprocess module to
        start them
        """
        frame_list = self._construct_frame_list()
        arg_holder = [[self._blender_path, "-b", self._blender_file_path, "-P", self._script_path, f"{start} {end}"]
                      for start, end in frame_list]

        start = f"{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"
        start_clock = time.time()
        print(f"Started {len(arg_holder)} processes of lengths {[end - start for start, end in frame_list]} at {start}")

        sub_p = []
        for args in arg_holder:
            p = subprocess.Popen(args)
            sub_p.append(p)

        for sub in sub_p:
            sub.wait()

        end = f"{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}"
        end_clock = time.time()
        print(f"Finished at {end}! It took {round((end_clock - start_clock) / 60, 2)} minutes to process")

    @staticmethod
    def _chunk_list(list_to_chunk, chunk_length):
        """
        Returns n-sized chunks from list.
        """
        return [list_to_chunk[i:i+max(1, chunk_length)] for i in range(0, len(list_to_chunk), max(1, chunk_length))]

    def _restructure_frames(self, frame_list):
        """
        In some cases we may end up with rounding errors which leads to chunks larger than subproccess, this resets it
        """
        restructured = []
        for index, (start_frame, end_frame) in enumerate(frame_list, 1):
            if index < self._sub:
                restructured.append([start_frame, end_frame])
            elif index == self._sub:
                restructured.append([start_frame, frame_list[len(frame_list) - 1][1]])
                return restructured

    def _construct_frame_list(self):
        """
        Chunk a list into a number of lists each of which represents a frame to be rendered, calculated as the maximum
        frame divided by the number of subproccess. So the more subproccess you assign for a given animation the smaller
        each list will be. Then a list is constructed from the first and last frame of each core's frame list.
        """

        chunks = self._chunk_list(list(range(self._start_frame, self._max_frame + 1)),
                                  int((self._max_frame - self._start_frame) / self._sub))
        frame_list = [[c[0], c[len(c) - 1]] for c in chunks]

        # Fix the frame_list in case of rounding errors
        if len(frame_list) > self._sub:
            frame_list = self._restructure_frames(frame_list)
        return frame_list
