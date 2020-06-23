# -*- coding:utf-8 -*-
# @author :adolf
from torch import nn
import torch.onnx
from rpa_ocr.Identify_English.crnn_model import CRNN


def convert_model(torch_model, model_path):
    torch_model.load_state_dict(torch.load(model_path, map_location="cpu"))
    torch_model.eval()
    # x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)
    x = torch.randn(1, 1, 32, 85).to('cpu')

    torch.onnx.export(
        torch_model,
        x,
        "crnn.onnx",
        export_params=True,
        verbose=False,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input":
                {
                    0: "batch_size", 3: "w"
                },
            "output": {
                0: "batch_size"
            }
        }
    )


torchmodel = CRNN(imgH=32, nc=1, nclass=63, nh=256)
convert_model(torch_model=torchmodel, model_path='rpa_ocr/model/custom_verification.pth')
