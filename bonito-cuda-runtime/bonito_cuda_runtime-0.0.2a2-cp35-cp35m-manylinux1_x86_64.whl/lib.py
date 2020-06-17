"""
Python Interface around the CFFI binding
"""

import torch
from _runtime import lib, ffi



def void_ptr(x):
    """
    Return a void * for given Tensor `x`
    """
    return ffi.cast("void *", x.data_ptr())


def empty(size, device):
    """
    Create an empty Tensor of size `size` on device `device`
    """
    x = torch.empty(size, dtype=torch.float16, device=device)
    return x, void_ptr(x)


def workspace(n, c, w, device, cfg=0):
    """
    Return a void * for a workspace buffer
    """
    workspace_size = lib.get1x1ConvBiasBNReLuWorkspaceSize(n, w, c, 1, c, cfg)
    workspace = torch.empty(workspace_size, dtype=torch.float16, device=device)
    return void_ptr(workspace)


def to_interleaved(x):
    """
    Transform a NCW Tensor to the interleaved format
    """
    n, c, w = x.size()
    p_in = void_ptr(x)
    out, p_out = empty((n, c, w), x.device)
    lib.transformNCHWToInterleaved(p_out, p_in, n, w, c)
    return out, p_out


def from_interleaved(x):
    """
    Transform interleaved format to a NCW Tensor
    """
    n, c, w = x.size()
    p_in = void_ptr(x)
    out, p_out = empty((n, c, w), x.device)
    lib.transformInterleavedToNCHW(p_out, p_in, n, w, c)
    return out, p_out


def _transform_weights(layer, cfg, t, chunk_size):

    c = layer.in_channels
    o = layer.out_channels
    k = layer.kernel_size[0]

    w = layer.weight
    p_w = void_ptr(w)
    out, p_out = empty(w.size(), w.device)
    w_tmp, p_w_tmp = empty(w.size(), w.device)

    if t == 0:
        lib.transformNCHWToInterleaved(p_w_tmp, p_w, c, k, o)
        lib.transformPointwiseWeights(p_out, p_w_tmp, c, k, o, cfg)
    elif t == 1:
        lib.transformNCHWToInterleaved(p_w_tmp, p_w, 1, k, o)
        lib.transformDepthwiseWeights(p_out, p_w_tmp, c, k, o, chunk_size, cfg)
    else:
        raise ValueError("unknown value t=%s" % t)

    return out, p_out


def transform_pointwise_weights(layer, chunk_size, cfg=0):
    assert(layer.kernel_size[0] == 1)
    return _transform_weights(layer, cfg, 0, chunk_size)


def transform_depthwise_weights(layer, chunk_size, cfg=0):
    assert(layer.out_channels == layer.groups)
    return _transform_weights(layer, cfg, 1, chunk_size)


def depthwise(x, blk, chunk_size, cfg=0, transform_weights=True):

    n, c, w = x.size()

    x_interleave, p_x_interleave = to_interleaved(x)
    x_out, p_x_out = empty((n, c, w), x.device)

    if transform_weights:
        dw_trans, p_dw_trans = transform_depthwise_weights(blk.depthwise, chunk_size=chunk_size, cfg=cfg)
    else:
        p_dw_trans = void_ptr(blk.depthwise.weight)

    lib.runDepthwise(
        p_x_out,
        p_x_interleave,
        p_dw_trans,
        n,
        w,
        blk.depthwise.in_channels,
        blk.depthwise.kernel_size[0],
        blk.depthwise.out_channels,
        cfg
    )

    return from_interleaved(x_out)[0]


def fused_conv_bn_relu(x, blk, chunk_size, cfg=0, transform_weights=True, use_relu=True, residual_input=None):

    if (residual_input is not None) and use_relu:
        raise NotImplementedError("Residual input can only be used with ReLU deactivated")

    n, c, w = x.size()

    x_interleaved, p_x_interleaved = to_interleaved(x)
    x_out, p_x_out = empty((n, c, w), x.device)

    # transformed conv weights
    if transform_weights:
        pw_trans, p_pw_trans = transform_pointwise_weights(blk.pointwise, chunk_size, cfg=cfg)
    else:
        p_pw_trans = void_ptr(blk.pointwise.weight)

    lib.run1x1ConvBiasBNReLu(
        p_x_out,
        p_x_interleaved,
        p_pw_trans,
        void_ptr(blk.bn.bias),
        void_ptr(blk.bn.weight),
        workspace(n, c, w, x.device),
        n,
        w,
        blk.pointwise.in_channels,
        blk.pointwise.kernel_size[0],
        blk.pointwise.out_channels,
        int(use_relu),
        cfg,
    )

    # interleave the residual input
    if residual_input is not None:
        residual_input_interleaved, _ = to_interleaved(residual_input)
        x_out += residual_input_interleaved

    return from_interleaved(x_out)[0]


def block(x, blk, chunk_size, dw_cfg, pw_cfg):
    x = depthwise(x, blk, chunk_size, dw_cfg, transform_weights=False)
    x = fused_conv_bn_relu(x, blk, chunk_size, pw_cfg, transform_weights=False)
    return x
