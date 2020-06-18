# install minimal components
!pip install -q parallel_wavegan PyYaml unidecode ConfigArgparse g2p_en nltk
!git clone -q https://github.com/espnet/espnet.git
!cd espnet && git fetch && git checkout -b v.0.6.1 1e8b6ce88d57b53d1b60cbb3f306652468b0ab63


# download pretrained models
url_transformer = "https://drive.google.com/open?id=1Hh3iHmyMyiWxuljDPLXgDejTRj5Unv2f"
parallelwavegan_config = "https://drive.google.com/open?id=1eIgEuILooSJ7Mqo4LhILVVz6zdFCBBOV"
url_parallelwavegan = "https://drive.google.com/open?id=1fxfqVFhxAdZs4NLlysWKGxnPPbcLtjtM"
train_no_dev_units = "https://drive.google.com/open?id=1sKazNb43clsbpp4HsJpS7Mx0oyPCZIdc"
model_json = "https://drive.google.com/open?id=1D6yR5xVk0wgViu1WJkcDP8dc6H_oXpxH"
cidian = "https://drive.google.com/open?id=1rfgx40GrYjip65A1TDA7m-31Yb6SFUHt"

from guang.Utils.google import download
download(url_transformer)
download(url_parallelwavegan)
download(parallelwavegan_config)
download(train_no_dev_units)
download(model_json)
download(cidian)
print("\n sucessfully finished download.")

import os
# set path
dict_path = "/content/train_no_dev_units.txt"
model_path = "/content/model.last1.avg.best"
vocoder_path = "/content/checkpoint-500000steps.pkl"
vocoder_conf = "/content/parallel_wavegan.v1.yaml"

import sys
sys.path.append("espnet")
import torch
device = torch.device("cuda")

# define E2E-TTS model
from argparse import Namespace
from espnet.asr.asr_utils import get_model_conf
from espnet.asr.asr_utils import torch_load
from espnet.utils.dynamic_import import dynamic_import
idim, odim, train_args = get_model_conf(model_path)
model_class = dynamic_import(train_args.model_module)
model = model_class(idim, odim, train_args)
torch_load(model_path, model)
model = model.eval().to(device)
inference_args = Namespace(**{"threshold": 0.5, "minlenratio": 0.0, "maxlenratio": 10.0})

# define neural vocoder
import yaml
from parallel_wavegan.models import ParallelWaveGANGenerator
with open(vocoder_conf) as f:
    config = yaml.load(f, Loader=yaml.Loader)
vocoder = ParallelWaveGANGenerator(**config["generator_params"])
vocoder.load_state_dict(torch.load(vocoder_path, map_location="cpu")["model"]["generator"])
vocoder.remove_weight_norm()
vocoder = vocoder.eval().to(device)

from guang.Utils.jupyter import reload
from guang.Voice.txt2phone import py2ph
# define text frontend

with open(dict_path) as f:
    lines = f.readlines()

lines = [line.replace("\n", "").split(" ") for line in lines]
char_to_id = {c: int(i) for c, i in lines}

def frontend(text):
    """Clean text and then convert to id sequence."""
    idseq = []
    for i in py2ph(text):
        idseq += [char_to_id[i]]
    idseq += [idim - 1]  # <eos>
    return torch.LongTensor(idseq).view(-1).to(device)

import time
from IPython.display import display, Audio

input_text = input("pls input\n")

with torch.no_grad():
    start = time.time()
    x = frontend(input_text)
    c, _, _ = model.inference(x, inference_args)
    z = torch.randn(1, 1, c.size(0) * config["hop_size"]).to(device)
    c = torch.nn.ReplicationPad1d(
        config["generator_params"]["aux_context_window"])(c.unsqueeze(0).transpose(2, 1))
    y = vocoder(z, c).view(-1)
rtf = (time.time() - start) / (len(y) / config["sampling_rate"])
print(f"RTF = {rtf:5f}")

display(Audio(y.view(-1).cpu().numpy(), rate=config["sampling_rate"]))
