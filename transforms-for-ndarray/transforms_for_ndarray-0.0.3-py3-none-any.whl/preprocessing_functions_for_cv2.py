# coding=gbk
"""
author(作者): Channing Xie(谢琛)
time(时间): 2020/6/18 10:04
filename(文件名): preprocessing_functions_for_cv2.py
function description(功能描述):
...
"""
# coding=gbk
import collections
Iterable = collections.abc.Iterable
import numbers
import torch
import numpy as np
import cv2
import sys
from PIL import Image
import PIL
# import warnings
print("Opencv.version: ", cv2.__version__)
print("PIL.version: ", PIL.__version__)

if sys.version_info < (3, 3):
    Sequence = collections.Sequence
    Iterable = collections.Iterable
else:
    Sequence = collections.abc.Sequence
    Iterable = collections.abc.Iterable


def _is_tensor_image(img):
    return torch.is_tensor(img) and img.ndimension() == 3


def _is_pil_image(pic):
    return isinstance(pic, Image.Image)


def _is_numpy(pic):
    return isinstance(pic, np.ndarray)


def _is_numpy_image(pic: np.ndarray):
    return isinstance(pic, np.ndarray) and (pic.ndim in {2, 3})


def to_tensor(pic, mode):
    """Convert a ``PIL Image`` or ``numpy.ndarray`` to tensor.

    See ``ToTensor`` for more details.

    Args:
        pic (PIL Image or numpy.ndarray): Image to be converted to tensor.
        mode

    Returns:
        Tensor: Converted image.
    """
    if not(_is_pil_image(pic) or _is_numpy(pic)):
        raise TypeError('pic should be PIL Image or ndarray. Got {}'.format(type(pic)))

    if _is_numpy(pic) and not _is_numpy_image(pic):
        raise ValueError('pic should be 2/3 dimensional. Got {} dimensions.'.format(pic.ndim))

    if isinstance(pic, np.ndarray):
        # handle numpy array
        if pic.ndim == 2:
            pic = pic[:, :, None]
        img = pic
        if mode == 1:
            img = torch.from_numpy(pic.transpose((2, 0, 1)))
        # backward compatibility
        if isinstance(img, torch.ByteTensor):
            return img.float()/255.
        else:
            return img

    # handle PIL Image
    if pic.mode == 'I':
        img = torch.from_numpy(np.array(pic, np.int32, copy=False))
    elif pic.mode == 'I;16':
        img = torch.from_numpy(np.array(pic, np.int16, copy=False))
    elif pic.mode == 'F':
        img = torch.from_numpy(np.array(pic, np.float32, copy=False))
    elif pic.mode == '1':
        img = 255 * torch.from_numpy(np.array(pic, np.uint8, copy=False))
    else:
        # pass
        img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))
    # PIL image mode: L, LA, P, I, F, RGB, YCbCr, RGBA, CMYK
    if pic.mode == 'YCbCr':
        nchannel = 3
    elif pic.mode == 'I;16':
        nchannel = 1
    else:
        nchannel = len(pic.mode)
    img = img.view(pic.size[1], pic.size[0], nchannel)
    # put it from HWC to CHW format
    # yikes, this transpose takes 80% of the loading time/CPU
    img = img.transpose(0, 1).transpose(0, 2).contiguous()
    if isinstance(img, torch.ByteTensor):
        return img.float()/255
    else:
        return img


def cut(image: np.ndarray):
    if isinstance(image, np.ndarray):
        if str(image.dtype) == 'uint8':
            image[np.where(image > 255)] = 255
            image[np.where(image < 0)] = 0
        elif str(image.dtype) == 'float64':
            image[np.where(image > 1.)] = 1.
            image[np.where(image < 0.)] = 0.
    return image


def normalize(tensor, mean, std, inplace=False):
    """Normalize a tensor image with mean and standard deviation.

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    See :class:`~torchvision.transforms.Normalize` for more details.

    Args:
        tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool,optional): Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """
    if not _is_tensor_image(tensor):
        raise TypeError('tensor is not a torch image.')

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    tensor.sub_(mean[:, None, None]).div_(std[:, None, None])
    return tensor


def resize(image, new_size, interpolation=cv2.INTER_LINEAR):
    """
        Resize the input PIL Image to the given size.

        Args:
            image (PIL Image): Image to be resized.
            new_size (sequence or int): Desired output size. If size is a sequence like
                (h, w), the output size will be matched to this. If size is an int,
                the smaller edge of the image will be matched to this number maintaining
                the aspect ratio. i.e, if height > width, then image will be rescaled to
            interpolation (int, optional): Desired interpolation. Default is
                "cv2.INTER_LINEAR"

        Returns:
            numpy image: Resized image.
    """
    if not _is_numpy_image(image):
        # print(image)
        raise TypeError('img should be numpy.ndarray. Got {}'.format(type(image)))
    if not (isinstance(new_size, int) or (isinstance(new_size, Iterable) and len(new_size) == 2)):
        raise TypeError('Got inappropriate size arg: {}'.format(new_size))

    if isinstance(new_size, int):
        h, w = image.shape[:2]
        if (w <= h and w == new_size) or (h <= w and h == new_size):
            return image
        if w < h:
            ow = new_size
            oh = int(new_size * h / w)
            return cv2.resize(image, (oh, ow), interpolation=interpolation)
            # return img.resize((ow, oh), interpolation)
        else:
            oh = new_size
            ow = int(new_size * w / h)
            return cv2.resize(image, (oh, ow), interpolation=interpolation)
            # return image.resize((ow, oh), interpolation)
    else:
        return cv2.resize(image, new_size, interpolation=interpolation)
        # return image.resize(new_size, interpolation)


def crop(image, i, j, h, w):
    """Crop the given numpy Image.

    Args:
        image (numpy Image): Image to be cropped.
        i (int): i in (i,j) i.e coordinates of the upper left corner.
        j (int): j in (i,j) i.e coordinates of the upper left corner.
        h (int): Height of the cropped image.
        w (int): Width of the cropped image.

    Returns:
        PIL Image: Cropped image.
    """
    if not _is_numpy_image(image):
        raise TypeError('img should be numpy.ndarray. Got {}'.format(type(image)))

    return image[i:i + h, j:j + w]


def center_crop(img, output_size):
    if isinstance(output_size, numbers.Number):
        output_size = (int(output_size), int(output_size))
    h, w = img.shape[:2]
    th, tw = output_size
    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))
    return crop(img, i, j, th, tw)


# TODO
def pad(image, padding, fill, padding_mode):
    """Pad the given PIL Image on all sides with specified padding mode and fill value.

       Args:
           image (numpy.ndarray): Image to be padded.
           padding (int or tuple): Padding on each border. If a single int is provided this
               is used to pad all borders. If tuple of length 2 is provided this is the padding
               on left/right and top/bottom respectively. If a tuple of length 4 is provided
               this is the padding for the left, top, right and bottom borders
               respectively.
           fill: Pixel fill value for constant fill. Default is 0. If a tuple of
               length 3, it is used to fill R, G, B channels respectively.
               This value is only used when the padding_mode is constant
           padding_mode: Type of padding. Should be: constant, edge, reflect or symmetric. Default is constant.

               - constant: pads with a constant value, this value is specified with fill

               - edge: pads with the last value on the edge of the image

               - reflect: pads with reflection of image (without repeating the last value on the edge)

                          padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode
                          will result in [3, 2, 1, 2, 3, 4, 3, 2]

               - symmetric: pads with reflection of image (repeating the last value on the edge)

                            padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode
                            will result in [2, 1, 1, 2, 3, 4, 4, 3]

       Returns:
           PIL Image: Padded image.
    """
    if not _is_numpy_image(image):
        raise TypeError('img should be numpy.ndarray. Got {}'.format(type(image)))

    if not isinstance(padding, (numbers.Number, tuple)):
        raise TypeError('Got inappropriate padding arg, it should be an integer or a tuple')
    if not isinstance(fill, (numbers.Number, str, tuple)):
        raise TypeError('Got inappropriate fill arg, it should be an integer, string or tuple')
    if not isinstance(padding_mode, str):
        raise TypeError('Got inappropriate padding_mode arg, it should be a string')

    if isinstance(padding, Sequence) and len(padding) not in [2, 4]:
        raise ValueError("Padding must be an int or a 2, or 4 element tuple, not a " +
                         "{} element tuple".format(len(padding)))

    assert padding_mode in ['constant', 'edge', 'reflect', 'symmetric'], \
        'Padding mode should be either constant, edge, reflect or symmetric'

    if padding_mode == 'constant':
        if image.mode == 'P':
            palette = image.getpalette()
            image = ImageOps.expand(image, border=padding, fill=fill)
            image.putpalette(palette)
            return image

        return ImageOps.expand(image, border=padding, fill=fill)
    else:
        if isinstance(padding, int):
            pad_left = pad_right = pad_top = pad_bottom = padding
        if isinstance(padding, Sequence) and len(padding) == 2:
            pad_left = pad_right = padding[0]
            pad_top = pad_bottom = padding[1]
        if isinstance(padding, Sequence) and len(padding) == 4:
            pad_left = padding[0]
            pad_top = padding[1]
            pad_right = padding[2]
            pad_bottom = padding[3]

        if image.mode == 'P':
            palette = image.getpalette()
            img = np.asarray(image)
            img = np.pad(img, ((pad_top, pad_bottom), (pad_left, pad_right)), padding_mode)
            img = Image.fromarray(img)
            img.putpalette(palette)
            return img

        img = np.asarray(image)
        # RGB image
        if len(img.shape) == 3:
            img = np.pad(img, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), padding_mode)
        # Grayscale image
        if len(img.shape) == 2:
            img = np.pad(img, ((pad_top, pad_bottom), (pad_left, pad_right)), padding_mode)

        return Image.fromarray(img)


def hflip(image: np.ndarray):
    """
    Flip the numpy Image horizontally.
    :param image: Image to be flipped.
    :return: Flipped Image
    """
    dim = len(image.shape)
    if dim == 2:
        return image[::-1, :]
    else:
        return image[::-1, :, :]


def vflip(image: np.ndarray):
    """
    Flip the numpy Image vertically.
    :param image: Image to be flipped.
    :return: Flipped Image
    """
    dim = len(image.shape)
    if dim == 2:
        return image[:, ::-1]
    else:
        return image[:, ::-1, :]


# TODO
def perspective(image, startPoints, endPoints, interpolation):
    """
    反射变换？？？
    :param image:
    :param startPoints:
    :param endPoints:
    :param interpolation:
    :return:
    """
    pass


def resized_crop(img, i, j, h, w, size, interpolation=Image.BILINEAR):
    """Crop the given numpy Image and resize it to desired size.

    Notably used in :class:`~torchvision.transforms.RandomResizedCrop`.

    Args:
        img (numpy Image): Image to be cropped.
        i (int): i in (i,j) i.e coordinates of the upper left corner
        j (int): j in (i,j) i.e coordinates of the upper left corner
        h (int): Height of the cropped image.
        w (int): Width of the cropped image.
        size (sequence or int): Desired output size. Same semantics as ``resize``.
        interpolation (int, optional): Desired interpolation. Default is
            ``cv2.INTER_LINEAR``.
    Returns:
        numpy Image: Cropped image.
    """
    assert _is_numpy_image(img), 'img should be numpy Image'
    img = crop(img, i, j, h, w)
    img = resize(img, size, interpolation)
    return img


def five_crop(image, size):
    """
    Crop the given numpy Image into four corners and the central crop.
    Note::
        This transform returns a tuple of images and there may be a mismatch in the number
        of inputs and targets your "Dataset" returns.
    :param image: (numpy image) Image to be five_cropped.
    :param size: (sequence or int) Desired output size of the crop. If size is an int instead of
                    sequence like (h, w), a square crop (size, size) is made.
    :return: (tuple) (tl, tr, bl, br, center), corresponding top left, top right, bottom left, bottom
                    right and center crop.
    """
    if isinstance(size, numbers.Number):
        size = (int(size), int(size))
    else:
        assert len(size) == 2, "Please provide only 2 dimensions (h, w) for size."

    h, w = image.shape[:2]
    crop_h, crop_w = size
    if crop_w > w or crop_h > h:
        raise ValueError("Requested crop size {} is bigger than input size {}".format(size, (h, w)))
    tl = crop(image, 0, 0, crop_h, crop_w)
    tr = crop(image, 0, w - crop_w, crop_h, crop_w)
    bl = crop(image, h - crop_h, 0, crop_h, crop_w)
    br = crop(image, h - crop_h, w - crop_w, crop_h, crop_w)
    center = center_crop(image, (crop_h, crop_w))
    return tl, tr, bl, br, center


def ten_crop(img, size, vertical_flip=False):
    """
    Crop the given numpy image into four corners and the central crop together with their
    flipped version (horizontal flipping is used by default).
    :param img: (numpy image) image to be ten_cropped.
    :param size: (sequence or int) Desired output size of the crop. If size is an int instead of
                 sequence like (h, w), a square crop (size, size) is made.
    :param vertical_flip: (bool) whether use vertical flipping instead of horizontal or not.
    :return: (tuple) tl, tr, bl, br, center, tl_flip, tr_flip, bl_flip, br_flip, center_flip images.
    """
    if isinstance(size, numbers.Number):
        size = (int(size), int(size))
    else:
        assert len(size) == 2, "Please provide only 2 dimensions (h, w) for size."

    first_five = five_crop(img, size)

    if vertical_flip:
        img = vflip(img)
    else:
        img = hflip(img)
    second_five = five_crop(img, size)
    return first_five + second_five


# subFunction for ColorJitter
# TODO
def adjust_brightness(img, brightness_factor):
    """
    Adjust brightness of a numpy Image.
    :param img: (numpy Image) Image to be adjusted.
    :param brightness_factor: (float) How much to adjust the brightness. Can be any non-negative number.
            0 gives a black image, 1 gives the original image while 2 increases the brightness by a
            factor of 2.
    :return: Brightness adjusted image.
    """
    if not _is_numpy_image(img):
        raise TypeError("Image should be numpy Image. Got {}".format(type(img)))
    return None


# TODO
def adjust_contrast(img, contrast_factor):
    return None


# TODO
def adjust_saturation(img, saturation_factor):
    return None


# TODO
def adjust_hue(img, hue_factor):
    return None


def rotate(img, angle, resample=False, expand=1., center=None):
    """
    Rotate the image by angle.
    :param img: (numpy image) image to be rotated.
    :param angle: (float or int) In degrees degrees counter clockwise order.
    :param resample: (optional) "cv2.INTER_LINEAR", "cv2.INTER_NEAREST", "cv2.INTER_CUBIC"
    :param expand: (None or tuple) If true, expands the output image to make it large enough to hold the entire
                    rotated image. If false or omitted, make the output image the same size as the input
                    image. Note that the expand flag assumes rotation around the center and no translation.
    :param center: (2-tuple) Center of rotation. Default is the center of the image. Origin is the upper left.
    :return: Rotated image.
    """
    if not _is_numpy_image(img):
        raise TypeError("Image should be numpy Image. Got {}".format(type(img)))
    h, w = img.shape[:2]
    if not isinstance(angle, numbers.Number):
        raise TypeError("Angle should be a number. Got {}".format(type(angle)))
    if (resample is None) or (resample == 1):
        resample = cv2.INTER_LINEAR
    elif resample == 0:
        resample = cv2.INTER_NEAREST
    elif resample == 2:
        resample = cv2.INTER_CUBIC
    # to be continued ...

    if expand is None:
        expand = (h, w)
    elif not isinstance(expand, numbers.Number):
        raise ValueError("The type of 'expand' should be float, the type of input 'expand' is {}".format(type(expand)))
    elif expand <= 0:
        raise ValueError("'expand' should be a positive number.")
    else:
        expand = (int(h * expand), int(w * expand))
    if center is None:
        center = (int(expand[1] / 2.), int(expand[0] / 2.))
    else:
        assert len(center) == 2, "Please provide only 2 dimensions (h, w) for size."

    image = None
    if len(img.shape) == 3:
        image = np.zeros((expand[0], expand[1], 3)).astype(np.uint8)
        y, x = (expand[0] - h) // 2, (expand[1] - w) // 2
        image[y:y+h, x:x+w, :] = img
        matrix = cv2.getRotationMatrix2D(center, angle, 1.)
        image = cv2.warpAffine(image, matrix, (expand[1], expand[0]), flags=resample)
    elif len(img.shape) == 2:
        image = np.zeros(expand)
        y, x = ((expand[0] - h) / 2.), int((expand[1] - w) / 2.)
        image[y:y + h, x:x + w] = img
        matrix = cv2.getRotationMatrix2D(center, angle, 1.)
        image = cv2.warpAffine(image, matrix, (expand[1], expand[0]), flags=resample)
        # cv2.circle(image, center, 5, (255, 0, 0))
    return image


# TODO
def affine(img, param, resample, fillcolor):
    return None


def to_grayscale(img, num_output_channels=1):
    """
    Convert image to grayscale version of image.
    :param img: (numpy image) Image to be converted to grayscale.
    :param num_output_channels: The number of the output image channel.
            If num_output_channels = 1, the output image has only one channel.
            If num_output_channels = 3, the output image has 3 channels with r = b = g.
    :return: Gray_scaled image.
    """
    if not _is_numpy_image(img):
        raise TypeError("Image should be numpy image. Got {}.".format(type(img)))
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if num_output_channels == 1:
        return img
    elif num_output_channels == 3:
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = np.dstack([img, img, img])
        return img


def erase(img, x, y, h, w, v=0., inplace=False):
    """ Erase the input Tensor Image with given value.

        Args:
            img (Tensor Image): Tensor image of size (C, H, W) to be erased
            x (int): x in (x, y) i.e coordinates of the upper left corner.
            y (int): y in (x, y) i.e coordinates of the upper left corner.
            h (int): Height of the erased region.
            w (int): Width of the erased region.
            v: Erasing value.
            inplace(bool, optional): For in-place operations. By default is set False.

        Returns:
            Tensor Image: Erased image.
        """
    if not _is_numpy_image(img):
        raise TypeError('img should be numpy Image. Got {}'.format(type(img)))

    if not inplace:
        img = img.copy()
        # img = img

    img[x:x + h, y:y + w, :] = v
    return img


def invert(image):
    """
    Invert an numpy image. If the image is a single-channel image, the value of pixel v is converted to 255 - v. If
    the image is a 3-channel image, the RGB value is converted respectively.
    :param image: The image to be converted.
    :return: The converted image.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("The image should be of type np.ndarray. Got type {}.".format(type(image)))
    if str(image.dtype) == 'uint8':
        image = 255 - image
    else:
        image = 1. - image
    return image


def gray_scale_log(image, scale, translation):
    """
    Operate log on the value of image.
    :param image: (numpy image) image to be operated.
    :param scale: Log scale of the operation.
    :param translation: Translation ot the log operation.
    :return: Gray_scale_logged image.
    """
    image = scale * np.log(image + translation)
    image = cut(image.astype(np.uint8))
    # print(image.shape)
    return image


def gray_scale_gamma(image, scale, translation):
    """
        Operate gamma transformation on the value of image.
        :param image: (numpy image) image to be operated.
        :param scale: Log scale of the operation.
        :param translation: Translation ot the log operation.
        :return: Gray_scale_logged image.
        """
    image = np.power(image + translation, scale)
    image = cut(image.astype(np.uint8))
    # print(image.shape)
    return image


def threshold(image, thresh, out_channels=1):
    """
    Threshold a numpy image.
    :param out_channels: the output channel number
    :param image: (numpy image) Image to be threshold.
    :param thresh: (int or str or None) If int, it is used to threshold.
    :return: threshed image.
    """
    gray_image = to_grayscale(image, num_output_channels=1)
    if isinstance(thresh, int):
        if (thresh < 0) or (thresh > 255):
            raise ValueError("Thresh should be between [0, 255]")
        _, image = cv2.threshold(gray_image, thresh, 255, cv2.THRESH_BINARY)
    elif isinstance(thresh, str) or (thresh is None):
        thresh, image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    if out_channels == 1:
        return image
    elif out_channels == 3:
        return np.dstack([image, image, image])


def histeq(image: np.ndarray):
    """
    operate histogram equalization on the image.
    :param image: Image to be operated.
    :return: The operated image.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("Image should be of type np.ndarray. Got {}.".format(type(image)))
    temp = 0
    max_value = np.max(image)
    area = image.shape[0] * image.shape[1]
    New_image = np.zeros_like(image)
    for value in range(256):
        index_i = np.where(image == value)
        # print(len(index_i[0]), len(index_i[1]))
        temp += len(index_i[0])
        new_value = max_value * temp / area
        New_image[index_i] = new_value
    return New_image.astype(np.uint8)


def meanBlur(image, kernel_size, anchor):
    if not isinstance(image, np.ndarray):
        raise TypeError("Image should be of type np.ndarray. Got {}.".format(type(image)))
    if isinstance(kernel_size, numbers.Number):
        kernel_size = (kernel_size, kernel_size)
    elif isinstance(kernel_size, tuple):
        if not (len(kernel_size) == 2):
            raise ValueError("kernel_size's length should be 2. Got length {}.".format(len(kernel_size)))
    image = cv2.blur(image, ksize=kernel_size, anchor=anchor)
    return image


def gaussianBlur(image, kernel_size, sigmaX, sigmaY):
    if not isinstance(image, np.ndarray):
        raise TypeError("Image should be of type np.ndarray. Got {}.".format(type(image)))
    if isinstance(kernel_size, numbers.Number):
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel_size = (kernel_size, kernel_size)
    elif isinstance(kernel_size, tuple):
        if not (len(kernel_size) == 2):
            raise ValueError("kernel_size's length should be 2. Got length {}.".format(len(kernel_size)))
        kernel_size = list(kernel_size)
        for i, number in enumerate(kernel_size):
            if number % 2 == 0:
                kernel_size[i] += 1
        kernel_size = tuple(kernel_size)
    image = cv2.GaussianBlur(image, ksize=kernel_size, sigmaX=sigmaX, sigmaY=sigmaY)
    return image


def medianBlur(image, kernel_size):
    if not isinstance(image, np.ndarray):
        raise TypeError("Image should be of type np.ndarray. Got {}.".format(type(image)))
    if not isinstance(kernel_size, numbers.Number):
        raise TypeError("kernel_size should be an integer. Got {}.".format(type(kernel_size)))
    image = cv2.medianBlur(image, kernel_size)
    return image


def sobel(image, mode='x'):
    if mode not in ['x', 'y', 'xy']:
        raise ValueError("Mode options: 'x', 'y', 'xy'. Got '{}'.".format(mode))
    if mode == 'x':
        return np.uint8(np.absolute(cv2.Sobel(image, cv2.CV_64F, 1, 0)))
    elif mode == 'y':
        return np.uint8(np.absolute(cv2.Sobel(image, cv2.CV_64F, 0, 1)))
    elif mode == 'xy':
        return cv2.bitwise_or(np.uint8(np.absolute(cv2.Sobel(image, cv2.CV_64F, 1, 0))),
                              np.uint8(np.absolute(cv2.Sobel(image, cv2.CV_64F, 0, 1))))

