# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Data Augmentations for object detection."""

import logging
import torch
import random
import torchvision.transforms.functional as functional

logger = logging.getLogger(__name__)


def hflip(image, boxes):
    """
    Flip image horizontally.

    :param image: image
    :type image: PIL Image
    :param boxes: bounding boxes in (x_min, y_min, x_max, y_max)
    :type boxes: tensor (n_objects, 4)
    :return: flipped image, updated bounding boxes
    :rtype: PIL Image, tensor
    """
    new_image = functional.hflip(image)

    new_boxes = boxes
    new_boxes[:, [0, 2]] = image.width - boxes[:, [2, 0]]

    return new_image, new_boxes


def expand(image, boxes):
    """
    Expand image and fill the surrounding space with the mean of ImageNet.
    This is intended to detect smaller objects.

    :param image: image
    :type image: PIL Image
    :param boxes: bounding boxes in (x_min, y_min, x_max, y_max)
    :type boxes: tensor (n_objects, 4)
    :return: expanded image, new boxes
    :rtype: PIL Image, tensor
    """
    imagenet_mean = [0.485, 0.456, 0.406]

    tensor_image = functional.to_tensor(image)
    depth, height, width = tensor_image.size()

    ratio = random.uniform(1, 2)
    new_height = int(height * ratio)
    new_width = int(width * ratio)
    top = random.randint(0, new_height - height)
    left = random.randint(0, new_width - width)

    # place a image in a larger mean image
    new_image = torch.ones((3, new_height, new_width), dtype=torch.float)
    new_image[:, :, :] *= torch.FloatTensor(imagenet_mean).unsqueeze(1).unsqueeze(2)
    new_image[:, top:top + height, left:left + width] = tensor_image

    new_boxes = boxes
    new_boxes[:, :2] += torch.FloatTensor([left, top])
    new_boxes[:, 2:] += torch.FloatTensor([left, top])

    new_image = functional.to_pil_image(new_image)

    return new_image, new_boxes


def random_crop_around_bbox(image, boxes):
    """
    Randomly crop image but include all the bounding boxes.

    :param image: image
    :type image: PIL Image
    :param boxes: bounding boxes in (x_min, y_min, x_max, y_max)
    :type boxes: tensor (n_objects, 4)
    :return: expanded image, new boxes
    :rtype: PIL Image, tensor
    """
    tensor_image = functional.to_tensor(image)
    depth, height, width = tensor_image.size()

    x_min = int(torch.min(boxes[:, 0]))
    y_min = int(torch.min(boxes[:, 1]))
    x_max = int(torch.max(boxes[:, 2]))
    y_max = int(torch.max(boxes[:, 3]))
    # make sure box coordinates are within the size of image
    box_w = min(x_max - x_min, width)
    box_h = min(y_max - y_min, height)

    # bypass in case of negative bbox coordinates
    if any(coord < 0 for coord in [x_min, y_min, box_w, box_h]):
        logger.warning("Due to negative bbox coordinates, no random_crop_around_bbox will be applied")
        return image, boxes

    max_trials = 50
    for _ in range(max_trials):

        new_w = random.randint(box_w, width)
        new_h = random.randint(box_h, height)

        # retry if image size is too small or aspect_ratio is way off
        aspect_ratio = new_h / new_w
        if new_h * new_w < height * width * 0.6 or not 0.5 < aspect_ratio < 2:
            continue

        left = random.randint(0, min(width - new_w, x_min))
        right = left + new_w
        top = random.randint(0, min(height - new_h, y_min))
        bottom = top + new_h
        crop = torch.FloatTensor([left, top, right, bottom])

        # crop image
        new_image = tensor_image[:, top:bottom, left:right]

        # adjust bbox
        new_boxes = boxes
        new_boxes[:, :2] -= crop[:2]
        new_boxes[:, 2:] -= crop[:2]

        new_image = functional.to_pil_image(new_image)

        return new_image, new_boxes

    return image, boxes


def spatial_level_transforms(image, boxes, prob):
    """
    Apply various spatial change of both an input image and bounding boxes in an random order.
    Support expand, hflip and random_crop_around_bbox.

    :param image: image
    :type image: PIL Image
    :param boxes: bounding boxes in (x_min, y_min, x_max, y_max)
    :type boxes: tensor (n_objects, 4)
    :param prob: target probability of applying each of data augmentations
    :type prob: float
    :return: augmented image, boxes
    :rtype: PIL image, tensor
    """
    new_image = image
    new_boxes = boxes

    if random.random() < prob:
        if random.random() < prob:
            new_image, new_boxes = random_crop_around_bbox(new_image, new_boxes)
        else:
            new_image, new_boxes = expand(new_image, new_boxes)

    if random.random() < prob:
        new_image, new_boxes = hflip(new_image, new_boxes)

    return new_image, new_boxes


def transform(image, boxes, is_train, prob):
    """
    Apply data augmentations for Object Detection.

    :param image: image
    :type image: PIL Image
    :param boxes: bounding boxes in (x_min, y_min, x_max, y_max)
    :type boxes: tensor (n_objects, 4)
    :param is_train: which mode (training, inferencing) is the network in?
    :type is_train: boolean
    :param prob: target probability of applying each of data augmentations
    :type prob: float
    :return: augmented image, boxes, areas, image height, image width
    :rtype: PIL image, tensor, list, int, int
    """
    new_image = image
    new_boxes = boxes

    if is_train:
        new_image, new_boxes = spatial_level_transforms(new_image, new_boxes, prob)

    new_height = new_image.height
    new_width = new_image.width
    new_image = functional.to_tensor(new_image)
    # update the areas of bbox for mAP calculation for each object group based on the size of objects
    new_areas = ((new_boxes[:, 2] - new_boxes[:, 0]) * (new_boxes[:, 3] - new_boxes[:, 1])).tolist()

    return new_image, new_boxes, new_areas, new_height, new_width
