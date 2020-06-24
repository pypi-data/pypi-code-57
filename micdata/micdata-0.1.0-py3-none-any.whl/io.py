import os
from abc import ABCMeta, abstractmethod, abstractproperty
import numpy as np
import tifffile


class IOFactory():
    def __init__(self, path, dtype=np.float32):
        self.path = path
        (self.ext, self.no_ext, self.dir_name, self.file_name) = self.split_path()

    def load(self, path=None):
        path = path or self.path
        ext, _, _, _ = self.split_path(path)
        loader = self.get_loader(ext=ext)
        return loader.load(path)

    def write(self, data, path=None, ext=None):
        if ext is not None:
            path = self.no_ext + ext
        elif path is None:
            path = self.path
        writer = self.get_writer(path)
        writer.write(path, data)

    def get_writer(self, path=None):
        return TiffWriter(compress=9)

    def get_loader(self, ext=None):
        ext = ext or self.ext
        if ext == '.tif' or ext == '.tiff':
            return TiffLoader()
        elif ext == '.nd2' or ext == '.stk':
            return BioFormatsLoader()
        else:
            raise NotImplementedError('Cannot load files with extension "{}"'.format(self.ext))

    def split_path(self, path=None):
        path = path or self.path
        (dir_name, file_name) = os.path.split(path)
        (no_ext, ext) = os.path.splitext(path)
        return (ext, no_ext, dir_name, file_name)


class ImageWriter(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self.kwargs = kwargs  # used to configure the writer library

    @abstractmethod
    def write(self, path, data):
        '''Save data to disk, ideally using the appropriate library.

        Arguments:
        path: path where the file should be saved
        data: data to be saved
        '''


class TiffWriter(ImageWriter):

    def write(self, path, data):
        (no_ext, _) = os.path.splitext(path)
        tifffile.imsave(no_ext + '.tif', data, **self.kwargs)


class ImageLoader(metaclass=ABCMeta):
    """Abstract base class for image loader methods."""

    def __init__(self, dtype=np.float32):
        self.dtype = dtype

    @abstractmethod
    def load(self, path):
        '''Load the file from disk, ideally using the appropriate library.

        Arguments:
        path: path to the image file

        Returns:
        numpy array with shape: (time, x, y, color_channel)
        '''

    def _check_dimensions(self, stack):
        stack = stack.astype(self.dtype)
        assert len(
            stack.shape) > 1, "The image should have at least two dimensions"
        if len(stack.shape) < 3:
            # add the time axis if necessary
            stack = stack[np.newaxis]
        if len(stack.shape) < 4:
            # add the color dimension if necessary
            stack = stack[..., np.newaxis]
        if len(stack.shape) > 4:
            raise ValueError(
                'The stack has too many dimensions. I can handle at most 4 dimensions: (time, x, y, color_channel)')
        return stack


class TiffLoader(ImageLoader):
    '''Loader for tiff files using tifffile'''

    def load(self, path):
        '''Implements ImageLoader.load()'''
        stack = tifffile.imread(path)
        return self._check_dimensions(stack)


class BioFormatsLoader(ImageLoader):
    '''Loader for files supported by the bioformats java library'''

    def load(self, path):
        '''Implements ImageLoader.load()'''
        import javabridge
        import bioformats
        javabridge.start_vm(class_path=bioformats.JARS)
        with bioformats.ImageReader(path) as reader:
            stack = reader.read(rescale=False)
            stack = stack[np.newaxis]
            t = 1
            while True:
                try:
                    plane = reader.read(t=t, rescale=False)
                    plane = plane[np.newaxis]
                    stack = np.vstack((stack, plane))
                    t += 1
                except javabridge.JavaException:
                    break
        return self._check_dimensions(stack)
