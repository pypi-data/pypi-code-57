import collections

from torch import nn


class TextCNNConv(nn.Module):
    """
    Convolution Block
    """

    def __init__(self, in_ch, out_ch, kernel_size):
        super(TextCNNConv, self).__init__()
        self.conv = nn.Sequential(collections.OrderedDict([
            ('text_cnn_conv_1', nn.Conv1d(in_ch, out_ch, kernel_size=kernel_size, bias=True)),
            ('text_cnn_relu_1', nn.ReLU(inplace=True)),
        ]))

    def forward(self, x):
        _out = self.conv(x)
        return _out
