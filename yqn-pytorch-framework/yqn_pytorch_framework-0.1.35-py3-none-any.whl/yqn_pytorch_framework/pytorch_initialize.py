import numpy as np
import torch
import torch.nn as nn

from yqn_pytorch_framework.device import cpu_device


def init_cnn_weight(cnn_layer, seed=2233):
    """初始化cnn层权重
    Args:
        cnn_layer: weight.size() == [nb_filter, in_channels, [kernel_size]]
        seed: int
    """
    filter_nums = cnn_layer.weight.size(0)
    kernel_size = cnn_layer.weight.size()[2:]
    scope = np.sqrt(2. / (filter_nums * np.prod(kernel_size)))
    torch.manual_seed(seed)
    nn.init.normal_(cnn_layer.weight, -scope, scope)
    cnn_layer.bias.data.zero_()


def init_cnn(cnn_layer, seed=2233):
    """初始化cnn层权重
    Args:
        cnn_layer: weight.size() == [nb_filter, in_channels, [kernel_size]]
        seed: int
    """
    filter_nums = cnn_layer.weight.size(0)
    kernel_size = cnn_layer.weight.size()[2:]
    scope = np.sqrt(2. / (filter_nums * np.prod(kernel_size)))
    torch.manual_seed(seed)
    nn.init.xavier_normal_(cnn_layer.weight)
    cnn_layer.bias.data.uniform_(-scope, scope)


def init_lstm_weight(lstm, num_layer=1, seed=2233):
    """初始化lstm权重
    Args:
        lstm: torch.nn.LSTM
        num_layer: int, lstm层数
        seed: int
    """
    for i in range(num_layer):
        weight_h = getattr(lstm, 'weight_hh_l{0}'.format(i))
        scope = np.sqrt(6.0 / (weight_h.size(0) / 4. + weight_h.size(1)))
        torch.manual_seed(seed)
        nn.init.uniform_(getattr(lstm, 'weight_hh_l{0}'.format(i)), -scope, scope)

        weight_i = getattr(lstm, 'weight_ih_l{0}'.format(i))
        scope = np.sqrt(6.0 / (weight_i.size(0) / 4. + weight_i.size(1)))
        torch.manual_seed(seed)
        nn.init.uniform_(getattr(lstm, 'weight_ih_l{0}'.format(i)), -scope, scope)

    if lstm.bias:
        for i in range(num_layer):
            weight_h = getattr(lstm, 'bias_hh_l{0}'.format(i))
            weight_h.data.zero_()
            weight_h.data[lstm.hidden_size: 2 * lstm.hidden_size] = 1
            weight_i = getattr(lstm, 'bias_ih_l{0}'.format(i))
            weight_i.data.zero_()
            weight_i.data[lstm.hidden_size: 2 * lstm.hidden_size] = 1


def init_linear(input_linear, seed=2233):
    """初始化全连接层权重
    """
    torch.manual_seed(seed)
    scope = np.sqrt(6.0 / (input_linear.weight.size(0) + input_linear.weight.size(1)))
    nn.init.uniform_(input_linear.weight, -scope, scope)
    # nn.init.uniform(input_linear.bias, -scope, scope)
    if input_linear.bias is not None:
        input_linear.bias.data.zero_()


def init_linear_weight_bias(input_linear, seed=2233):
    """
    :param input_linear:
    :param seed:
    :return:
    """
    torch.manual_seed(seed)
    nn.init.xavier_uniform_(input_linear.weight)
    scope = np.sqrt(6.0 / (input_linear.weight.size(0) + 1))
    if input_linear.bias is not None:
        input_linear.bias.data.uniform_(-scope, scope)


def init_embedding(input_embedding, seed=5566):
    """初始化embedding层权重
    """
    torch.manual_seed(seed)
    scope = np.sqrt(8.0 / input_embedding.size(1))
    nn.init.uniform_(input_embedding, -scope, scope)


def init_embed(input_embedding, seed=5566):
    """初始化embedding层权重
    """
    torch.manual_seed(seed)
    nn.init.xavier_uniform_(input_embedding)


def prepare_pack_padded_sequence(inputs_words, seq_lengths, device=cpu_device, descending=True):
    """
    :param device:
    :param inputs_words:
    :param seq_lengths:
    :param descending:
    :return:
    """
    sorted_seq_lengths, indices = torch.sort(seq_lengths, dim=0, descending=descending)
    if device != cpu_device:
        sorted_seq_lengths, indices = sorted_seq_lengths.cuda(), indices.cuda()
    _, sorted_indices = torch.sort(indices.view(indices.size(0)), descending=False)
    sorted_inputs_words = inputs_words[sorted_indices]
    return sorted_inputs_words, sorted_seq_lengths.cpu().numpy().reshape(-1), sorted_indices
