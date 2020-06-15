from collections import Counter
from io import BytesIO
from typing import Tuple, Union, Optional

import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans, MeanShift


def dec_to_hex(dec: int) -> str:
    return hex(dec)[2:].rjust(2, '0')


def arr_to_color_code(arr: np.array) -> str:
    return '#' + ''.join(map(dec_to_hex, arr))


def kmeans_dominant(samples: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Detects dominant colors using Mini Batch K-Means algorithm.
    """
    #kmeans = MiniBatchKMeans(n_clusters=k)
    kmeans = MeanShift()
    kmeans.fit(samples)

    dominants = kmeans.cluster_centers_.astype(samples.dtype)
    labels = kmeans.labels_

    counter = Counter(labels)

    most_common = counter.most_common(k)
    colors = dominants[list(map(lambda t: t[0], most_common))]
    counts = np.array(list(map(lambda t: t[1], most_common)))
    percentages = counts / counts.sum()

    return colors, percentages


def detect_colors(image: Union[str, BytesIO, Image], k: int = 5, downsample_to: Optional[Tuple[int, int]] = (512, 512)) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Detects dominant color of an image Mini Batch K-Means.
    @image_path: path to the source image
    @k: number of colors to detect
    @downsample_to: maximum size for image to be downsampled to
    """
    if type(image) is not Image:
        img = Image.open(image)
    else:
        img = image
    if downsample_to:
        img.thumbnail(downsample_to, Image.LANCZOS)

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    im = np.array(img)
    im = im[im[:, :, 3] > 128]
    im = im[:, :3]

    colors, counts = kmeans_dominant(im, k)
    return np.array(list(map(lambda c: arr_to_color_code(c), colors))), counts
