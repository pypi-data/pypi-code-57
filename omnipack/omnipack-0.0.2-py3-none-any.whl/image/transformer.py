from PIL import Image, ImageFilter, ImageEnhance
import random
import numpy as np
import math


class Transformer(object):

    def __init__(self, img: Image.Image, **kwargs):
        raise Exception("Not implemented")

    def __call__(self, *args, **kwargs):
        raise Exception("Not implemented")


class RandomNoise(Transformer):

    def __init__(self, mean: tuple, std: tuple):
        if isinstance(mean, tuple) and len(mean) == 2:
            self.min_mean = mean[0]
            self.max_mean = mean[1]
        elif isinstance(mean, (int, float)):
            self.min_mean = mean
            self.max_mean = mean
        else:
            raise TypeError(
                "Argument mean is either a tuple of 2, int or float.")

        if isinstance(std, tuple) and len(std) == 2:
            self.min_std = std[0]
            self.max_std = std[1]
        elif isinstance(std, (int, float)):
            self.min_std = std
            self.max_std = std
        else:
            raise TypeError(
                "Argument std is either a tuple of 2, int or float.")

    def __call__(self, img: Image.Image, **kwargs):
        """
        Add random Gaussian noise to image
        """

        mean = random.uniform(self.min_mean, self.max_mean)
        std = random.uniform(self.min_std, self.max_std)

        img = np.asarray(img)
        img = img + np.random.normal(mean, std, img.shape)
        img = Image.fromarray(np.uint8(img))
        return img, kwargs


class Resize(Transformer):
    def __init__(self, shape):
        assert isinstance(shape, tuple)
        assert len(shape) == 2

        self.shape = shape

    def __call__(self, img: Image.Image, **kwargs):
        img = img.resize(self.shape)
        return img, kwargs


class RandomBlur(Transformer):
    def __init__(self, min_radius, max_radius):
        self.min_radius = min_radius
        self.max_radius = max_radius

    def __call__(self, img: Image.Image, **kwargs):
        radius = random.uniform(self.min_radius, self.max_radius)
        smooth_img = img.filter(ImageFilter.GaussianBlur(radius))
        return smooth_img, kwargs


class RandomContrast(Transformer):
    def __init__(self, min_factor, max_factor):
        self.min_factor = min_factor
        self.max_factor = max_factor

    def __call__(self, img: Image.Image, **kwargs):
        factor = random.uniform(self.min_factor, self.max_factor)
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor), kwargs


class RandomColor(Transformer):
    def __init__(self, min_factor, max_factor):
        self.min_factor = min_factor
        self.max_factor = max_factor

    def __call__(self, img: Image.Image, **kwargs):
        factor = np.random.uniform(self.min_factor, self.max_factor)
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(factor), kwargs


class RandomBrightness(Transformer):
    def __init__(self, min_factor, max_factor):
        self.min_factor = min_factor
        self.max_factor = max_factor

    def __call__(self, img: Image.Image, **kwargs):
        factor = np.random.uniform(self.min_factor, self.max_factor)
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor), kwargs


class RandomRotate(Transformer):
    def __init__(self, min_degree: int, max_degree: int):
        self.min_degree = min_degree
        self.max_degree = max_degree

    def __call__(self, img: Image.Image, **kwargs):
        degree = random.uniform(self.min_degree, self.max_degree)
        img = img.rotate(degree)
        return img, kwargs
