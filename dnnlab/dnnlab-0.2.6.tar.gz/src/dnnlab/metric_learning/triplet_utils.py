# Copyright 2019 Kevin Hirschmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import tensorflow as tf 
import cv2 
import matplotlib.pyplot as plt


def construct_mined_triplets(inputs, ap_indices, an_indices):
    """
    Construct the mined triplets which are used for (Online) TripletLoss.

    Args:
        inputs (tf.tensor): inputs of the original TripletNet
        ap_indices (tf.tensor): indices [batch_size, 2] of anchor-positive pairs of mined triplets (will be set during training of TripletNet)
        an_indices (tf.tensor): indices [batch_size, 2] of anchor-negative pairs of mined triplets (will be set during training of TripletNet)

    Returns:
        selected_triplets (tf.tensor): 5D-tensor [batch_size, 3, h, w, c] containing each mined/selected triplet 
    """
    b, h, w, c = inputs.shape

    selected_triplets = tf.TensorArray(tf.float32, size=b)

    for i in range(inputs.shape[0]):
        triplet_ta = tf.TensorArray(tf.float32, size=3) # tf.TensorArray for a single triplet

        anchor_index = ap_indices[i][0]
        pos_index = ap_indices[i][1]
        neg_index = an_indices[i][1]
            
        anchor = inputs[anchor_index]
        positive = inputs[pos_index]
        negative = inputs[neg_index]

        # Workaround for: tf.EagerTensor object does not support item assignment
        # use tf.TensorArray and tf.stack to fake correct tensor assignment
        triplet_ta = triplet_ta.write(0, anchor)
        triplet_ta = triplet_ta.write(1, positive)
        triplet_ta = triplet_ta.write(2, negative)

        triplet_ta = triplet_ta.stack() # stack array, result is a tensor [3, h, w, c]

        # add current Triplet to selected Triplet TensorArray
        selected_triplets = selected_triplets.write(i, triplet_ta)

    selected_triplets = selected_triplets.stack() # stack array, result is a tensor [batch_size, 3, h, w, c]
        
    return selected_triplets



def create_heatmap(image):
    """create heatmap of the activations of an image.

    Arg:
        image (tf.tensor): tensor of a single image

    Return:
        heatmap (tf.tensor): heatmap of image activation
    """
    normalized = image / tf.reduce_max(image)
    normalized = tf.maximum(normalized, 0)

    # apply cv2 Color Map - cv2.COLORMAP_JET
    # normalized = tf.multiply(normalized, tf.subtract(1.0, normalized))
    normalized = normalized * (1.0 - normalized)
    normalized = tf.cast(normalized, dtype=tf.uint8)
    heatmap = cv2.applyColorMap(normalized.numpy(), cv2.COLORMAP_JET)
    return heatmap



def add_heatmap_to_image(orig_images, masked_images, attention_maps):
    """ draw images with similiarity heatmaps for tensorboard

    Args:
        orig_images (tf.tensor): 4-d tensor of a triplet containing anchor, positive and negative of the original images
        masked_images (tf.tensor): 4-d tensor of a triplet containing anchor, positive and negative of the masked images
        attention_maps (tuple(tf.tensor, tf.tensor, tf.tensor)): corresponding attention_maps for anchor, positive and negative 

    Return:
        anchor_att (tf.tensor): anchor image with overlying attention heatmap
        positive_att (tf.tensor): positive image with overlying attention heatmap
        negative_att (tf.tensor): negative image with overlying attention heatmap
    """

    # cast to tf.py_function to be able to use type np.float which is equivalent to type cv.Mat
    heatmap_anchor = tf.py_function(func=create_heatmap, inp=[attention_maps[0]], Tout=tf.float32)
    heatmap_positive = tf.py_function(func=create_heatmap, inp=[attention_maps[1]], Tout=tf.float32)
    heatmap_negative = tf.py_function(func=create_heatmap, inp=[attention_maps[2]], Tout=tf.float32)

    anchor_att = masked_images[0] * 0.7 + heatmap_anchor / 255 * 0.3
    positive_att = masked_images[1] * 0.7 + heatmap_positive / 255 * 0.3
    negative_att = masked_images[2] * 0.7 + heatmap_negative / 255 * 0.3

        
    return anchor_att, positive_att, negative_att