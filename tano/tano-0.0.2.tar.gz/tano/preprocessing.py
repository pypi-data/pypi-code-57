from PIL import Image
from torchvision.transforms import functional as TF
import torch


def path_to_tensor(image_path, resize=False, height=0, width=0):
    """Returns Pytorch Image Tensor given path to Image"""
    image = Image.open(image_path).convert('RGB')
    if resize:
        image = TF.resize(image, (height, width))
    image = TF.to_tensor(image)
    image = torch.unsqueeze(image, dim=0)
    return image
