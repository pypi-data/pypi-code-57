# coding=gbk
"""
author(作者): Channing Xie(谢琛)
time(时间): 2020/6/18 10:01
filename(文件名): transforms_for_cv2.py
function description(功能描述):
...
"""
import torch
import math
import sys
import random
import numpy as np
import cv2
import numbers
import collections
import warnings
# import types
print("torch.version: ", torch.__version__)
print("numpy.version: ", np.__version__)

import preprocessing_functions_for_cv2 as F

if sys.version_info < (3, 3):
    Sequence = collections.Sequence
    Iterable = collections.Iterable
else:
    Sequence = collections.abc.Sequence
    Iterable = collections.abc.Iterable

_cv2_interpolation_to_str = {
    cv2.INTER_NEAREST: "cv2.INTER_NEAREST",
    cv2.INTER_LINEAR: "cv2.INTER_LINEAR",
    cv2.INTER_CUBIC: "cv2.INTER_CUBIC",
    cv2.INTER_AREA: "cv2.INTER_AREA",
    cv2.INTER_LANCZOS4: "cv2.LANCZOS4",
}

__all__ = ["Compose", "Normalize", "ToTensor", "Resize", "CenterCrop", "Pad", "Lambda",
           "RandomApply", "RandomChoice", "RandomOrder", "RandomTransforms", "RandomCrop",
           "RandomHorizontalFlip", "RandomVerticalFlip", "RandomPerspective", "RandomResizedCrop",
           "FiveCrop", "TenCrop", "LinearTransformation", "ColorJitter", "RandomRotation", "RandomAffine",
           "Grayscale", "RandomGrayscale", "RandomErasing", "Invert", "GrayScaleLog", "GrayScaleGamma", "Threshold",
           "HistEqualize", "MeanBlur", "GaussianBlur", "MedianBlur", "SobelSharpen"]


class SobelSharpen(object):
    """
    Operate sobel sharpening on the image.
    """
    def __init__(self, mode='x'):
        self.mode = mode

    def __call__(self, image):
        return F.sobel(image, self.mode)

    def __repr__(self):
        return self.__class__.__name__


class MedianBlur(object):
    """
    MedianBlur the image.
    """
    def __init__(self, kernel_size: int = 3):
        self.kernel_size = kernel_size

    def __call__(self, image):
        return F.medianBlur(image, self.kernel_size)

    def __repr__(self):
        return self.__class__.__name__


class GaussianBlur(object):
    """
    GaussianBlur the image.
    """
    def __init__(self, kernel_size: (tuple, int) = (3, 3), sigmaX=0., sigmaY=0.):
        self.kernel_size = kernel_size
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY

    def __call__(self, image):
        return F.gaussianBlur(image, self.kernel_size, self.sigmaX, self.sigmaY)

    def __repr__(self):
        return self.__class__.__name__


class MeanBlur(object):
    """
    Blur the image.
    """
    def __init__(self, kernel_size: (int, tuple) = (3, 3), anchor=None):
        self.kernel_size = kernel_size
        self.anchor = anchor

    def __call__(self, image):
        return F.meanBlur(image, self.kernel_size, self.anchor)

    def __repr__(self):
        return self.__class__.__name__


class HistEqualize(object):
    """
    Operate hist_equalization on a numpy image.
    """
    def __call__(self, Image):
        return F.histeq(Image)

    def __repr__(self):
        return self.__class__.__name__


class Threshold(object):
    """
    Threshold the numpy image.
    """
    def __init__(self, thresh: (int, str, None), out_channels=1):
        self.thresh = thresh
        self.channels = out_channels

    def __call__(self, Image):
        return F.threshold(Image, self.thresh, self.channels)

    def __repr__(self):
        return self.__class__.__name__


class GrayScaleGamma(object):
    """
        Operate gamma transformation on the value of numpy image.
        """

    def __init__(self, scale=1, translation=1):
        self.scale = scale
        self.translation = translation

    def __call__(self, Image):
        return F.gray_scale_gamma(Image, self.scale, self.translation)

    def __repr__(self):
        return self.__class__.__name__


class GrayScaleLog(object):
    """
    Operate log transformation on the value of numpy image.
    """
    def __init__(self, scale=1, translation=1):
        self.scale = scale
        self.translation = translation

    def __call__(self, Image):
        return F.gray_scale_log(Image, self.scale, self.translation)

    def __repr__(self):
        return self.__class__.__name__


class Invert(object):
    """
    Invert an image.
    """
    def __call__(self, image: np.ndarray):
        return F.invert(image)

    def __repr__(self):
        return self.__class__.__name__


class RandomErasing(object):
    """
    Randomly selects a rectangle region in an image and erases its pixels.
        'Random Erasing Data Augmentation' by Zhong et al.
        See https://arxiv.org/pdf/1708.04896.pdf
    Args:
         p: probability that the random erasing operation will be performed.
         scale: range of proportion of erased area against input image.
         ratio: range of aspect ratio of erased area.
         value: erasing value. Default is 0. If a single int, it is used to
            erase all pixels. If a tuple of length 3, it is used to erase
            R, G, B channels respectively.
            If a str of 'random', erasing each pixel with random values.
         inplace: boolean to make this transform inplace. Default set to False.

    Returns:
        Erased Image.
    # Examples:
        transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        transforms.RandomErasing(),
        ])
    """

    def __init__(self, p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3), value=0, inplace=False):
        assert isinstance(value, (numbers.Number, str, tuple, list))
        if (scale[0] > scale[1]) or (ratio[0] > ratio[1]):
            warnings.warn("range should be of kind (min, max)")
        if scale[0] < 0 or scale[1] > 1:
            raise ValueError("range of scale should be between 0 and 1")
        if p < 0 or p > 1:
            raise ValueError("range of random erasing probability should be between 0 and 1")

        self.p = p
        self.scale = scale
        self.ratio = ratio
        self.value = value
        self.inplace = inplace

    @staticmethod
    def get_params(img, scale, ratio, value=0):
        """Get parameters for ``erase`` for a random erasing.

        Args:
            img (numpy image): numpy image to be erased.
            scale: range of proportion of erased area against input image.
            ratio: range of aspect ratio of erased area.
            value: value to be set on the erased area.

        Returns:
            tuple: params (i, j, h, w, v) to be passed to ``erase`` for random erasing.
        """
        img_h, img_w = img.shape[:2]
        area = img_h * img_w

        for attempt in range(10):
            erase_area = random.uniform(scale[0], scale[1]) * area
            aspect_ratio = random.uniform(ratio[0], ratio[1])

            h = int(round(math.sqrt(erase_area * aspect_ratio)))
            w = int(round(math.sqrt(erase_area / aspect_ratio)))

            if h < img_h and w < img_w:
                i = random.randint(0, img_h - h)
                j = random.randint(0, img_w - w)
                v = None
                if isinstance(value, numbers.Number):
                    v = np.ones(shape=(h, w, 3)) * value
                elif isinstance(value, str):
                    v = np.random.normal(size=(h, w, 3))
                    # v = torch.empty([img_c, h, w], dtype=torch.float32).normal_()
                elif isinstance(value, (list, tuple)):
                    if not len(value) == 3:
                        raise ValueError("If 'value' is a tuple or a list, it should be of length 3 corresponding to "
                                         "R, G, B channel. Got length {} {}.".format(len(value), type(value)))
                    else:
                        v1 = np.ones(shape=(h, w)) * value[0]
                        v2 = np.ones(shape=(h, w)) * value[1]
                        v3 = np.ones(shape=(h, w)) * value[2]
                        v = np.dstack([v1, v2, v3])
                        # v = torch.tensor(value, dtype=torch.float32).view(-1, 1, 1).expand(-1, h, w)
                # print(h, w, v.shape)
                return i, j, h, w, v

        # Return original image
        return 0, 0, img_h, img_w, img

    def __call__(self, img):
        """
        Args:
            img (Tensor): Tensor image of size (C, H, W) to be erased.

        Returns:
            img (Tensor): Erased Tensor image.
        """
        if random.uniform(0, 1) < self.p:
            x, y, h, w, v = self.get_params(img, scale=self.scale, ratio=self.ratio, value=self.value)
            return F.erase(img, x, y, h, w, v, self.inplace)
        return img


class RandomGrayscale(object):
    """
    Randomly convert an image to grayscale with a probability of p (default is 0.1).

    Args:
        p (float): probability that image would be converted to grayscale.

    Returns:
        numpy Image: Grayscale version of the input image with probability p and unchanged
        with probability (1-p).
        - If input image is 1 channel: grayscale version is 1 channel
        - If input image is 3 channel: grayscale version is 3 channel with r == g == b

    """

    def __init__(self, p=0.1):
        self.p = p

    def __call__(self, img):
        """
        Args:
            img (numpy Image): Image to be converted to grayscale.

        Returns:
            numpy Image: Randomly grayscaled image.
        """
        # num_output_channels = 1 if img.mode == 'L' else 3
        if random.random() < self.p:
            return F.to_grayscale(img)
            # return F.to_grayscale(img, num_output_channels=num_output_channels)
        return img

    def __repr__(self):
        return self.__class__.__name__ + '(p={0})'.format(self.p)


class Grayscale(object):
    """Convert image to grayscale.

    Args:
        num_output_channels (int): (1 or 3) number of channels desired for output image

    Returns:
        PIL Image: Grayscale version of the input.
        - If num_output_channels == 1 : returned image is single channel
        - If num_output_channels == 3 : returned image is 3 channel with r == g == b

    """

    def __init__(self, num_output_channels=1):
        self.num_output_channels = num_output_channels

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be converted to grayscale.

        Returns:
            PIL Image: Randomly grayscaled image.
        """
        return F.to_grayscale(img, num_output_channels=self.num_output_channels)

    def __repr__(self):
        return self.__class__.__name__ + '(num_output_channels={0})'.format(self.num_output_channels)


# TODO
class RandomAffine(object):
    """
    Random affine transformation of the image keeping center invariant

    Args:
        degrees (sequence or float or int): Range of degrees to select from.
            If degrees is a number instead of sequence like (min, max), the range of degrees
            will be (-degrees, +degrees). Set to 0 to deactivate rotations.
        translate (tuple, optional): tuple of maximum absolute fraction for horizontal
            and vertical translations. For example translate=(a, b), then horizontal shift
            is randomly sampled in the range -img_width * a < dx < img_width * a and vertical shift is
            randomly sampled in the range -img_height * b < dy < img_height * b. Will not translate by default.
        scale (tuple, optional): scaling factor interval, e.g (a, b), then scale is
            randomly sampled from the range a <= scale <= b. Will keep original scale by default.
        shear (sequence or float or int, optional): Range of degrees to select from.
            If shear is a number, a shear parallel to the x axis in the range (-shear, +shear)
            will be apllied. Else if shear is a tuple or list of 2 values a shear parallel to the x axis in the
            range (shear[0], shear[1]) will be applied. Else if shear is a tuple or list of 4 values,
            a x-axis shear in (shear[0], shear[1]) and y-axis shear in (shear[2], shear[3]) will be applied.
            Will not apply shear by default
        resample ({cv2.INTER_NEAREST, cvw.INTER_LINEAR, cv2.INTER_CUBIC}, optional):
            An optional resampling filter. See `filters`_ for more information.
            If omitted, or if the image has mode "1" or "P", it is set to cv2.INTER_NEAREST.
        fillcolor (tuple or int): Optional fill color (Tuple for RGB Image And int for grayscale) for the area
            outside the transform in the output image.
    """

    def __init__(self, degrees, translate=None, scale=None, shear=None, resample=False, fillcolor=0):
        if isinstance(degrees, numbers.Number):
            if degrees < 0:
                raise ValueError("If degrees is a single number, it must be positive.")
            self.degrees = (-degrees, degrees)
        else:
            assert isinstance(degrees, (tuple, list)) and len(degrees) == 2, \
                "degrees should be a list or tuple and it must be of length 2."
            self.degrees = degrees

        if translate is not None:
            assert isinstance(translate, (tuple, list)) and len(translate) == 2, \
                "translate should be a list or tuple and it must be of length 2."
            for t in translate:
                if not (0.0 <= t <= 1.0):
                    raise ValueError("translation values should be between 0 and 1")
        self.translate = translate

        if scale is not None:
            assert isinstance(scale, (tuple, list)) and len(scale) == 2, \
                "scale should be a list or tuple and it must be of length 2."
            for s in scale:
                if s <= 0:
                    raise ValueError("scale values should be positive")
        self.scale = scale

        if shear is not None:
            if isinstance(shear, numbers.Number):
                if shear < 0:
                    raise ValueError("If shear is a single number, it must be positive.")
                self.shear = (-shear, shear)
            else:
                assert isinstance(shear, (tuple, list)) and \
                    (len(shear) == 2 or len(shear) == 4), \
                    "shear should be a list or tuple and it must be of length 2 or 4."
                # X-Axis shear with [min, max]
                if len(shear) == 2:
                    self.shear = [shear[0], shear[1], 0., 0.]
                elif len(shear) == 4:
                    self.shear = [s for s in shear]
        else:
            self.shear = shear

        self.resample = resample
        self.fillcolor = fillcolor

    @staticmethod
    def get_params(degrees, translate, scale_ranges, shears, img_size):
        """Get parameters for affine transformation

        Returns:
            sequence: params to be passed to the affine transformation
        """
        angle = random.uniform(degrees[0], degrees[1])
        translations, scale, shear = None, None, None
        if translate is not None:
            max_dx = translate[0] * img_size[0]
            max_dy = translate[1] * img_size[1]
            translations = (np.round(random.uniform(-max_dx, max_dx)),
                            np.round(random.uniform(-max_dy, max_dy)))
        else:
            translations = (0, 0)

        if scale_ranges is not None:
            scale = random.uniform(scale_ranges[0], scale_ranges[1])
        else:
            scale = 1.0

        if shears is not None:
            if len(shears) == 2:
                shear = [random.uniform(shears[0], shears[1]), 0.]
            elif len(shears) == 4:
                shear = [random.uniform(shears[0], shears[1]),
                         random.uniform(shears[2], shears[3])]
        else:
            shear = 0.0

        return angle, translations, scale, shear

    def __call__(self, img):
        """
            img (PIL Image): Image to be transformed.

        Returns:
            PIL Image: Affine transformed image.
        """
        ret = self.get_params(self.degrees, self.translate, self.scale, self.shear, img.size)
        return F.affine(img, *ret, resample=self.resample, fillcolor=self.fillcolor)

    def __repr__(self):
        s = '{name}(degrees={degrees}'
        if self.translate is not None:
            s += ', translate={translate}'
        if self.scale is not None:
            s += ', scale={scale}'
        if self.shear is not None:
            s += ', shear={shear}'
        if self.resample > 0:
            s += ', resample={resample}'
        if self.fillcolor != 0:
            s += ', fillcolor={fillcolor}'
        s += ')'
        d = dict(self.__dict__)
        d['resample'] = _cv2_interpolation_to_str[d['resample']]
        return s.format(name=self.__class__.__name__, **d)


class RandomRotation(object):
    """
    Rotate the image by angle.
    Args:
        degrees (sequence or float or int): Range of degrees to select from.
            If degrees is a number instead of sequence like (min, max), the range of degrees
            will be (-degrees, +degrees).
        resample ({cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_CUBIC}, optional):
            An optional resampling filter.
        expand (bool, optional): Optional expansion flag.
            If true, expands the output to make it large enough to hold the entire rotated image.
            If false or omitted, make the output image the same size as the input image.
            Note that the expand flag assumes rotation around the center and no translation.
        center (2-tuple, optional): Optional center of rotation.
            Origin is the upper left corner.
            Default is the center of the image.
    """

    def __init__(self, degrees, resample=False, expand=1., center=None):
        if isinstance(degrees, numbers.Number):
            if degrees < 0:
                raise ValueError("If degrees is a single number, it must be positive.")
            self.degrees = (-degrees, degrees)
        else:
            if len(degrees) != 2:
                raise ValueError("If degrees is a sequence, it must be of len 2.")
            self.degrees = degrees

        self.resample = resample
        self.expand = expand
        self.center = center

    @staticmethod
    def get_params(degrees):
        """Get parameters for ``rotate`` for a random rotation.

        Returns:
            sequence: params to be passed to ``rotate`` for random rotation.
        """
        angle = random.uniform(degrees[0], degrees[1])

        return angle

    def __call__(self, img):
        """
        Args:
            img (numpy Image): Image to be rotated.

        Returns:
            numpy Image: Rotated image.
        """

        angle = self.get_params(self.degrees)

        return F.rotate(img, angle, self.resample, self.expand, self.center)

    def __repr__(self):
        format_string = self.__class__.__name__ + '(degrees={0}'.format(self.degrees)
        format_string += ', resample={0}'.format(self.resample)
        format_string += ', expand={0}'.format(self.expand)
        if self.center is not None:
            format_string += ', center={0}'.format(self.center)
        format_string += ')'
        return format_string


# TODO
class ColorJitter(object):
    """
    Randomly change the brightness, contrast and saturation of an numpy image. (亮度，对比度，饱和度)

    Args:
        brightness (float or tuple of float (min, max)): How much to jitter brightness.
            brightness_factor is chosen uniformly from [max(0, 1 - brightness), 1 + brightness]
            or the given [min, max]. Should be non negative numbers.
        contrast (float or tuple of float (min, max)): How much to jitter contrast.
            contrast_factor is chosen uniformly from [max(0, 1 - contrast), 1 + contrast]
            or the given [min, max]. Should be non negative numbers.
        saturation (float or tuple of float (min, max)): How much to jitter saturation.
            saturation_factor is chosen uniformly from [max(0, 1 - saturation), 1 + saturation]
            or the given [min, max]. Should be non negative numbers.
        hue (float or tuple of float (min, max)): How much to jitter hue.
            hue_factor is chosen uniformly from [-hue, hue] or the given [min, max].
            Should have 0<= hue <= 0.5 or -0.5 <= min <= max <= 0.5.
    """
    def __init__(self, brightness=0, contrast=0, saturation=0, hue=0):
        self.brightness = self._check_input(brightness, 'brightness')
        self.contrast = self._check_input(contrast, 'contrast')
        self.saturation = self._check_input(saturation, 'saturation')
        self.hue = self._check_input(hue, 'hue', center=0, bound=(-0.5, 0.5),
                                     clip_first_on_zero=False)

    @staticmethod
    def _check_input(value, name, center=1, bound=(0, float('inf')), clip_first_on_zero=True):
        if isinstance(value, numbers.Number):
            if value < 0:
                raise ValueError("If {} is a single number, it must be non negative.".format(name))
            value = [center - value, center + value]
            if clip_first_on_zero:
                value[0] = max(value[0], 0)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            if not bound[0] <= value[0] <= value[1] <= bound[1]:
                raise ValueError("{} values should be between {}".format(name, bound))
        else:
            raise TypeError("{} should be a single number or a list/tuple with length 2.".format(name))

        # if value is 0 or (1., 1.) for brightness/contrast/saturation
        # or (0., 0.) for hue, do nothing
        if value[0] == value[1] == center:
            value = None
        return value

    @staticmethod
    def get_params(brightness, contrast, saturation, hue):
        """Get a randomized transform to be applied on image.

        Arguments are the same as that of __init__.

        Returns:
            Transform which randomly adjusts brightness, contrast and
            saturation in a random order.
        """
        transforms = []

        if brightness is not None:
            brightness_factor = random.uniform(brightness[0], brightness[1])
            transforms.append(Lambda(lambda img: F.adjust_brightness(img, brightness_factor)))

        if contrast is not None:
            contrast_factor = random.uniform(contrast[0], contrast[1])
            transforms.append(Lambda(lambda img: F.adjust_contrast(img, contrast_factor)))

        if saturation is not None:
            saturation_factor = random.uniform(saturation[0], saturation[1])
            transforms.append(Lambda(lambda img: F.adjust_saturation(img, saturation_factor)))

        if hue is not None:
            hue_factor = random.uniform(hue[0], hue[1])
            transforms.append(Lambda(lambda img: F.adjust_hue(img, hue_factor)))

        random.shuffle(transforms)
        transform = Compose(transforms)

        return transform

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Input image.

        Returns:
            PIL Image: Color jittered image.
        """
        transform = self.get_params(self.brightness, self.contrast,
                                    self.saturation, self.hue)
        return transform(img)

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        format_string += 'brightness={0}'.format(self.brightness)
        format_string += ', contrast={0}'.format(self.contrast)
        format_string += ', saturation={0}'.format(self.saturation)
        format_string += ', hue={0})'.format(self.hue)
        return format_string


class LinearTransformation(object):
    """Transform a tensor image with a square transformation matrix and a mean_vector computed
    offline.
    Given transformation_matrix and mean_vector, will flatten the torch.*Tensor and
    subtract mean_vector from it which is then followed by computing the dot
    product with the transformation matrix and then reshaping the tensor to its
    original shape.

    Applications:
        whitening transformation: Suppose X is a column vector zero-centered data.
        Then compute the data covariance matrix [D x D] with torch.mm(X.t(), X),
        perform SVD on this matrix and pass it as transformation_matrix.

    Args:
        transformation_matrix (Tensor): tensor [D x D], D = C x H x W
        mean_vector (Tensor): tensor [D], D = C x H x W
    """

    def __init__(self, transformation_matrix, mean_vector):
        if transformation_matrix.size(0) != transformation_matrix.size(1):
            raise ValueError("transformation_matrix should be square. Got " +
                             "[{} x {}] rectangular matrix.".format(*transformation_matrix.size()))

        if mean_vector.size(0) != transformation_matrix.size(0):
            raise ValueError("mean_vector should have the same length {}".format(mean_vector.size(0)) +
                             " as any one of the dimensions of the transformation_matrix [{} x {}]"
                             .format(*transformation_matrix.size()))

        self.transformation_matrix = transformation_matrix
        self.mean_vector = mean_vector

    def __call__(self, tensor):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be whitened.

        Returns:
            Tensor: Transformed image.
        """
        if tensor.size(0) * tensor.size(1) * tensor.size(2) != self.transformation_matrix.size(0):
            raise ValueError("tensor and transformation matrix have incompatible shape." +
                             "[{} x {} x {}] != ".format(*tensor.size()) +
                             "{}".format(self.transformation_matrix.size(0)))
        flat_tensor = tensor.view(1, -1) - self.mean_vector
        transformed_tensor = torch.mm(flat_tensor, self.transformation_matrix)
        tensor = transformed_tensor.view(tensor.size())
        return tensor

    def __repr__(self):
        format_string = self.__class__.__name__ + '(transformation_matrix='
        format_string += (str(self.transformation_matrix.tolist()) + ')')
        format_string += (", (mean_vector=" + str(self.mean_vector.tolist()) + ')')
        return format_string


class TenCrop(object):
    """
    Crop the given numpy Image into four corners and the central crop together with their the
    flipped version (horizontal flipping is used by default).

    .. Note::
         This transform returns a tuple of images and there may be a mismatch in the number of
         inputs and targets your Dataset returns. See below for an example of how to deal with
         this.

    Args:
        size (sequence or int): Desired output size of the crop. If size is an
            int instead of sequence like (h, w), a square crop (size, size) is
            made.
        vertical_flip (bool): Use vertical flipping instead of horizontal

    Example:
         transform = Compose([
            TenCrop(size), # this is a list of numpy Images
            Lambda(lambda crops: torch.stack([ToTensor()(crop) for crop in crops])) # returns a 4D tensor
         ])
         #In your test loop you can do the following:
         input, target = batch # input is a 5d tensor, target is 2d
         bs, ncrops, c, h, w = input.size()
         result = model(input.view(-1, c, h, w)) # fuse batch size and ncrops
         result_avg = result.view(bs, ncrops, -1).mean(1) # avg over crops
    """

    def __init__(self, size, vertical_flip=False):
        self.size = size
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            assert len(size) == 2, "Please provide only two dimensions (h, w) for size."
            self.size = size
        self.vertical_flip = vertical_flip

    def __call__(self, img):
        return F.ten_crop(img, self.size, self.vertical_flip)

    def __repr__(self):
        return self.__class__.__name__ + '(size={0}, vertical_flip={1})'.format(self.size, self.vertical_flip)


class FiveCrop(object):
    """
    Crop the given numpy Image into five crop, including four corners and the central crop.

    Notes::
        This transform returns a tuple of images and there may be a mismatch in the number of
        inputs and targets your Dataset returns. See below for an example of how to deal with this.

    Example:
        transform = Compose([
            FiveCrop(size),  # this is a list of numpy Images
            Lambda( lambda crops: torch.stack([ToTensor()(crop) for crop in crops]))  # returns a 4D tensor
        ])
        # In the test loop, you can do the following:
        input, target = batch  # input is a 5D tensor, target is 2D
        bs, ncrops, c, h, w = input.size()
        result = model(input.view(-1, c, h, w))  # fuse batch size and ncrops
        result_avg = result.view(bs, ncrops, -1).mean(1)  # average over crops

    Args:
        size (sequence or int): Desired output size of the crop. If size is an "int" instead of
            sequence like (h, w), a square crop of size (size, size) is made.
    """
    def __init__(self, size):
        self.size = size
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            assert len(size) == 2, "Please provide only 2 dimensions (h, w) for size."
            self.size = size

    def __call__(self, Image):
        return F.five_crop(Image, self.size)

    def __repr__(self):
        return self.__class__.__name__ + "(size={0})".format(self.size)


class RandomResizedCrop(object):
    """Crop the given numpy Image to random size and aspect ratio.

    A crop of random size (default: of 0.08 to 1.0) of the original size and a random
    aspect ratio (default: of 3/4 to 4/3) of the original aspect ratio is made. This crop
    is finally resized to given size.
    This is popularly used to train the Inception networks.

    Args:
        size: expected output size of each edge
        scale: range of size of the origin size cropped
        ratio: range of aspect ratio of the origin aspect ratio cropped
        interpolation: Default: PIL.Image.BILINEAR
    """

    def __init__(self, size, scale=(0.08, 1.0), ratio=(3. / 4., 4. / 3.), interpolation=cv2.INTER_LINEAR):
        if isinstance(size, tuple):
            self.size = size
        else:
            self.size = (size, size)
        if (scale[0] > scale[1]) or (ratio[0] > ratio[1]):
            warnings.warn("range should be of kind (min, max)")

        self.interpolation = interpolation
        self.scale = scale
        self.ratio = ratio

    @staticmethod
    def get_params(img, scale, ratio):
        """Get parameters for ``crop`` for a random sized crop.

        Args:
            img (numpy Image): Image to be cropped.
            scale (tuple): range of size of the origin size cropped
            ratio (tuple): range of aspect ratio of the origin aspect ratio cropped

        Returns:
            tuple: params (i, j, h, w) to be passed to ``crop`` for a random
                sized crop.
        """
        area = img.shape[0] * img.shape[1]

        for attempt in range(10):
            target_area = random.uniform(*scale) * area
            log_ratio = (math.log(ratio[0]), math.log(ratio[1]))
            aspect_ratio = math.exp(random.uniform(*log_ratio))

            w = int(round(math.sqrt(target_area * aspect_ratio)))
            h = int(round(math.sqrt(target_area / aspect_ratio)))

            if w <= img.shape[1] and h <= img.shape[0]:
                i = random.randint(0, img.size[1] - h)
                j = random.randint(0, img.size[0] - w)
                return i, j, h, w

        # Fallback to central crop
        in_ratio = img.shape[1] / img.shape[0]
        if in_ratio < min(ratio):
            w = img.shape[1]
            h = int(round(w / min(ratio)))
        elif in_ratio > max(ratio):
            h = img.shape[0]
            w = int(round(h * max(ratio)))
        else:  # whole image
            w = img.shape[1]
            h = img.shape[0]
        i = (img.shape[0] - h) // 2
        j = (img.shape[1] - w) // 2
        return i, j, h, w

    def __call__(self, img):
        """
        Args:
            img (PIL Image): Image to be cropped and resized.

        Returns:
            PIL Image: Randomly cropped and resized image.
        """
        i, j, h, w = self.get_params(img, self.scale, self.ratio)
        return F.resized_crop(img, i, j, h, w, self.size, self.interpolation)

    def __repr__(self):
        interpolate_str = _cv2_interpolation_to_str[self.interpolation]
        format_string = self.__class__.__name__ + '(size={0}'.format(self.size)
        format_string += ', scale={0}'.format(tuple(round(s, 4) for s in self.scale))
        format_string += ', ratio={0}'.format(tuple(round(r, 4) for r in self.ratio))
        format_string += ', interpolation={0})'.format(interpolate_str)
        return format_string


class RandomPerspective(object):
    """Performs Perspective transformation of the given numpy Image randomly with a given probability.

    Args:
        interpolation : Default- cv2.INTER_CUBIC

        p (float): probability of the image being perspectively transformed. Default value is 0.5

        distortion_scale(float): it controls the degree of distortion and ranges from 0 to 1. Default value is 0.5.

    """

    def __init__(self, distortion_scale=0.5, p=0.5, interpolation=cv2.INTER_CUBIC):
        self.p = p
        self.interpolation = interpolation
        self.distortion_scale = distortion_scale

    def __call__(self, image):
        """
        Args:
            image (numpy.ndarray): Image to be Perspectively transformed.

        Returns:
            numpy Image: Random perspectivley transformed image.
        """
        if not F._is_numpy_image(image):
            raise TypeError('img should be numpy Image. Got {}'.format(type(image)))

        if random.random() < self.p:
            height, width = image.shape[:2]
            startPoints, endPoints = self.get_params(width, height, self.distortion_scale)
            return F.perspective(image, startPoints, endPoints, self.interpolation)
        return image

    @staticmethod
    def get_params(width, height, distortion_scale):
        """Get parameters for ``perspective`` for a random perspective transform.

        Args:
            width : width of the image.
            height : height of the image.
            distortion_scale : degree of distortion and ranges from 0 to 1. Default value is 0.5.

        Returns:
            List containing [top-left, top-right, bottom-right, bottom-left] of the original image,
            List containing [top-left, top-right, bottom-right, bottom-left] of the transformed image.
        """
        half_height = int(height / 2)
        half_width = int(width / 2)
        topleft = (random.randint(0, int(distortion_scale * half_width)),
                   random.randint(0, int(distortion_scale * half_height)))
        topright = (random.randint(width - int(distortion_scale * half_width) - 1, width - 1),
                    random.randint(0, int(distortion_scale * half_height)))
        botright = (random.randint(width - int(distortion_scale * half_width) - 1, width - 1),
                    random.randint(height - int(distortion_scale * half_height) - 1, height - 1))
        botleft = (random.randint(0, int(distortion_scale * half_width)),
                   random.randint(height - int(distortion_scale * half_height) - 1, height - 1))
        startpoints = [(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)]
        endpoints = [topleft, topright, botright, botleft]
        return startpoints, endpoints

    def __repr__(self):
        return self.__class__.__name__ + '(p={})'.format(self.p)


class RandomVerticalFlip(object):
    """
    Vertically flip the given numpy Image randomly with a given probability.
    Args:
        p (float): probability of the image being flipped. Default value is 0.5.
    """
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, image):
        """
        :param image: numpy Image to be flipped.
        :return:randomly flipped image.
        """
        if random.random() < self.p:
            return F.vflip(image)
        return image


class RandomHorizontalFlip(object):
    """
    Horizontally flip the given numpy Image randomly with a given probability.
    Args:
        p (float): probability of the image being flipped. Default value is 0.5.
    """
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, image):
        """
        :param image: numpy Image to be flipped.
        :return:randomly flipped image.
        """
        if random.random() < self.p:
            return F.hflip(image)
        return image


# TODO
class RandomCrop(object):
    pass


class RandomTransforms(object):
    """Base class for a list of transformations with randomness

    Args:
        transforms (list or tuple): list of transformations
    """

    def __init__(self, transforms):
        assert isinstance(transforms, (list, tuple))
        self.transforms = transforms

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    # def __call__(self, img):
    #     return img

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string


class RandomApply(RandomTransforms):
    """Apply randomly a list of transformations with a given probability

    Args:
        transforms (list or tuple): list of transformations
        p (float): probability
    """

    def __init__(self, transforms, p=0.5):
        super(RandomApply, self).__init__(transforms)
        self.p = p

    def __call__(self, img):
        if self.p < random.random():
            return img
        for t in self.transforms:
            img = t(img)
        return img

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        format_string += '\n    p={}'.format(self.p)
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string


class RandomOrder(RandomTransforms):
    """Apply a list of transformations in a random order
    """
    def __call__(self, img):
        order = list(range(len(self.transforms)))
        random.shuffle(order)
        for i in order:
            img = self.transforms[i](img)
        return img


class RandomChoice(RandomTransforms):
    """Apply single transformation randomly picked from a list
    """
    def __call__(self, img):
        t = random.choice(self.transforms)
        return t(img)


class Lambda(object):
    """Apply a user-defined lambda as a transform.

    Args:
        lambd (function): Lambda/function to be used for transform.
    """

    def __init__(self, lambd):
        assert callable(lambd), repr(type(lambd).__name__) + " object is not callable"
        self.lambd = lambd

    def __call__(self, img):
        return self.lambd(img)

    def __repr__(self):
        return self.__class__.__name__ + '()'


class Pad(object):
    """
    Pad the given numpy Image on its sides with the given "pad" value.

    Args:
        padding (int or tuple): Padding on each border. If a single int is provided, it will be
            used to pad all borders. If tuple of length 2 is provided, it will be padded on left/right
            and top/bottom respectively. If a tuple of length 4 is provided, it will be padded for the
            left, top, right and bottom.
        fill (int or tuple): Pixel fill value for constant fill. Default is 0. If a tuple of length 3,
            it is used to fill R, G, B channels respectively.
        padding_mode (str): Type of padding. It should be "constant", "edge", "reflect", "symmetric".
            Default is "constant".
            - constant: pad with a constant value, this value is specified with fill.
            - edge: pad with the last value at the edge of the image.
            - reflect: pad with reflection of image without repeating the last value on the edge.
                For example, padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode will
                result in [3, 2, 1, 2, 3, 4, 3, 2]
            - symmetric: pad with reflection of image repeating the last value on the edge.
                For example, padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode will
                result in [2, 1, 1, 2, 3, 4, 4, 3]

    """
    def __init__(self, padding, fill=0, padding_mode='constant'):
        assert isinstance(padding, (numbers.Number, tuple))
        assert isinstance(fill, (numbers.Number, str, tuple))
        assert padding_mode in ['constant', "edge", "reflect", "symmetric"]
        if isinstance(padding, Sequence) and len(padding) not in [2, 4]:
            raise ValueError("Padding must be an int or a 2, or 4 element tuple, not a" +
                             "{} element tuple".format(len(padding)))

        self.padding = padding
        self.fill = fill
        self.padding_mode = padding_mode

    def __call__(self, image):
        """

        :param image (numpy.ndarray): Image to be padded.
        :return: Padded image (numpy.ndarray)
        """
        return F.pad(image, self.padding, self.fill, self.padding_mode)


class CenterCrop(object):
    """
    Crop the given numpy Image at the center.

    Args:
        size (sequence or int): Desired output size of the crop. If size is an integer
        instead of sequence like (h, w), a square crop (size, size) is made.
    """
    def __init__(self, size):
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size

    def __call__(self, image):
        """
        :param image: (numpy.ndarray) Image to be cropped.
        :return: (numpy.ndarray) Cropped image.
        """
        return F.center_crop(image, self.size)


class Resize(object):
    """
    Resize the input ndarray image to the given size.

    Args:
        size(sequence or int): Desired output size. If size is a sequence like (h, w), the output
        size will be matched to it. If size is an int, smaller edge of the image will be matched
        to this integer. For example, if height > width, the image will be resized to the shape
        (size * height / width, size), else (size, size * width / height).
        interpolation(int, optional): Desired interpolation. Default is "cv2.BILINEAR"
    """
    def __init__(self, size, interpolation=cv2.INTER_LINEAR):
        assert isinstance(size, int) or (isinstance(size, Iterable) and len(size) == 2)
        self.size = size
        self.interpolation = interpolation

    def __call__(self, img):
        """
        :param img: Image to be resized.
        :return: ReSized image
        """
        img = img[0]
        return F.resize(img, self.size, self.interpolation)


class Compose(object):
    """
    Composes several transforms together.
    Example:
        transforms.Compose([
                        transforms.CenterCrop(10),
                        transforms.ToTensor(),
                        ])
    """
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, *args, **kwargs):
        for transform in self.transforms:
            args = transform(args)
        # self.__repr__()
        return args

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string


class Normalize(object):
    """
    Normalize a tensor image with mean and standard deviation.
    Args:
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool, optional): Bool to make this operation in-place or not.
    """
    def __init__(self, mean, std, inplace=False):
        self.mean = mean
        self.std = std
        self.inplace = inplace

    def __call__(self, tensor):
        """
        Normalize the tensor.
        :param tensor: Tensor image of size(C, H, W) to be normalized.
        :return: Normalized Tensor image
        """
        return F.normalize(tensor, self.mean, self.std, self.inplace)


class ToTensor(object):
    """
    Convert a "PIL Image" or "numpy.ndarray" to a tensor.

    Convert a PIL Image or numpy.ndarray (in shape H x W x C) in the range [0, 255] to a torch tensor
    (in shape C x H x W) in the range [0.0, 1.0].
    """
    def __init__(self, mode=1):
        self.mode = mode

    def __call__(self, pic):
        return F.to_tensor(pic, mode=self.mode)

