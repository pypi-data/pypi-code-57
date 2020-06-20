from .load_data import *
from .models import *
from .plotting import *
from .training import *

class Go():
    def __init__(self,device='cuda', trans=CIFAR10_AlbumTrans, dataset= CIFAR10DataLoader,
                batch_size= 128, model_name= CusResNet18):
        self.trans = trans
        self.dataset = dataset
        self.batch_size = batch_size
        self.model_name = model_name().to(device)

        transformation = self.trans()
        self.data = self.dataset(transformation, self.batch_size)

    def loaders(self):
        return self.data.get_loaders() 

    def display_samples(self, loader, n):
        return display(loader, n)

    def model(self):
        return self.model_name, model_summary(self.model_name)
    
