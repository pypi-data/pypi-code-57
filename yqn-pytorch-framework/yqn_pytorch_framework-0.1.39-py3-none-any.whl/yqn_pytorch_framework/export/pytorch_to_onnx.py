import torch

from yqn_pytorch_framework.device import tensor_load_device


def pytorch_to_onnx(model, device, pth_path, save_path, dummy_inputs, input_names, output_names):
    model = tensor_load_device(model, device).eval()
    checkpoint = torch.load(pth_path, map_location=device)
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    dynamic_dict = {}
    # for input_name in input_names:
    #     dynamic_dict[input_name] = {0: "batch_size"}
    # for output_name in output_names:
    #     dynamic_dict[output_name] = {0: "batch_size"}
    torch.onnx.export(model,
                      dummy_inputs,
                      save_path,
                      input_names=input_names,
                      output_names=output_names,
                      export_params=True,
                      # dynamic_axes=dynamic_dict,
                      verbose=True)
