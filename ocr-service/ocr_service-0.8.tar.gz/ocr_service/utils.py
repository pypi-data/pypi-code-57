import cv2
import numpy as np
def imread(img_or_path, flag=1):
    """Read an image using cv2.

    Args:
        img_or_path (ndarray or str): Either a numpy array or image path.
            If it is a numpy array (loaded image), then it will be returned
            as is.
        flag (0 or 1): default 1
            0 is grayscale
            1 is normal

    Returns:
        ndarray: Loaded image array.
    """
    if isinstance(img_or_path, np.ndarray):
        return img_or_path
    else:
        return cv2.imread(img_or_path, flag)