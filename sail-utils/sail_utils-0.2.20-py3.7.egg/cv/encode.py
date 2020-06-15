# -*- coding: utf-8 -*-
"""
module for encoders
"""

import cv2
import numpy as np

from sail_utils import LOGGER


def _run_in_batches(func, data_dict, out, batch):
    data_len = len(out)
    num_batches = int(data_len / batch)

    start, end = 0, 0
    for i in range(num_batches):
        start, end = i * batch, (i + 1) * batch
        batch_data_dict = {k: v[start:end] for k, v in data_dict.items()}
        out[start:end] = func(batch_data_dict)
    if end < len(out):
        batch_data_dict = {k: v[end:] for k, v in data_dict.items()}
        out[end:] = func(batch_data_dict)


class ImageEncoder:
    """
    image encoding class
    """

    def __init__(self,
                 checkpoint: str,
                 input_name: str = "images",
                 output_name: str = "features"):
        import tensorflow as tf

        self._session = tf.Session()
        with tf.gfile.GFile(checkpoint, 'rb') as f_handle:
            graph = tf.GraphDef()
            graph.ParseFromString(f_handle.read())

        tf.import_graph_def(graph, name='net')
        self._input = tf.get_default_graph().get_tensor_by_name("net/%s:0" % input_name)
        self._output = tf.get_default_graph().get_tensor_by_name("net/%s:0" % output_name)

        self._feature_dim = self._output.get_shape().as_list()[-1]
        self._image_shape = self._input.get_shape().as_list()[1:]

    @property
    def image_shape(self):
        """
        get image shape required for the net
        :return:
        """
        return self._image_shape

    def encode(self, data_x, batch=32):
        """
        encode detection results
        :param data_x:
        :param batch:
        :return:
        """
        out = np.zeros((len(data_x), self._feature_dim), np.float32)
        _run_in_batches(
            lambda x: self._session.run(self._output, feed_dict=x),
            {self._input: data_x}, out, batch)
        return out


def _extract_image_patch(image, bbox, patch_shape):
    """Extract image patch from bounding box.

    Parameters
    ----------
    image : ndarray
        The full image.
    bbox : array_like
        The bounding box in format (x, y, width, height).
    patch_shape : Optional[array_like]
        This parameter can be used to enforce a desired patch shape
        (height, width). First, the `bbox` is adapted to the aspect ratio
        of the patch shape, then it is clipped at the image boundaries.
        If None, the shape is computed from :arg:`bbox`.

    Returns
    -------
    ndarray | NoneType
        An image patch showing the :arg:`bbox`, optionally reshaped to
        :arg:`patch_shape`.
        Returns None if the bounding box is empty or fully outside of the image
        boundaries.

    """
    bbox = np.array(bbox)
    if patch_shape is not None:
        # correct aspect ratio to patch shape
        target_aspect = float(patch_shape[1]) / patch_shape[0]
        new_width = target_aspect * bbox[3]
        bbox[0] -= (new_width - bbox[2]) / 2
        bbox[2] = new_width

    # convert to top left, bottom right
    bbox[2:] += bbox[:2]
    bbox = bbox.astype(np.int)

    # clip at image boundaries
    bbox[:2] = np.maximum(0, bbox[:2])
    bbox[2:] = np.minimum(np.asarray(image.shape[:2][::-1]) - 1, bbox[2:])
    if np.any(bbox[:2] >= bbox[2:]):
        return None
    s_x, s_y, e_x, e_y = bbox
    image = image[s_y:e_y, s_x:e_x]
    image = cv2.resize(image, tuple(patch_shape[::-1]))
    return image


def create_box_encoder(model_filename, input_name="images",
                       output_name="features", batch_size=32):
    """
    wrapper to create bounding box encoder
    :param model_filename:
    :param input_name:
    :param output_name:
    :param batch_size:
    :return:
    """
    image_encoder = ImageEncoder(model_filename, input_name, output_name)
    image_shape = image_encoder.image_shape

    def encoder(image, boxes):
        image_patches = []
        for box in boxes:
            patch = _extract_image_patch(image, box, image_shape[:2])
            if patch is None:
                LOGGER.warning("WARNING: Failed to extract image patch: %s." % str(box))
                patch = np.random.uniform(
                    0., 255., image_shape).astype(np.uint8)
            image_patches.append(patch)
        image_patches = np.asarray(image_patches)
        return image_encoder.encode(image_patches, batch_size)
    return encoder
