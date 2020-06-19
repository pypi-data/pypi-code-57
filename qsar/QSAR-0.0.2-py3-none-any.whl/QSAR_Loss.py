# implemented by modifying tensorflow code
# https://github.com/tensorflow/tensorflow/blob/r1.15/tensorflow/contrib/losses/python/metric_learning/metric_loss_ops.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.framework import tensor_shape
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import logging_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import script_ops
from tensorflow.python.ops import sparse_ops
from tensorflow.python.summary import summary


def pairwise_distance(feature, squared=False):
    """Computes the pairwise distance matrix with numerical stability.

    output[i, j] = || feature[i, :] - feature[j, :] ||_2

    :param feature: 2-D Tensor of size [number of data, feature dimension].
    :type feature: 2-D tensor
    :param squared: whether or not to square the pairwise distances, defaults to False
    :param squared: whether or not to square the pairwise distances, defaults to False
    :type squared: bool, optional
    :return: pairwise_distances
    :rtype: 2-D Tensor of size [number of data, number of data]
    """
    pairwise_distances_squared = math_ops.add(
        math_ops.reduce_sum(math_ops.square(feature), axis=[1], keepdims=True),
        math_ops.reduce_sum(
            math_ops.square(array_ops.transpose(feature)),
            axis=[0],
            keepdims=True)) - 2.0 * math_ops.matmul(feature,
                                                    array_ops.transpose(feature))

    # Deal with numerical inaccuracies. Set small negatives to zero.
    pairwise_distances_squared = math_ops.maximum(
        pairwise_distances_squared, 0.0)
    # Get the mask where the zero distances are at.
    error_mask = math_ops.less_equal(pairwise_distances_squared, 0.0)

    # Optionally take the sqrt.
    if squared:
        pairwise_distances = pairwise_distances_squared
    else:
        pairwise_distances = math_ops.sqrt(
            pairwise_distances_squared +
            math_ops.cast(error_mask, dtypes.float32) * 1e-16)

    # Undo conditionally adding 1e-16.
    pairwise_distances = math_ops.multiply(
        pairwise_distances,
        math_ops.cast(math_ops.logical_not(error_mask), dtypes.float32))

    num_data = array_ops.shape(feature)[0]
    # Explicitly set diagonals to zero.
    mask_offdiagonals = array_ops.ones_like(pairwise_distances) - array_ops.diag(
        array_ops.ones([num_data]))
    pairwise_distances = math_ops.multiply(
        pairwise_distances, mask_offdiagonals)
    return pairwise_distances


def masked_maximum(data, mask, dim=1):
    """Computes the axis wise maximum over chosen elements.

    :param data: input data, 2-D float `Tensor` of size [n, m].
    :type data: tensor
    :param mask: mask tensor, 2-D Boolean `Tensor` of size [n, m].
    :type mask: tensor
    :param dim: [The dimension over which to compute the maximum, defaults to 1
    :type dim: int, optional
    :return:     masked_maximums: N-D `Tensor`, the maximized dimension is of \
      size 1 after the operation.
    :rtype: tensor
    """
    axis_minimums = math_ops.reduce_min(data, dim, keepdims=True)
    masked_maximums = math_ops.reduce_max(
        math_ops.multiply(data - axis_minimums, mask), dim,
        keepdims=True) + axis_minimums
    return masked_maximums


def masked_minimum(data, mask, dim=1):
    """Computes the axis wise minimum over chosen elements.

    :param data: input data, 2-D float `Tensor` of size [n, m].
    :type data: tensor
    :param mask: mask tensor, 2-D Boolean `Tensor` of size [n, m].
    :type mask: tensor
    :param dim: [The dimension over which to compute the minimum, defaults to 1
    :type dim: int, optional
    :return:     masked_maximums: N-D `Tensor`, the minimized dimension is of \
      size 1 after the operation.
    :rtype: tensor
    """

    axis_maximums = math_ops.reduce_max(data, dim, keepdims=True)
    masked_minimums = math_ops.reduce_min(
        math_ops.multiply(data - axis_maximums, mask), dim,
        keepdims=True) + axis_maximums
    return masked_minimums


def triplet_semihard_loss(labels, embeddings, margin=1.0):
    """Computes the triplet loss with semi-hard negative mining.
    The loss encourages the positive distances (between a pair of embeddings with
    the same labels) to be smaller than the minimum negative distance among
    which are at least greater than the positive distance plus the margin constant
    (called semi-hard negative) in the mini-batch. If no such negative exists,
    uses the largest negative distance instead.
    See: https://arxiv.org/abs/1503.03832.

    :param labels: 1-D tf.int32 `Tensor` with shape [batch_size] of multiclass
      integer labels.
    :type labels: 1-D tf.int32 tensor
    :param embeddings: 2-D float `Tensor` of embedding vectors. Embeddings should
      be l2 normalized.
    :type embeddings: 2-D float tensor
    :param margin: margin term in the loss definition, defaults to 1.0
    :type margin: float, optional
    :return: triplet_loss
    :rtype: tf.float32 scalar
    """
    unknown = True

    # Reshape [batch_size] label tensor to a [batch_size, 1] label tensor.
    lshape = array_ops.shape(labels)
    #assert lshape.shape == 1
    labels = array_ops.reshape(labels, [lshape[0], 1])

    # Build pairwise squared distance matrix.
    pdist_matrix = pairwise_distance(embeddings, squared=True)
    # Build pairwise binary adjacency matrix.
    adjacency = math_ops.equal(labels, array_ops.transpose(labels))
    # Invert so we can select negatives only.
    adjacency_not = math_ops.logical_not(adjacency)

    batch_size = array_ops.size(labels)

    # Compute the mask.
    pdist_matrix_tile = array_ops.tile(pdist_matrix, [batch_size, 1])
    mask = math_ops.logical_and(
        array_ops.tile(adjacency_not, [batch_size, 1]),
        math_ops.greater(
            pdist_matrix_tile, array_ops.reshape(
                array_ops.transpose(pdist_matrix), [-1, 1])))
    mask_final = array_ops.reshape(
        math_ops.greater(
            math_ops.reduce_sum(
                math_ops.cast(mask, dtype=dtypes.float32), 1, keepdims=True),
            0.0), [batch_size, batch_size])
    mask_final = array_ops.transpose(mask_final)

    adjacency_not = math_ops.cast(adjacency_not, dtype=dtypes.float32)
    mask = math_ops.cast(mask, dtype=dtypes.float32)

    # negatives_outside: smallest D_an where D_an > D_ap.
    negatives_outside = array_ops.reshape(
        masked_minimum(pdist_matrix_tile, mask), [batch_size, batch_size])
    negatives_outside = array_ops.transpose(negatives_outside)

    # negatives_inside: largest D_an.
    negatives_inside = array_ops.tile(
        masked_maximum(pdist_matrix, adjacency_not), [1, batch_size])
    semi_hard_negatives = array_ops.where(
        mask_final, negatives_outside, negatives_inside)

    loss_mat = math_ops.add(margin, pdist_matrix - semi_hard_negatives)

    if unknown:
        bool_mask = math_ops.not_equal(labels, 0)
        mask_unknown = math_ops.cast(bool_mask, dtype=dtypes.float32)
        loss_mat = array_ops.transpose(math_ops.multiply(
            mask_unknown, array_ops.transpose(math_ops.multiply(loss_mat, mask_unknown))))

    mask_positives = math_ops.cast(
        adjacency, dtype=dtypes.float32) - array_ops.diag(
            array_ops.ones([batch_size]))

    # In lifted-struct, the authors multiply 0.5 for upper triangular
    #   in semihard, they take all positive pairs except the diagonal.
    num_positives = math_ops.reduce_sum(mask_positives)

    triplet_loss = math_ops.truediv(
        math_ops.reduce_sum(
            math_ops.maximum(
                math_ops.multiply(loss_mat, mask_positives), 0.0)),
        num_positives,
        name='triplet_semihard_loss')

    return triplet_loss
