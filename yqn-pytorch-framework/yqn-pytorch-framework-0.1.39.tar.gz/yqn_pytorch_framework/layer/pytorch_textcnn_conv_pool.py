from torch import nn

from yqn_pytorch_framework.layer.pytorch_textcnn_conv import TextCNNConv


class TextCNNConvPoolBlock(nn.Module):
    """
    Convolution Block
    """

    def __init__(self, sentence_length, out_ch, kernel_size):
        super(TextCNNConvPoolBlock, self).__init__()
        max_pool_kernel = sentence_length - kernel_size + 1
        self.conv = TextCNNConv(sentence_length, out_ch, kernel_size)
        self.max_pool = nn.MaxPool1d(kernel_size=max_pool_kernel)

    def forward(self, x):
        _out = self.conv(x)
        _out_pool = self.max_pool(_out)
        return _out_pool
