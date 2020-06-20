"""
FractalCam
"""
import cv2
import inspect
import numpy as np
from scipy import ndimage
# Local imports
from . import fractals

__version__ = '0.1.1'

def getmapper(mappername):
    """
    Function to get the fractal mapper given a name. Raises ValueError if name
    not in factals.
    """

    options = []

    for element_name in dir(fractals):
        if element_name.startswith('_'):
            continue
        element = getattr(fractals, element_name)
        if inspect.isfunction(element):
            options.append(element_name)
            if mappername == element_name:
                return element

    raise ValueError(f'Fractal "{mappername}" not found. Use one of {options}')

class Camera(object):
    """
    Create a camera object

    Parameters
    ----------
    mappername : str
        Name of mapping function to use.
    device : int
        Webcam device number for OpenCV to use.
    """

    def __init__(self, mappername, device):
        self.mapping_func = getmapper(mappername)
        self.devicenum = device
        self.vc = None
        self.rval = False
        self.frame = None
        self.rows = None
        self.cols = None

    def __enter__(self):
        cv2.namedWindow('FractalCam', cv2.WND_PROP_FULLSCREEN)          
        cv2.setWindowProperty(
            'FractalCam',
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )
        self.vc = cv2.VideoCapture(self.devicenum)

        # Read one frame to setup the mapper. Only need to apply the mapper
        # once and store the results for row/col lookup.
        if self.vc.isOpened():
            self.rval, self.frame = self.vc.read()
        else:
            raise ValueError(
                f'Problem using device {self.devicenum}, try a different value.'
            )
        self.rows, self.cols = self.mapping_func(
            self.frame.shape[0],
            self.frame.shape[1]
        )

        return self

    def __exit__(self, *args):
        self.vc.release()
        cv2.destroyWindow("FractalCam")

    def iterate(self):
        """
        Method to get webcam frame and apply mapping
        """

        if self.vc.isOpened():
            self.rval, self.frame = self.vc.read()
        else:
            self.rval = False
        
        img = np.zeros(self.frame.shape, dtype=np.uint8)
        for i in range(3):
            img[:,:,i] = ndimage.map_coordinates(
                self.frame[:,:,i],
                [self.rows,self.cols], 
                order=2
            )
        cv2.imshow("FractalCam", img)

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            self.rval = False