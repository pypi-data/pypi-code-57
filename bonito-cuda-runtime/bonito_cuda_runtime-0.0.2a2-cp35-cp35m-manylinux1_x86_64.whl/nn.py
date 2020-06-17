import torch
from collections import OrderedDict
from fast_ctc_decode import beam_search, viterbi_search
from torch.nn import Module, Sequential, Conv1d, BatchNorm1d, ReLU, Parameter
from bonito_cuda_runtime.lib import transform_depthwise_weights, transform_pointwise_weights
from bonito_cuda_runtime.lib import lib, block, empty, void_ptr, workspace, to_interleaved, from_interleaved


@torch.jit.script
def swish(x):
    return x * torch.sigmoid(x)


class Swish(Module):
    def forward(self, x):
        return swish(x)


Activations = [None, ReLU, Swish]


class CuModel(Module):

    def __init__(self, cfg, chunksize, weights=None):
        super().__init__()

        if 'qscore' not in cfg:
            self.qbias = 0.0
            self.qscale = 1.0
        else:
            self.qbias = cfg['qscore']['bias']
            self.qscale = cfg['qscore']['scale']
        self.alphabet = cfg['labels']['labels']
        self.alphabet = cfg['labels']['labels']
        self.stride = cfg['block'][0]['stride'][0]

        if chunksize % self.stride:
            raise RuntimeError('Chunksize should be divisable by stride')

        self.chunksize = chunksize // self.stride

        if cfg['encoder']['activation'] == 'relu':
            activation_idx = 1
        elif cfg['encoder']['activation'] == 'swish':
            activation_idx = 2
        else:
            raise RuntimeError('Unsupported Activation')

        # C1
        bcfg = cfg['block'][0]
        self.pre = Sequential(
            Conv1d(
                1, bcfg['filters'], bcfg['kernel'][0], stride=bcfg['stride'][0],
                padding=bcfg['kernel'][0]//2, bias=False
            ),
            BatchNorm1d(bcfg['filters']),
            Activations[activation_idx](),
        )

        # B1 - C2
        self.layers = Sequential(
            *[
                CuRepeatBlock(
                    bcfg['repeat'], cfg['block'][idx]['filters'], bcfg['filters'],
                    bcfg['kernel'][0], self.chunksize, activation_idx
                )
                for idx, bcfg in enumerate(cfg['block'][1:-1])
            ]
        )

        # C3
        lbcfg = cfg['block'][-2]
        bcfg = cfg['block'][-1]
        self.post = Sequential(
            Conv1d(lbcfg['filters'], bcfg['filters'], bcfg['kernel'][0], padding=bcfg['kernel'][0]//2, bias=False),
            BatchNorm1d(bcfg['filters']),
            Activations[activation_idx](),
        )

        self.decoder = Sequential(
            Conv1d(bcfg['filters'], len(self.alphabet), kernel_size=1, bias=True),
        )

        self.max_c = max(layer.max_c for layer in self.layers)
        self._transformed = False
        if weights: self.load_weights(weights)

    def decode(self, x, beamsize=5, threshold=1e-3, qscores=False, return_path=False):
        if beamsize == 1 or qscores:
            seq, path  = viterbi_search(x, self.alphabet, qscores, self.qscale, self.qbias)
        else:
            seq, path = beam_search(x, self.alphabet, beamsize, threshold)
        if return_path: return seq, path
        return seq

    def transform_weights(self):
        if self._transformed is False:
            for layer in self.layers:
                layer.transform_weights()
            self._transformed = True

    def forward(self, x):
        return self.forward_cuda(x)

    def forward_py(self, x):
        x = self.pre(x)
        x = self.layers(x)
        x = self.post(x)
        x = self.decoder(x)
        return torch.nn.functional.log_softmax(x.transpose(1, 2), dim=2)

    def forward_cuda(self, x):

        if self._transformed is False:
            self.transform_weights()

        x = self.pre(x)

        n, c, w = x.size()

        # zero pad any chunks smaller than chunksize and make batchsize divisible by 4
        if w < self.chunksize: # or n % 4:
            padded = torch.zeros(
                #(n + (4 - n % 4), c, self.chunksize),
                (n, c, self.chunksize),
                dtype=torch.float16, device=x.device
            )
            padded[:n, :, :w] = x
            x = padded

        n, c, w = x.size()

        x_in, p_x_in = to_interleaved(x)
        x_tmp, p_x_tmp = empty((n, self.max_c, w), x.device)
        x_out, p_x_out = empty((n, self.max_c, w), x.device)
        p_workspace = workspace(n, self.max_c, w, x.device, 0)

        for layer in self.layers:
            x_in = layer.forward_cuda(x_in, x_tmp, p_x_tmp, x_out, p_x_out, p_workspace)

        x = from_interleaved(x_in)[0]

        # buffers are oversize to the largest layer
        # reshape to the last layer in the group
        o = layer.layers[-1].pointwise.out_channels
        x = x.view(-1)[:n * o * w].view(n, o, w)

        x = self.post(x)
        x = self.decoder(x)
        return x.transpose(1, 2)

    def load_weights(self, weights):
        new_state_dict = OrderedDict()
        for ok, nw  in zip(weights.keys(), self.state_dict()):
            assert(ok.split('.')[-1] == nw.split('.')[-1])
            new_state_dict[nw] = weights[ok]
        self.load_state_dict(new_state_dict)


class CuRepeatBlock(Module):
    def __init__(self, repeat, in_channels, out_channels, kernel_size, chunk_size, activation_idx):
        super().__init__()

        self.pw_cfg = 0
        self.dw_cfg = 1 #if kernel_size < 50 else 0

        self.repeat = repeat
        self.chunk_size = chunk_size
        self.activation_idx = activation_idx

        self.layers = Sequential(
            CuBlock(
                in_channels, out_channels, kernel_size, chunk_size, activation_idx, pw_cfg=self.pw_cfg, dw_cfg=self.dw_cfg
            ),
            *[CuBlock(
                out_channels, out_channels, kernel_size, chunk_size, activation_idx,
                active=(not i == repeat - 2), pw_cfg=self.pw_cfg, dw_cfg=self.dw_cfg
            ) for i in range(repeat - 1)],
        )

        if repeat > 1:
            self.residual = Sequential(
                Conv1d(in_channels, out_channels, kernel_size=1, bias=False),
                BatchNorm1d(out_channels),
            )
            self.activation = self.layers[0].activation

        self.max_c = max(layer.pointwise.out_channels for layer in self.layers)
        self.max_k = max(layer.depthwise.kernel_size[0] for layer in self.layers)

    def transform_weights(self):
        for layer in self.layers:
            layer.transform_weights()

        if self.repeat > 1:
            pw = self.residual[0]
            bn = self.residual[1]
            pw.weight.data = transform_pointwise_weights(pw, self.pw_cfg)[0]

            bias = bn.bias.float()
            scale = bn.weight.float()
            mean = bn.running_mean.float()
            var = bn.running_var.float()

            bn.bias = Parameter((bias - (scale * mean) / torch.sqrt(var + 1e-5)).half())
            bn.weight = Parameter((scale / torch.sqrt(var + 1e-5)).half())

    def forward(self, x):
        if self.repeat > 1:
            return self.activation(self.layers(x) + self.residual(x))
        else:
            return self.layers(x)

    def forward_cuda(self, x_in, x_tmp, p_x_tmp, x_out, p_x_out, p_workspace):

        n, c, w = x_in.size()

        p_x_in = void_ptr(x_in)
        p_residual = p_x_in

        if w != self.chunk_size:
            raise RuntimeError("Width dimension does not match chunksize (%s!=%s)" % (w, self.chunk_size))

        if self.dw_cfg == 0 and w + self.max_k / 2 > 2048:
            raise RuntimeError("W + K/2 > 2048 (W=%s; K=%s; %s>2048)" % (w, self.max_k, w + self.max_k / 2))

        if self.dw_cfg == 1 and w + self.max_k * 2 > 6143:
            raise RuntimeError("W + K*2 > 6143 (W=%s; K=%s; %s>6143)" % (w, self.max_k, w + self.max_k * 2))

        for idx, layer in enumerate(self.layers, start=1):

            use_relu = int(self.repeat == 1 or idx < self.repeat) * self.activation_idx

            lib.runDepthwise(
                p_x_tmp,
                p_x_in,
                void_ptr(layer.depthwise.weight),
                n,
                w,
                layer.depthwise.in_channels,
                layer.depthwise.kernel_size[0],
                layer.depthwise.out_channels,
                self.dw_cfg
            )

            lib.run1x1ConvBiasBNReLu(
                p_x_out,
                p_x_tmp,
                void_ptr(layer.pointwise.weight),
                void_ptr(layer.bn.bias),
                void_ptr(layer.bn.weight),
                p_workspace,
                n,
                w,
                layer.pointwise.in_channels,
                1,
                layer.pointwise.out_channels,
                use_relu,
                self.pw_cfg,
            )

            p_x_in = p_x_out

        # no residual connection
        if self.repeat == 1: return x_out

        # forward on the residual connection
        lib.run1x1ConvBiasBNReLu(
            p_x_tmp,
            p_residual,
            void_ptr(self.residual[0].weight),
            void_ptr(self.residual[1].bias),
            void_ptr(self.residual[1].weight),
            p_workspace,
            n,
            w,
            self.residual[0].in_channels,
            1,
            self.residual[0].out_channels,
            False,
            self.pw_cfg,
        )

        return self.activation(x_out + x_tmp)


class CuBlock(Module):
    def __init__(self, in_channels, out_channels, kernel_size, chunk_size, activation_idx, active=True, dw_cfg=1, pw_cfg=0):
        super().__init__()

        if in_channels % 8 > 0 or out_channels % 8 > 0:
            raise ValueError("Channels must be divisable by 8")

        if kernel_size % 2 == 0:
            raise ValueError("Kernel size must be odd")

        if kernel_size > 256:
            raise ValueError("Kernel size must <= 256")

        if dw_cfg not in (0, 1):
            raise ValueError("Invalid depthwise config")

        if pw_cfg not in (0, 1, 2, 3, 4, 5, 6, 7):
            raise ValueError("Invalid pointwise config")

        self.dw_cfg = dw_cfg
        self.pw_cfg = pw_cfg

        self.depthwise = Conv1d(
            in_channels,
            in_channels,
            kernel_size=kernel_size,
            padding=(kernel_size // 2),
            groups=in_channels,
            bias=False,
        )

        self.chunk_size = chunk_size

        self.pointwise = Conv1d(
            in_channels, out_channels,
            kernel_size=1, bias=False
        )

        self.bn = BatchNorm1d(out_channels)

        self.active = active
        if self.active:
            self.activation = Activations[activation_idx]()

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        if self.active: x = self.activation(x)
        return x

    def transform_weights(self):
        """
        Transform weights performs two functions:

        1. Adjust Batchnorm bias and weight to incorporate variance and expectation values at inference
        2. transform depthwise and pointwise weights to interleaved fromat for improved performance
        """
        # Adjust Batchnorm scale and bias
        bias = self.bn.bias.float()
        scale = self.bn.weight.float()
        mean = self.bn.running_mean.float()
        var = self.bn.running_var.float()

        self.bn.bias = Parameter((bias - (scale * mean) / torch.sqrt(var + 1e-5)).half())
        self.bn.weight = Parameter((scale / torch.sqrt(var + 1e-5)).half())

        # Interleave pointwise and depthwise coefficient layouts
        self.depthwise.weight.data = transform_depthwise_weights(self.depthwise, self.chunk_size, self.dw_cfg)[0]
        self.pointwise.weight.data = transform_pointwise_weights(self.pointwise, self.pw_cfg)[0]

    def forward_cuda(self, x):
        return block(x, self, self.chunk_size, self.dw_cfg, self.pw_cfg)
