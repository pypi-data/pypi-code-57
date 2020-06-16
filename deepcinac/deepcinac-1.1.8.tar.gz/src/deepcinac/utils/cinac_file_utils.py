import h5py
import numpy as np
import os
import yaml
from ScanImageTiffReader import ScanImageTiffReader
import time
from PIL import ImageSequence
import PIL
import PIL.Image
import tifffile

class CinacFileReader_open_close:
    # temporary version, to see if it would work better
    def __init__(self, file_name, frames_to_keep=None):
        """

        Args:
            file_name: path + filename of the cinac file
            frames_to_keep: tuple of 2 int representing the first_frame and last_frame of a new segment to keep.
            Useful only if all segments have the same number of frames
        """
        self.file_name = file_name
        # just the file
        self.base_name = os.path.basename(self.file_name)
        # removing the extension
        try:
            index_cinac_ext = self.base_name.index(".cinac")
        except ValueError:
            index_cinac_ext = self.base_name.index(".h5")
            # otherwise it will raise an exception
        self.base_name = self.base_name[:index_cinac_ext]

        # opening with a so we can add segment later on if necessary
        self.cinac_file = None # h5py.File(self.file_name, 'r')
        self.is_closed = False
        self.frames_to_keep = frames_to_keep
        self.segments_list = []
        self.n_frames_gt = 0
        self.n_active_frame = 0
        # contains the groups corresponding to each segment contains in the CINAC file
        # each key is a tuple of 3 keys that represent the cell and the first_frame & last_frame
        self.segments_group_dict = dict()
        self.__building_segments_list()


    def _open_file(self):
        self.cinac_file = h5py.File(self.file_name, 'r') # , swmr=True)
        self.is_closed = False

    def close_file(self):
        """
        Close the file
        Returns:

        """
        self.cinac_file.close()
        self.is_closed = True

    def create_new_cinac_file_for_segment_chunk(self, dir_path, segment, first_frame, last_frame):
        # segment data is identified by the cell index, the first and last frame index of the window
        cell = segment[0]
        first_frame_id = segment[1]
        # last_frame is included
        last_frame_id = segment[2]

        new_base_name = "_".join([self.base_name, str(cell), str(first_frame_id), str(last_frame_id),
                                  str(first_frame_id+first_frame), str(first_frame_id+last_frame)]) + ".cinac"
        new_file_name = os.path.join(dir_path, new_base_name)
        # we check first if the file exists, if does we load it, otherwise we create it
        if os.path.exists(new_file_name):
            # print(f"Using cinac file {new_base_name}")
            return CinacFileReader(file_name=new_file_name)

        raster_dur = self.get_segment_raster_dur(segment=segment)[first_frame:last_frame+1]
        doubtful_frames = self.get_segment_doubtful_frames(segment)[first_frame:last_frame+1]
        ci_movie = self.get_segment_ci_movie(segment)[first_frame:last_frame+1]

        smooth_traces = self.get_segment_smooth_traces(segment)[first_frame:last_frame+1]
        raw_traces = self.get_segment_raw_traces(segment)[first_frame:last_frame+1]

        pixels_around = self.get_segment_pixels_around(segment)
        buffer = self.get_segment_pixels_around(segment)

        cells_contour = self.get_segment_cells_contour(segment)
        cells_contour = [np.vstack((coord_data[0], coord_data[1])) for coord_data in cells_contour]

        cell_type = self.get_segment_cell_type(segment)

        invalid_cells = self.get_segment_invalid_cells(segment)

        cinac_writer = CinacFileWriter(file_name=new_file_name)

        group_name = cinac_writer.add_segment_group(cell=cell, first_frame=first_frame_id+first_frame,
                                                    last_frame=first_frame_id+last_frame, raster_dur=raster_dur,
                                                    doubtful_frames=doubtful_frames, ci_movie=ci_movie,
                                                    pixels_around=pixels_around,
                                                    buffer=buffer,
                                                    cells_contour=cells_contour,
                                                    smooth_traces=smooth_traces,
                                                    raw_traces=raw_traces,
                                                    cell_type=cell_type,
                                                    invalid_cells=invalid_cells)

        cinac_writer.close_file()

        return CinacFileReader(file_name=new_file_name)

    def create_cinac_file_for_each_segment(self, dir_path, return_file_readers):
        """
        For each segment in the instance, it created a .cinac file
        that will contain just that sequence.
        Args:
            dir_path: Directory in which save the new .cinac files
            return_file_readers: (bool) if True return a list of instances of
            CinacFileReader from the individual .cinac files created

        Returns:

        """
        cinac_file_readers = []

        segments_list = self.get_all_segments()

        for segment in segments_list:
            # for individual segment cianc file we don't put full data information
            # like path to full movie, all cells coord etc...


            # key is an int representing the cell index, and the value a 1d array representing the raster dur for this
            # cell. Dict is used just to avoid unecessary computation if raster_dur for a cell has already been
            # computed
            raster_dur_dict = dict()

            # segment data is identified by the cell index, the first and last frame index of the window
            cell = segment[0]
            first_frame = segment[1]
            # last_frame is included
            last_frame = segment[2]

            raster_dur = self.get_segment_raster_dur(segment=segment)
            doubtful_frames = self.get_segment_doubtful_frames(segment)
            ci_movie = self.get_segment_ci_movie(segment)
            smooth_traces = self.get_segment_smooth_traces(segment)
            raw_traces = self.get_segment_raw_traces(segment)

            pixels_around = self.get_segment_pixels_around(segment)
            buffer = self.get_segment_pixels_around(segment)

            cells_contour = self.get_segment_cells_contour(segment)
            cells_contour = [np.vstack((coord_data[0], coord_data[1])) for coord_data in cells_contour]

            cell_type = self.get_segment_cell_type(segment)

            invalid_cells = self.get_segment_invalid_cells(segment)

            n_frames = len(raster_dur)

            # in case we want to reduce it more
            chunk_size = 2500
            if n_frames % chunk_size == 0:
            # if False:
                # then we split it in 2500 frames chunck
                for new_first_frame in np.arange(first_frame, last_frame+1, chunk_size):
                    # last_frame is included
                    new_last_frame = new_first_frame + chunk_size - 1

                    new_base_name = "_".join([self.base_name, str(cell), str(new_first_frame), str(new_last_frame)]) + ".cinac"
                    new_file_name = os.path.join(dir_path, new_base_name)
                    # we check first if the file exists, if does we load it, otherwise we create it
                    if os.path.exists(new_file_name):
                        print(f"Using cinac file {new_base_name}")
                        cinac_file_reader = CinacFileReader(file_name=new_file_name)
                        cinac_file_readers.append(cinac_file_reader)
                        continue

                    print(f"Creating individual cinac file {new_base_name}")

                    new_raster_dur = raster_dur[new_first_frame:new_last_frame+1]
                    new_doubtful_frames = doubtful_frames[new_first_frame:new_last_frame+1]
                    # print(f"ci_movie.shape {ci_movie.shape}")
                    new_ci_movie = ci_movie[new_first_frame:new_last_frame+1]
                    new_smooth_traces = smooth_traces[new_first_frame:new_last_frame+1]
                    new_raw_traces = raw_traces[new_first_frame:new_last_frame+1]

                    cinac_writer = CinacFileWriter(file_name=new_file_name)

                    group_name = cinac_writer.add_segment_group(cell=cell, first_frame=new_first_frame,
                                                                last_frame=new_last_frame,
                                                                raster_dur=new_raster_dur,
                                                                doubtful_frames=new_doubtful_frames,
                                                                ci_movie=new_ci_movie,
                                                                pixels_around=pixels_around,
                                                                buffer=buffer,
                                                                cells_contour=cells_contour,
                                                                smooth_traces=new_smooth_traces,
                                                                raw_traces=new_raw_traces,
                                                                cell_type=cell_type,
                                                                invalid_cells=invalid_cells)

                    cinac_writer.close_file()
            else:
                new_base_name = "_".join([self.base_name, str(cell), str(first_frame), str(last_frame)]) + ".cinac"
                new_file_name = os.path.join(dir_path, new_base_name)
                # we check first if the file exists, if does we load it, otherwise we create it
                if os.path.exists(new_file_name):
                    print(f"Using cinac file {new_base_name}")
                    cinac_file_reader = CinacFileReader(file_name=new_file_name)
                    cinac_file_readers.append(cinac_file_reader)
                    continue

                print(f"Creating individual cinac file {new_base_name}")

                cinac_writer = CinacFileWriter(file_name=new_file_name)

                group_name = cinac_writer.add_segment_group(cell=cell, first_frame=first_frame,
                                                            last_frame=last_frame, raster_dur=raster_dur,
                                                            doubtful_frames=doubtful_frames, ci_movie=ci_movie,
                                                            pixels_around=pixels_around,
                                                            buffer=buffer,
                                                            cells_contour=cells_contour,
                                                            smooth_traces=smooth_traces,
                                                            raw_traces=raw_traces,
                                                            cell_type=cell_type,
                                                            invalid_cells=invalid_cells)

                cinac_writer.close_file()

            # then reading it and adding it to cinac_file_readers if return_file_readers is True
            if return_file_readers:
                cinac_file_reader = CinacFileReader(file_name=new_file_name)
                cinac_file_readers.append(cinac_file_reader)

        if return_file_readers:
            return cinac_file_readers

    def __building_segments_list(self):
        def list_arg_sort(seq):
            # http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
            # by unutbu
            return sorted(range(len(seq)), key=seq.__getitem__)
        self._open_file()
        groups_keys_set = set(self.cinac_file.keys())
        # only keeping the groups representing segments
        groups_keys_set.discard("full_data")
        segments_list = list()
        n_frames = 0
        # list used to sort the segments
        list_cell_frames_str = []
        for group_key in groups_keys_set:
            if group_key.count("_") != 3:
                # just in case
                continue
            # group_key format: f"cell_{cell}_{first_frame}_{last_frame}"
            first_index = group_key.index("_")
            second_index = group_key[first_index + 1:].index("_") + first_index + 1
            cell = int(group_key[first_index + 1:second_index])
            third_index = group_key[second_index + 1:].index("_") + second_index + 1
            first_frame = int(group_key[second_index + 1:third_index])
            last_frame = int(group_key[third_index + 1:])
            if self.frames_to_keep is not None:
                if first_frame > self.frames_to_keep[0]:
                    raise Exception(f"first_frame {first_frame} can not be superior to frames_to_keep[0] "
                                    f"{self.frames_to_keep[0]}")
                first_frame = self.frames_to_keep[0]
                if last_frame < self.frames_to_keep[1]:
                    raise Exception(f"last_frame {first_frame} can not be superior to frames_to_keep[1] "
                                    f"{self.frames_to_keep[1]}")
                last_frame = self.frames_to_keep[1]
            segment_tuple = (cell, first_frame, last_frame)
            # adding 0 so we can sort it using alphabetical order, might not be the most efficient solution
            padded_cell = str(cell)
            if len(padded_cell) < 5:
                padded_cell = ("0" * (5 - len(padded_cell))) + padded_cell
            padded_first_frame = str(first_frame)
            if len(padded_first_frame) < 6:
                padded_first_frame = ("0" * (6 - len(padded_cell))) + padded_first_frame
            padded_last_frame = str(last_frame)
            if len(padded_first_frame) < 6:
                padded_last_frame = ("0" * (6 - len(padded_last_frame))) + padded_last_frame
            list_cell_frames_str.append(f"{padded_cell}{padded_first_frame}{padded_last_frame}")
            segments_list.append(segment_tuple)
            n_frames += (last_frame - first_frame + 1)

            group_data = self.cinac_file[group_key]
            if "raster_dur" in group_data:
                if self.frames_to_keep is not None:
                    self.n_active_frame += len(np.where(group_data["raster_dur"][first_frame:last_frame+1])[0])
                else:
                    self.n_active_frame += len(np.where(group_data["raster_dur"])[0])
            self.segments_group_dict[segment_tuple] = group_data

        sorted_indices = list_arg_sort(list_cell_frames_str)
        # sorted segments list
        self.segments_list = [segments_list[i] for i in sorted_indices]
        self.n_frames_gt = n_frames
        self.close_file()

    def _get_segment_group(self, segment):
        """
        Return the group from cinac_file, it should be open
        Args:
            segment:

        Returns:

        """
        if self.is_closed:
            raise Exception("in _get_segment_group() cinac_file should be opened")
        group_key = "cell_" + "_".join(list(map(str, segment)))

        group_data = self.cinac_file[group_key]


        return group_data

    def get_coords_full_movie(self):
        """

        Returns:

        """
        self._open_file()
        if self.with_full_data():
            if "cells_contour" in self.cinac_file['full_data']:
                result = list(self.cinac_file['full_data']["cells_contour"])
                self.close_file()
                return result
            self.close_file()
            return None
        self.close_file()
        return None

    def get_invalid_cells(self):
        """
        Return the invalid cells

        Returns: 1d array of n cells, as many cells. Binary array, 0 is valid, 1 if invalid
        Return None if no

        """
        self._open_file()
        if self.with_full_data():
            if "invalid_cells" in self.cinac_file['full_data']:
                result = np.array(self.cinac_file['full_data']["invalid_cells"])
                self.close_file()
                return result
        self.close_file()
        return None

    def with_full_data(self):
        """
        Return True if full data is available, meaning coords of cells in the original movie, invalid cells
        Returns:

        """
        if self.is_closed:
            self._open_file()
            result = 'full_data' in self.cinac_file
            self.close_file()
            return result
        else:
            return 'full_data' in self.cinac_file

    def get_ci_movie_file_name(self):
        """
        Returns the name of full calcium imaging movie file_name from which the data are extracted.
        None if the file_name is unknown.
        Returns:

        """
        self._open_file()
        if self.with_full_data():
            if "ci_movie_file_name" in self.cinac_file['full_data'].attrs:
                result = self.cinac_file['full_data'].attrs["ci_movie_file_name"]
                self.close_file()
                return result
        self.close_file()
        return None

    def get_all_segments(self):
        """
        Return a list of tuple of 3 int (cell, first_frame, last_frame) representing
        the segments of ground truth available in this file
        Returns: list

        """
        return self.segments_list

    def get_n_frames_gt(self):
        """
        Return the number of frames with ground truth
        Returns:

        """
        return self.n_frames_gt

    def get_n_active_frames(self):
        """
        Return the number of frames with cells being active
        Returns:

        """
        return self.n_active_frame

    def fill_doubtful_frames_from_segments(self, doubtful_frames_nums):
        """
                Fill the doubtful_frames_nums using the ground truth from the segments.
                Args:
                    doubtful_frames_nums: 2d arrays (n_cells x n_frames)

                Returns:

                """
        self._open_file()
        for segment in self.segments_list:
            group_data = self._get_segment_group(segment)
            if "doubtful_frames" in group_data:
                cell, first_frame, last_frame = segment
                doubtful_frames_nums[cell, first_frame:last_frame + 1] = np.array(group_data["doubtful_frames"])
        self.close_file()

    def fill_raster_dur_from_segments(self, raster_dur):
        """
        Fill the raster_dur using the ground truth from the segments.
        Args:
            raster_dur: 2d arrays (n_cells x n_frames)

        Returns:

        """
        self._open_file()
        for segment in self.segments_list:
            group_data = self._get_segment_group(segment)
            if "raster_dur" in group_data:
                cell, first_frame, last_frame = segment
                raster_dur[cell, first_frame:last_frame + 1] = np.array(group_data["raster_dur"])
        self.close_file()

    def get_segment_ci_movie(self, segment):
        """
                Return the calcium imaging from the ground truth segment.
                Args:
                    segment: segment to use to get ci_movie, tuple of 3 to 4 int

                Returns: 3d array

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "ci_movie" in group_data:
                # cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    result = np.array(group_data["ci_movie"])[self.frames_to_keep[0]:self.frames_to_keep[1]+1]
                else:
                    result = np.array(group_data["ci_movie"])
        self.close_file()
        return result

    def get_segment_ci_movie_frames(self, segment, frames):
        """
                Return frames from the calcium imaging from the ground truth segment.
                Args:
                    segment: segment to use to get ci_movie, tuple of 3 to 4 int

                Returns: 3d array

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)

            if "ci_movie" in group_data:
                # cell, first_frame, last_frame = segment
                result = np.array(group_data["ci_movie"][frames])

        self.close_file()
        return result

    def get_segment_cell_type(self, segment):
        """
        Return the name of the cell type from the segment, or None if this information is not known.
        Args:
            segment: segment
        Returns:

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "cell_type" in group_data.attrs:
                result = group_data.attrs["cell_type"]

        self.close_file()
        return result

    def get_segment_pixels_around(self, segment):
        """
        Return the pixels_around used to produce the cell profile on the frame (not really used anymore).
        Args:
            segment: segment
        Returns:

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "pixels_around" in group_data.attrs:
                result = group_data.attrs["pixels_around"]
        self.close_file()
        return result

    def get_segment_buffer(self, segment):
        """
        Return the buffer used to produce the cell profile on the frame (not really used anymore).
        Args:
            segment: segment
        Returns:

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "buffer" in group_data.attrs:
                result = group_data.attrs["buffer"]
        self.close_file()
        return result

    def get_all_cell_types(self):
        """
            Return a dict with as a key the cell index and value a string representing the cell type. Covers all the
            cells represented by the segments.

            Returns:

        """
        self._open_file()
        cell_type_dict = dict()
        for segment in self.segments_list:
            group_data = self._get_segment_group(segment)
            cell, first_frame, last_frame = segment
            if (cell not in cell_type_dict) and ("cell_type" in group_data.attrs):
                cell_type_dict[cell] = group_data.attrs["cell_type"]
        self.close_file()
        return cell_type_dict

    def get_segment_smooth_traces(self, segment):
        """
                Return the smooth fluorescence signal from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: 1d array

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "smooth_traces" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    result = np.array(group_data["smooth_traces"])[first_frame:last_frame + 1]
                else:
                    result = np.array(group_data["smooth_traces"])
        self.close_file()
        return result

    def get_segment_raw_traces(self, segment):
        """
                Return the smooth fluorescence signal from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: 1d array

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "raw_traces" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    result = np.array(group_data["raw_traces"])[first_frame:last_frame + 1]
                else:
                    result = np.array(group_data["raw_traces"])
        self.close_file()
        return result

    def get_segment_cells_contour(self, segment):
        """
                Return the cells contour from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: a list of 2d array that encodes x, y coord (len of the 2d array corresponds to the number
                of point in the contour.

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "cells_contour" in group_data:
                result = list(group_data["cells_contour"])
        self.close_file()
        return result

    def get_segment_raster_dur(self, segment):
        """
        Return the raster_dur from the ground truth segment.
        Args:
            segment: segment to use to get raster_dur

        Returns: 1d array of n frames as specified in segment

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "raster_dur" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    result = np.array(group_data["raster_dur"])[first_frame:last_frame + 1]
                else:
                    result = np.array(group_data["raster_dur"])
        self.close_file()
        return result

    def get_segment_invalid_cells(self, segment):
        """
        Return the invalid cells from the ground truth segment.
        Args:
            segment: segment (tuple of 3 int)

        Returns: 1d array of n cells, as many cells as in the segment (cell of interest + interesections).
        Binary, 0 is valid, 1 if invalid

        """
        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "invalid_cells" in group_data:
                result = np.array(group_data["invalid_cells"])
        self.close_file()
        return result

    def get_segment_doubtful_frames(self, segment):
        """
        Return the doubtful_frames from the ground truth segment.
        Args:
            segment: segment (tuple of 3 int)

        Returns: 1d array of n frames, as many frames as in the segment.
        Binary, 0 is not doubtful, 1 if doubtful

        """

        self._open_file()
        result = None
        if segment in self.segments_group_dict:
            group_data = self._get_segment_group(segment)
            if "doubtful_frames" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    result = np.array(group_data["doubtful_frames"])[first_frame:last_frame + 1]
                else:
                    result = np.array(group_data["doubtful_frames"])
        self.close_file()
        return result


class CinacFileWriter:

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_already_exists = os.path.isfile(self.file_name)
        # opening with a so we can add segment later on if necessary
        self.cinac_file = h5py.File(self.file_name, 'a')
        self.is_closed = False

    def close_file(self):
        """
        Close the file
        Returns:

        """
        self.cinac_file.close()
        self.is_closed = True

    def delete_groups(self, group_names):
        for group_name in group_names:
            del self.cinac_file[group_name]

    def get_group_names(self):
        return list(self.cinac_file.keys())

    def add_segment_group(self, cell, first_frame, last_frame, raster_dur, ci_movie, cells_contour,
                          pixels_around, buffer, invalid_cells, smooth_traces, raw_traces, cell_type=None,
                          doubtful_frames=None):
        """
        Add just a segment (some frames and a given cell)
        Args:
            cell:
            first_frame:
            last_frame:
            raster_dur:
            ci_movie:
            cells_contour:
            pixels_around:
            buffer:
            invalid_cells:
            smooth_traces: normalized (z-scored) smmoth fluorescence signal of the cell during the give frames
            doubtful_frames:
            raw_traces: normalized (z-scored) raw fluorescence signal of the cell during the give frames
            cell_type: any string describing the cell type, in our case it would be "interneuron" or "pyr"
            (for pyramidal cell). If None, means we don't encode this information, the cell type is
            not known ?

        Returns:

        """

        group_name = f"cell_{cell}_{first_frame}_{last_frame}"

        if group_name in self.cinac_file:
            cell_data_grp = self.cinac_file[group_name]
        else:
            cell_data_grp = self.cinac_file.create_group(group_name)

        cell_data_grp.attrs['pixels_around'] = pixels_around
        cell_data_grp.attrs['buffer'] = buffer
        if cell_type is not None:
            cell_data_grp.attrs['cell_type'] = cell_type

        # we decided to save raster_dur in order that if the segment cut a transient
        # we don't have an isolated onset or peak
        # the downside is that when loading, an onset or peak could be added at the beginning
        # or end of the segment.
        # the other solution, could have been to save onsets and peaks but make sure first
        # that segments added have the same number of onsets and peaks
        if "raster_dur" not in cell_data_grp:
            raster_dur_set = cell_data_grp.create_dataset("raster_dur", data=raster_dur)
        else:
            cell_data_grp["raster_dur"][:] = raster_dur

        if "smooth_traces" not in cell_data_grp:
            smooth_traces_set = cell_data_grp.create_dataset("smooth_traces", data=smooth_traces)
        else:
            cell_data_grp["smooth_traces"][:] = smooth_traces

        if "raw_traces" not in cell_data_grp:
            raw_traces_set = cell_data_grp.create_dataset("raw_traces", data=raw_traces)
        else:
            cell_data_grp["raw_traces"][:] = raw_traces

        if doubtful_frames is not None:
            if "doubtful_frames" not in cell_data_grp:
                doubtful_frames_set = cell_data_grp.create_dataset("doubtful_frames",
                                                                   data=doubtful_frames)
            else:
                cell_data_grp["doubtful_frames"][:] = doubtful_frames

        if "ci_movie" not in cell_data_grp:
            ci_movie_set = cell_data_grp.create_dataset("ci_movie",
                                                        data=ci_movie)
        # otherwise the movie is not supposed to change for a given set of frames and a given cell
        # else:
        #     cell_data_grp["ci_movie"][:] = ci_movie

        # cells_contour are not supposed to change during update
        if "cells_contour" not in cell_data_grp:
            dt = h5py.vlen_dtype(np.dtype('int32'))
            cells_contour_set = cell_data_grp.create_dataset(name="cells_contour",
                                                             shape=(len(cells_contour), 2,), dtype=dt)
            # list of np.array, each array can have a different size
            for coord_index, coord in enumerate(cells_contour):
                for i in np.arange(2):
                    cells_contour_set[coord_index, i] = coord[i]

        if invalid_cells is not None:
            if "invalid_cells" in cell_data_grp:
                cell_data_grp["invalid_cells"][:] = invalid_cells
            else:
                invalid_cells_set = cell_data_grp.create_dataset("invalid_cells",
                                                                 data=invalid_cells)

        return group_name

    def create_full_data_group(self, save_only_movie_ref, save_ci_movie_info, cells_contour,
                               n_frames, n_cells,
                               smooth_traces=None, raw_traces=None,
                               ci_movie_file_name=None, ci_movie=None, invalid_cells=None):
        """
        Create a group that represents all data (full movie, all cells etc...)
        Args:
            save_only_movie_ref: boolean, if True means we just save the path & file_name of the calcium imaging movie.
            Otherwise the full movie is saved if ci_movie argument is passed.
            save_ci_movie_info: boolean, if True then either the ci movie ref or the full data is saved in the file
            n_frames: number of frames in the full movie
            n_cells: number of cells segmented (should be the length of cells_contour)
            cells_contour: a list of 2d np.array representing the coordinates of the contour points
            smooth_traces: Smooth fluorescence signals of the cells (z-score)
            raw_traces: Raw fluorescence signals of the cells (z-score)
            ci_movie_file_name:
            ci_movie: np.array should be 3d: n_frames*len_x*len_y, calcium imaging data
            invalid_cells: a binary np.array of the length the number of cells, set to True or 1 is the cell is invalid.

        Returns:

        """
        full_data_grp = self.cinac_file.create_group("full_data")
        if save_ci_movie_info:
            if save_only_movie_ref:
                if ci_movie_file_name is not None:
                    full_data_grp.attrs['ci_movie_file_name'] = ci_movie_file_name
            else:
                if len(ci_movie.shape) == 4:
                    # we remove the last dimension
                    ci_movie = np.reshape(ci_movie, list(ci_movie.shape)[:-1])
                ci_movie_set = full_data_grp.create_dataset("ci_movie",
                                                            data=ci_movie)
        full_data_grp.attrs['n_frames'] = n_frames

        full_data_grp.attrs['n_cells'] = n_cells

        # variable length type
        dt = h5py.vlen_dtype(np.dtype('int16'))
        cells_contour_set = full_data_grp.create_dataset(name="cells_contour", shape=(len(cells_contour), 2,),
                                                         dtype=dt)

        # list of np.array, each array can have a different size
        for coord_index, coord in enumerate(cells_contour):
            for i in np.arange(2):
                cells_contour_set[coord_index, i] = coord[i]

        if invalid_cells is not None:
            invalid_cells_set = full_data_grp.create_dataset("invalid_cells",
                                                             data=invalid_cells)

        if smooth_traces is not None:
            smooth_traces_set = full_data_grp.create_dataset("smooth_traces",
                                                             data=smooth_traces)

        if raw_traces is not None:
            raw_traces_set = full_data_grp.create_dataset("raw_traces",
                                                          data=raw_traces)

    def get_n_cells(self):
        """

        Returns: the number of cells in the movie that have been segmented.
        Return None if this information if not available (need the full_data group to exists)

        """
        if 'full_data' in self.cinac_file:
            if 'cells_contour' in self.cinac_file['full_data']:
                return len(self.cinac_file['full_data']['cells_contour'])

        return None


def read_cell_type_categories_yaml_file(yaml_file, using_multi_class=2):
    """
    Read cell type categories from a yaml file. If more than 2 type cells are given, then a multi-class
    classifier will be used. If 2 type cells are given, then either it could be multi-class or binary classifier,
    then this choice should be given in the parameters of CinacModel.
    If 2 cell-type are given, for binary classifier, it should be precised which cell type should be predicted
    if we get more than 0.5 probability.
    Args:
        yaml_file:
        using_multi_class: int, give the default number of classes used, not necessary if already
        put in the yaml file

    Returns: cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg
    cell_type_from_code_dict: dict, key is an int, value is the cell_type
    cell_type_to_code_dict: dict, key is a string, value is the code of the cell_type. A code can have more than one
    string associated, but all of them represent the same cell_type defined in cell_type_from_code_dict
    multi_class_arg: is None if no multi_class_arg was given in the yaml_file, True or False, if False means we want
    to use a binary classifier

    """

    cell_type_from_code_dict = dict()
    cell_type_to_code_dict = dict()

    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.load(stream, Loader=yaml.FullLoader)

    multi_class_arg = None
    n_cell_categories = 0
    category_code_increment = 0
    # sys.stderr.write(f"{analysis_args_from_yaml}")
    for arg_name, args_content in yaml_data.items():
        if arg_name == "config":
            if isinstance(args_content, dict):
                if "multi_class" in args_content:
                    multi_class_arg = bool(args_content["multi_class"])

        if arg_name == "cell_type_categories":
            n_cell_categories = len(args_content)
            # if multi_class == 1, then we need a predicted_cell_type which will have the value 1
            predicted_cell_type = None
            # args_content is a list of dict, key is the cell_type name, value is a dict
            # with keywords (list of string as value) and predicted_celll_type (bool as value)
            if (multi_class_arg is None and using_multi_class == 1) or (multi_class_arg is False):
                for cell_type_dict in args_content:
                    for cell_type_category, category_dict in cell_type_dict.items():
                        if "predicted_celll_type" in category_dict:
                            predicted_cell_type = cell_type_category
            for cell_type_dict in args_content:
                for cell_type_category, category_dict in cell_type_dict.items():
                    if (predicted_cell_type is not None) and (predicted_cell_type == cell_type_category) and \
                            (n_cell_categories <= 2):
                        cell_type_from_code_dict[1] = cell_type_category
                        cell_type_code = 1
                    else:
                        cell_type_from_code_dict[category_code_increment] = cell_type_category
                        cell_type_code = category_code_increment
                        # print(f"cell_type_category {cell_type_category}: {cell_type_code}")
                        category_code_increment += 1
                        if (category_code_increment == 1) and (predicted_cell_type is not None) and \
                                (n_cell_categories <= 2):
                            category_code_increment += 1
                    cell_type_to_code_dict[cell_type_category] = cell_type_code
                    if "keywords" in category_dict:
                        for keyword in category_dict["keywords"]:
                            cell_type_to_code_dict[keyword] = cell_type_code

    return cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg

class CinacFileReader:

    def __init__(self, file_name, frames_to_keep=None):
        """

        Args:
            file_name: path + filename of the cinac file
            frames_to_keep: tuple of 2 int representing the first_frame and last_frame of a new segment to keep.
            Useful only if all segments have the same number of frames
        """
        self.file_name = file_name
        # just the file
        self.base_name = os.path.basename(self.file_name)
        # removing the extension
        try:
            index_cinac_ext = self.base_name.index(".cinac")
        except ValueError:
            index_cinac_ext = self.base_name.index(".h5")
            # otherwise it will raise an exception
        self.base_name = self.base_name[:index_cinac_ext]

        # opening with a so we can add segment later on if necessary
        self.cinac_file = h5py.File(self.file_name, 'r')
        self.is_closed = False
        self.frames_to_keep = frames_to_keep
        self.segments_list = []
        self.n_frames_gt = 0
        self.n_active_frame = 0
        # contains the groups corresponding to each segment contains in the CINAC file
        # each key is a tuple of 3 keys that represent the cell and the first_frame & last_frame
        self.segments_group_dict = dict()
        self.__building_segments_list()


    def close_file(self):
        """
        Close the file
        Returns:

        """
        self.cinac_file.close()
        self.is_closed = True

    def create_new_cinac_file_for_segment_chunk(self, dir_path, segment, first_frame, last_frame):
        # segment data is identified by the cell index, the first and last frame index of the window
        cell = segment[0]
        first_frame_id = segment[1]
        # last_frame is included
        last_frame_id = segment[2]

        new_base_name = "_".join([self.base_name, str(cell), str(first_frame_id), str(last_frame_id),
                                  str(first_frame_id+first_frame), str(first_frame_id+last_frame)]) + ".cinac"
        new_file_name = os.path.join(dir_path, new_base_name)
        # we check first if the file exists, if does we load it, otherwise we create it
        if os.path.exists(new_file_name):
            # print(f"Using cinac file {new_base_name}")
            return CinacFileReader(file_name=new_file_name)

        raster_dur = self.get_segment_raster_dur(segment=segment)[first_frame:last_frame+1]
        doubtful_frames = self.get_segment_doubtful_frames(segment)[first_frame:last_frame+1]
        ci_movie = self.get_segment_ci_movie(segment)[first_frame:last_frame+1]

        smooth_traces = self.get_segment_smooth_traces(segment)[first_frame:last_frame+1]
        raw_traces = self.get_segment_raw_traces(segment)[first_frame:last_frame+1]

        pixels_around = self.get_segment_pixels_around(segment)
        buffer = self.get_segment_pixels_around(segment)

        cells_contour = self.get_segment_cells_contour(segment)
        cells_contour = [np.vstack((coord_data[0], coord_data[1])) for coord_data in cells_contour]

        cell_type = self.get_segment_cell_type(segment)

        invalid_cells = self.get_segment_invalid_cells(segment)

        cinac_writer = CinacFileWriter(file_name=new_file_name)

        group_name = cinac_writer.add_segment_group(cell=cell, first_frame=first_frame_id+first_frame,
                                                    last_frame=first_frame_id+last_frame, raster_dur=raster_dur,
                                                    doubtful_frames=doubtful_frames, ci_movie=ci_movie,
                                                    pixels_around=pixels_around,
                                                    buffer=buffer,
                                                    cells_contour=cells_contour,
                                                    smooth_traces=smooth_traces,
                                                    raw_traces=raw_traces,
                                                    cell_type=cell_type,
                                                    invalid_cells=invalid_cells)

        cinac_writer.close_file()

        return CinacFileReader(file_name=new_file_name)

    def create_cinac_file_for_each_segment(self, dir_path, return_file_readers):
        """
        For each segment in the instance, it created a .cinac file
        that will contain just that sequence.
        Args:
            dir_path: Directory in which save the new .cinac files
            return_file_readers: (bool) if True return a list of instances of
            CinacFileReader from the individual .cinac files created

        Returns:

        """
        cinac_file_readers = []

        segments_list = self.get_all_segments()

        for segment in segments_list:
            # for individual segment cianc file we don't put full data information
            # like path to full movie, all cells coord etc...


            # key is an int representing the cell index, and the value a 1d array representing the raster dur for this
            # cell. Dict is used just to avoid unecessary computation if raster_dur for a cell has already been
            # computed
            raster_dur_dict = dict()

            # segment data is identified by the cell index, the first and last frame index of the window
            cell = segment[0]
            first_frame = segment[1]
            # last_frame is included
            last_frame = segment[2]

            raster_dur = self.get_segment_raster_dur(segment=segment)
            doubtful_frames = self.get_segment_doubtful_frames(segment)
            ci_movie = self.get_segment_ci_movie(segment)
            smooth_traces = self.get_segment_smooth_traces(segment)
            raw_traces = self.get_segment_raw_traces(segment)

            pixels_around = self.get_segment_pixels_around(segment)
            buffer = self.get_segment_pixels_around(segment)

            cells_contour = self.get_segment_cells_contour(segment)
            cells_contour = [np.vstack((coord_data[0], coord_data[1])) for coord_data in cells_contour]

            cell_type = self.get_segment_cell_type(segment)

            invalid_cells = self.get_segment_invalid_cells(segment)

            n_frames = len(raster_dur)

            # in case we want to reduce it more
            chunk_size = 2500
            if n_frames % chunk_size == 0:
            # if False:
                # then we split it in 2500 frames chunck
                for new_first_frame in np.arange(first_frame, last_frame+1, chunk_size):
                    # last_frame is included
                    new_last_frame = new_first_frame + chunk_size - 1

                    new_base_name = "_".join([self.base_name, str(cell), str(new_first_frame), str(new_last_frame)]) + ".cinac"
                    new_file_name = os.path.join(dir_path, new_base_name)
                    # we check first if the file exists, if does we load it, otherwise we create it
                    if os.path.exists(new_file_name):
                        print(f"Using cinac file {new_base_name}")
                        cinac_file_reader = CinacFileReader(file_name=new_file_name)
                        cinac_file_readers.append(cinac_file_reader)
                        continue

                    print(f"Creating individual cinac file {new_base_name}")

                    new_raster_dur = raster_dur[new_first_frame:new_last_frame+1]
                    new_doubtful_frames = doubtful_frames[new_first_frame:new_last_frame+1]
                    print(f"ci_movie.shape {ci_movie.shape}")
                    new_ci_movie = ci_movie[new_first_frame:new_last_frame+1]
                    new_smooth_traces = smooth_traces[new_first_frame:new_last_frame+1]
                    new_raw_traces = raw_traces[new_first_frame:new_last_frame+1]

                    cinac_writer = CinacFileWriter(file_name=new_file_name)

                    group_name = cinac_writer.add_segment_group(cell=cell, first_frame=new_first_frame,
                                                                last_frame=new_last_frame,
                                                                raster_dur=new_raster_dur,
                                                                doubtful_frames=new_doubtful_frames,
                                                                ci_movie=new_ci_movie,
                                                                pixels_around=pixels_around,
                                                                buffer=buffer,
                                                                cells_contour=cells_contour,
                                                                smooth_traces=new_smooth_traces,
                                                                raw_traces=new_raw_traces,
                                                                cell_type=cell_type,
                                                                invalid_cells=invalid_cells)

                    cinac_writer.close_file()


            else:
                new_base_name = "_".join([self.base_name, str(cell), str(first_frame), str(last_frame)]) + ".cinac"
                new_file_name = os.path.join(dir_path, new_base_name)
                # we check first if the file exists, if does we load it, otherwise we create it
                if os.path.exists(new_file_name):
                    print(f"Using cinac file {new_base_name}")
                    cinac_file_reader = CinacFileReader(file_name=new_file_name)
                    cinac_file_readers.append(cinac_file_reader)
                    continue

                print(f"Creating individual cinac file {new_base_name}")

                cinac_writer = CinacFileWriter(file_name=new_file_name)

                group_name = cinac_writer.add_segment_group(cell=cell, first_frame=first_frame,
                                                            last_frame=last_frame, raster_dur=raster_dur,
                                                            doubtful_frames=doubtful_frames, ci_movie=ci_movie,
                                                            pixels_around=pixels_around,
                                                            buffer=buffer,
                                                            cells_contour=cells_contour,
                                                            smooth_traces=smooth_traces,
                                                            raw_traces=raw_traces,
                                                            cell_type=cell_type,
                                                            invalid_cells=invalid_cells)

                cinac_writer.close_file()

            # then reading it and adding it to cinac_file_readers if return_file_readers is True
            if return_file_readers:
                cinac_file_reader = CinacFileReader(file_name=new_file_name)
                cinac_file_readers.append(cinac_file_reader)

        if return_file_readers:
            return cinac_file_readers

    def __building_segments_list(self):
        def list_arg_sort(seq):
            # http://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python/3382369#3382369
            # by unutbu
            return sorted(range(len(seq)), key=seq.__getitem__)
        groups_keys_set = set(self.cinac_file.keys())
        # only keeping the groups representing segments
        groups_keys_set.discard("full_data")
        segments_list = list()
        n_frames = 0
        # list used to sort the segments
        list_cell_frames_str = []
        for group_key in groups_keys_set:
            if group_key.count("_") != 3:
                # just in case
                continue
            # group_key format: f"cell_{cell}_{first_frame}_{last_frame}"
            first_index = group_key.index("_")
            second_index = group_key[first_index + 1:].index("_") + first_index + 1
            cell = int(group_key[first_index + 1:second_index])
            third_index = group_key[second_index + 1:].index("_") + second_index + 1
            first_frame = int(group_key[second_index + 1:third_index])
            last_frame = int(group_key[third_index + 1:])
            if self.frames_to_keep is not None:
                if first_frame > self.frames_to_keep[0]:
                    raise Exception(f"first_frame {first_frame} can not be superior to frames_to_keep[0] "
                                    f"{self.frames_to_keep[0]}")
                first_frame = self.frames_to_keep[0]
                if last_frame < self.frames_to_keep[1]:
                    raise Exception(f"last_frame {first_frame} can not be superior to frames_to_keep[1] "
                                    f"{self.frames_to_keep[1]}")
                last_frame = self.frames_to_keep[1]
            segment_tuple = (cell, first_frame, last_frame)
            # adding 0 so we can sort it using alphabetical order, might not be the most efficient solution
            padded_cell = str(cell)
            if len(padded_cell) < 5:
                padded_cell = ("0" * (5 - len(padded_cell))) + padded_cell
            padded_first_frame = str(first_frame)
            if len(padded_first_frame) < 6:
                padded_first_frame = ("0" * (6 - len(padded_cell))) + padded_first_frame
            padded_last_frame = str(last_frame)
            if len(padded_first_frame) < 6:
                padded_last_frame = ("0" * (6 - len(padded_last_frame))) + padded_last_frame
            list_cell_frames_str.append(f"{padded_cell}{padded_first_frame}{padded_last_frame}")
            segments_list.append(segment_tuple)
            n_frames += (last_frame - first_frame + 1)

            group_data = self.cinac_file[group_key]
            if "raster_dur" in group_data:
                if self.frames_to_keep is not None:
                    self.n_active_frame += len(np.where(group_data["raster_dur"][first_frame:last_frame+1])[0])
                else:
                    self.n_active_frame += len(np.where(group_data["raster_dur"])[0])
            self.segments_group_dict[segment_tuple] = group_data

        sorted_indices = list_arg_sort(list_cell_frames_str)
        # sorted segments list
        self.segments_list = [segments_list[i] for i in sorted_indices]
        self.n_frames_gt = n_frames

    def get_coords_full_movie(self):
        """

        Returns:

        """

        if self.with_full_data():
            if "cells_contour" in self.cinac_file['full_data']:
                return list(self.cinac_file['full_data']["cells_contour"])
            return None

        return None

    def get_n_cells(self):
        """
        Return the number of cells with contours in this movie (if the information is available, None otherwise)
        Returns:

        """
        coords = self.get_coords_full_movie()
        if coords is not None:
            return len(coords)
        if self.with_full_data():
            if "n_cells" in self.cinac_file['full_data'].attrs:
                return self.cinac_file['full_data'].attrs["n_cells"]
        return None

    def get_n_frames(self):
        """
        Return the number of frames in the full movie
        Returns:

        """
        if self.with_full_data():
            if "n_frames" in self.cinac_file['full_data'].attrs:
                return self.cinac_file['full_data'].attrs["n_frames"]
        return None

    def get_invalid_cells(self):
        """
        Return the invalid cells

        Returns: 1d array of n cells, as many cells. Binary array, 0 is valid, 1 if invalid
        Return None if no

        """

        if self.with_full_data():
            if "invalid_cells" in self.cinac_file['full_data']:
                return np.array(self.cinac_file['full_data']["invalid_cells"])
        return None

    def with_full_data(self):
        """
        Return True if full data is available, meaning coords of cells in the original movie, invalid cells
        Returns:

        """
        return 'full_data' in self.cinac_file

    def get_ci_movie_file_name(self):
        """
        Returns the name of full calcium imaging movie file_name from which the data are extracted.
        None if the file_name is unknown.
        Returns:

        """
        if self.with_full_data():
            if "ci_movie_file_name" in self.cinac_file['full_data'].attrs:
                return self.cinac_file['full_data'].attrs["ci_movie_file_name"]
        return None

    def get_all_segments(self):
        """
        Return a list of tuple of 3 int (cell, first_frame, last_frame) representing
        the segments of ground truth available in this file
        Returns: list

        """
        # TODO: See to sort the list
        return self.segments_list

    def get_n_frames_gt(self):
        """
        Return the number of frames with ground truth
        Returns:

        """
        return self.n_frames_gt

    def get_n_active_frames(self):
        """
        Return the number of frames with cells being active
        Returns:

        """
        return self.n_active_frame

    def fill_doubtful_frames_from_segments(self, doubtful_frames_nums):
        """
                Fill the doubtful_frames_nums using the ground truth from the segments.
                Args:
                    doubtful_frames_nums: 2d arrays (n_cells x n_frames)

                Returns:

                """

        for segment in self.segments_list:
            group_data = self.segments_group_dict[segment]
            if "doubtful_frames" in group_data:
                cell, first_frame, last_frame = segment
                doubtful_frames_nums[cell, first_frame:last_frame + 1] = np.array(group_data["doubtful_frames"])

    def fill_raster_dur_from_segments(self, raster_dur):
        """
        Fill the raster_dur using the ground truth from the segments.
        Args:
            raster_dur: 2d arrays (n_cells x n_frames)

        Returns:

        """

        for segment in self.segments_list:
            group_data = self.segments_group_dict[segment]
            if "raster_dur" in group_data:
                cell, first_frame, last_frame = segment
                raster_dur[cell, first_frame:last_frame + 1] = np.array(group_data["raster_dur"])

    def get_segment_ci_movie(self, segment):
        """
                Return the calcium imaging from the ground truth segment.
                Args:
                    segment: segment to use to get ci_movie, tuple of 3 to 4 int

                Returns: 3d array

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "ci_movie" in group_data:
                # cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    return np.array(group_data["ci_movie"])[self.frames_to_keep[0]:self.frames_to_keep[1]+1]
                else:
                    return np.array(group_data["ci_movie"])

    def get_segment_ci_movie_frames(self, segment, frames):
        """
                Return frames from the calcium imaging from the ground truth segment.
                Args:
                    segment: segment to use to get ci_movie, tuple of 3 to 4 int

                Returns: 3d array

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]

            if "ci_movie" in group_data:
                # cell, first_frame, last_frame = segment
                return np.array(group_data["ci_movie"][frames])

    def get_segment_cell_type(self, segment):
        """
        Return the name of the cell type from the segment, or None if this information is not known.
        Args:
            segment: segment
        Returns:

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "cell_type" in group_data.attrs:
                return group_data.attrs["cell_type"]
        return None

    def get_segment_pixels_around(self, segment):
        """
        Return the pixels_around used to produce the cell profile on the frame (not really used anymore).
        Args:
            segment: segment
        Returns:

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "pixels_around" in group_data.attrs:
                return group_data.attrs["pixels_around"]
        return None

    def get_segment_buffer(self, segment):
        """
        Return the buffer used to produce the cell profile on the frame (not really used anymore).
        Args:
            segment: segment
        Returns:

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "buffer" in group_data.attrs:
                return group_data.attrs["buffer"]
        return None

    def get_all_cell_types(self):
        """
            Return a dict with as a key the cell index and value a string representing the cell type. Covers all the
            cells represented by the segments.

            Returns:

        """
        cell_type_dict = dict()
        for segment in self.segments_list:
            group_data = self.segments_group_dict[segment]
            cell, first_frame, last_frame = segment
            if (cell not in cell_type_dict) and ("cell_type" in group_data.attrs):
                cell_type_dict[cell] = group_data.attrs["cell_type"]
        return cell_type_dict

    def get_segment_smooth_traces(self, segment):
        """
                Return the smooth fluorescence signal from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: 1d array

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "smooth_traces" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    return np.array(group_data["smooth_traces"])[first_frame:last_frame + 1]
                else:
                    return np.array(group_data["smooth_traces"])

    def get_segment_raw_traces(self, segment):
        """
                Return the smooth fluorescence signal from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: 1d array

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "raw_traces" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    return np.array(group_data["raw_traces"])[first_frame:last_frame + 1]
                else:
                    return np.array(group_data["raw_traces"])

    def get_segment_cells_contour(self, segment):
        """
                Return the cells contour from the ground truth segment.
                Args:
                    segment: segment to use to fill raster_dur, tuple of 3 to 4 int

                Returns: a list of 2d array that encodes x, y coord (len of the 2d array corresponds to the number
                of point in the contour.

        """
        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "cells_contour" in group_data:
                return list(group_data["cells_contour"])

    def get_segment_raster_dur(self, segment):
        """
        Return the raster_dur from the ground truth segment.
        Args:
            segment: segment to use to get raster_dur

        Returns: 1d array of n frames as specified in segment

        """

        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "raster_dur" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    return np.array(group_data["raster_dur"])[first_frame:last_frame + 1]
                else:
                    return np.array(group_data["raster_dur"])

    def get_segment_invalid_cells(self, segment):
        """
        Return the invalid cells from the ground truth segment.
        Args:
            segment: segment (tuple of 3 int)

        Returns: 1d array of n cells, as many cells as in the segment (cell of interest + interesections).
        Binary, 0 is valid, 1 if invalid

        """

        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "invalid_cells" in group_data:
                return np.array(group_data["invalid_cells"])
        return None

    def get_segment_doubtful_frames(self, segment):
        """
        Return the doubtful_frames from the ground truth segment.
        Args:
            segment: segment (tuple of 3 int)

        Returns: 1d array of n frames, as many frames as in the segment.
        Binary, 0 is not doubtful, 1 if doubtful

        """

        if segment in self.segments_group_dict:
            group_data = self.segments_group_dict[segment]
            if "doubtful_frames" in group_data:
                cell, first_frame, last_frame = segment
                if self.frames_to_keep is not None:
                    return np.array(group_data["doubtful_frames"])[first_frame:last_frame + 1]
                else:
                    return np.array(group_data["doubtful_frames"])
        return None


def create_tiffs_from_movie(path_for_tiffs, movie_identifier, movie_file_name=None, movie_data=None):
    """
    Take a Tiff movie or 3d array representing it, and save an unique tiff file for each of its frame.
    Save as well the mean and std as npy file, all in the directory path_for_tiffs, in a directory with the
    identifier
    Args:
        path_for_tiffs: str
        movie_identifier: str
        movie_file_name: str
        movie_data: 3d array

    Returns: boolean, return False if the directory with this identifier already exists, True if Tiffs have been
    created

    """

    if movie_data is None and movie_file_name is None:
       raise Exception("Movie_data or movie_file_name should not be None")

    dir_names = []
    # look for filenames in the fisrst directory, if we don't break, it will go through all directories
    for (dirpath, dirnames, local_filenames) in os.walk(path_for_tiffs):
        dir_names.extend([x.lower() for x in dirnames])
        break

    dir_found = False
    for dir_name in dir_names:
        if (movie_identifier.lower() in dir_name.lower()) or (dir_name.lower() in movie_identifier.lower()):
            dir_found = True
            break
    if dir_found:
        return False

    print(f"create_tiffs_from_movie for {movie_identifier}")

    if movie_data is None:
        try:
            start_time = time.time()
            movie_data = ScanImageTiffReader(movie_file_name).data()
            n_frames = len(movie_data)
            stop_time = time.time()
            print(f"Time for loading movie with scan_image_tiff: "
                  f"{np.round(stop_time - start_time, 3)} s")
        except Exception as e:
            start_time = time.time()
            im = PIL.Image.open(movie_file_name)
            n_frames = len(list(ImageSequence.Iterator(im)))
            dim_x, dim_y = np.array(im).shape
            print(f"n_frames {n_frames}, dim_x {dim_x}, dim_y {dim_y}")
            movie_data = np.zeros((n_frames, dim_x, dim_y), dtype="uint16")
            for frame, page in enumerate(ImageSequence.Iterator(im)):
                movie_data[frame] = np.array(page)
            stop_time = time.time()
            print(f"Time for loading movie: "
                  f"{np.round(stop_time - start_time, 3)} s")
    else:
        n_frames = len(movie_data)

    ms_path = os.path.join(path_for_tiffs, movie_identifier)
    os.mkdir(ms_path)

    # we can either save the file in 64 bits normalized
    # or save it in 16 bits and then normalizing it using the mean and std values saved
    # # normalizing movie
    # tiff_movie = (tiff_movie - np.mean(tiff_movie)) / np.std(tiff_movie)

    mean_value = np.mean(movie_data)
    std_value = np.std(movie_data)

    np.save(os.path.join(ms_path, "mean.npy"), mean_value)
    np.save(os.path.join(ms_path, "std.npy"), std_value)

    start_time = time.time()
    # then saving each frame as a unique tiff
    for frame in np.arange(n_frames):
        tiff_file_name = os.path.join(ms_path, f"{frame}.tiff")
        with tifffile.TiffWriter(tiff_file_name) as tiff:
            tiff.save(movie_data[frame], compress=0)
    stop_time = time.time()
    print(f"Time for writing the tiffs: "
          f"{np.round(stop_time - start_time, 3)} s")
