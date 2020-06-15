import gc
import inspect

import numpy as np
import torch

from yqn_pytorch_framework.device import tensor_load_device


def read_frame(frame):
    func_name = frame.f_code.co_name
    filename = frame.f_globals["__file__"]
    if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
        filename = filename[:-1]
    module_name = frame.f_globals["__name__"]
    curr_line = frame.f_lineno
    return func_name, module_name, curr_line


def get_tensors():
    tensor_list = []
    for obj in gc.get_objects():
        try:
            if torch.is_tensor(obj) or (hasattr(obj, 'data') and torch.is_tensor(obj.data)):
                tensor = obj
            else:
                continue
            if tensor.is_cuda:
                tensor_list.append(tensor)
        except Exception as e:
            pass
            # print('A trivial exception occurred: {}'.format(e))
    return tensor_list


def load_current_tensor():
    tensor_list = get_tensors()
    tensor_size_list = [tensor.size() for tensor in tensor_list]
    tensor_sizes = {(type(x),
                     tuple(x.size()),
                     tensor_size_list.count(x.size()),
                     np.prod(np.array(x.size())) * 4 / 1000 ** 2) for x in tensor_list}
    return tensor_sizes


def _track_step(frame, device):
    import pynvml
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(device.index)
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    # func_name, module_name, curr_line = read_frame(frame)
    # where_str = module_name + ' ' + func_name + ':' + ' line ' + str(curr_line)
    mem_info_mb = mem_info.used / 1000 ** 2
    tensor_list_with_sizes = load_current_tensor()
    tensor_mem_size = 0
    for tensor in tensor_list_with_sizes:
        tensor_mem_size += tensor[3]
    pynvml.nvmlShutdown()
    return "", mem_info_mb, tensor_list_with_sizes, tensor_mem_size


def model_size_estimate(device, get_model):
    _gpu_real_trace_size(device, get_model)
    from yqn_pytorch_framework.model.base_model import BaseModel
    model = tensor_load_device(get_model(), device).eval()
    if isinstance(model, BaseModel):
        _model_size(model, model.get_default_input(), device)


def _gpu_real_trace_size(device, get_model):
    # print(torch.cuda.memory_summary(device))
    frame = inspect.currentframe()
    where_str, preheat_mem_info_mb, preheat_tensor_size, _ = _track_step(frame, device)
    dummy_tensor_1 = tensor_load_device(torch.randn(1, 10, 100, 100).float(), device)
    where_str, base_mem_info_mb, base_tensor_size, _ = _track_step(frame, device)
    # print(f"GPU Memory Track | {datetime.datetime.now():%d-%b-%y-%H:%M:%S} |"
    #       f" Total Used Memory:{base_mem_info_mb:<7.1f}Mb\n\n")
    model = tensor_load_device(get_model(), device).eval()
    where_str, after_model_mem_info_mb, after_model_tensor_sizes, _ = _track_step(frame, device)
    # for t, s, n, m in after_model_tensor_sizes - base_tensor_size:
    #     print(f'add     | {str(n)} * Size:{str(s):<20} | Memory: {str(m * n)[:6]} M | {str(t):<20}\n')
    # for t, s, n, m in base_tensor_size - after_model_tensor_sizes:
    #     print(f'release | {str(n)} * Size:{str(s):<20} | Memory: {str(m * n)[:6]} M | {str(t):<20}\n')
    # print(f"GPU Memory Track | {datetime.datetime.now():%d-%b-%y-%H:%M:%S} |"
    #       f" Total Used Memory:{after_model_mem_info_mb:<7.1f}Mb\n\n")
    print(f"{model._get_name()} GPU Frame {(after_model_mem_info_mb - base_mem_info_mb):<7.1f}Mb")
    print(torch.cuda.memory_summary(device))
    del model, dummy_tensor_1
    torch.cuda.empty_cache()


def _model_size(model, input_features, device, type_size=4):
    """
    数据占用
    参数占用
    :param model:
    :param input_features:
    :param type_size:
    :return:
    """
    frame = inspect.currentframe()
    model_name = model._get_name()
    with torch.no_grad():
        para = sum([np.prod(list(p.size())) for p in model.parameters()])
        print('{} Params Used: {:<7.1f}M'.format(model_name, para * type_size / 1000 / 1000))
        # if input_features is tuple:
        #     input_ = input_features.clone()
        #     input_.requires_grad_(requires_grad=False)
        # else:
        #     input_ = input_features.clone()
        #     input_.requires_grad_(requires_grad=False)

        where_str, preheat_mem_info_mb, preheat_tensor_list, preheat_tensor_size = _track_step(frame, device)
        where_str, base_mem_info_mb, base_tensor_list, base_tensor_size = _track_step(frame, device)
        result = model(input_features)
        where_str, after_model_mem_info_mb, after_model_tensor_list, after_model_tensor_size = _track_step(frame,
                                                                                                           device)

        print(f"{model_name} Variables Used {(after_model_mem_info_mb - base_mem_info_mb):<7.1f}Mb")
    print(torch.cuda.memory_summary(device))
    del model
    torch.cuda.empty_cache()

    # mods = list(model.compute_modules())
    # out_sizes = []
    #
    # for i in range(1, len(mods)):
    #     m = mods[i]
    #     if isinstance(m, nn.ReLU):
    #         if m.inplace:
    #             continue
    #     out = m(input_)
    #     out_sizes.append(np.array(out.size()))
    #     input_ = out
    #
    # total_nums = 0
    # for i in range(len(out_sizes)):
    #     s = out_sizes[i]
    #     nums = np.prod(np.array(s))
    #     total_nums += nums
    # print('{} : intermediates variables: {:3f} M (infer)'
    #       .format(model_name, total_nums * type_size / 1000 / 1000))
    # print('{} : intermediates variables: {:3f} M (train)'
    #       .format(model_name, total_nums * type_size * 2 / 1000 / 1000))
