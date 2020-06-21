from ..model import ALL_TASK_MODEL_PATHS
from ..transformersx_base import *


@configclass
class FastTaskArguments:
    task_name: str = field('default', 'input the task name')
    data_dir: str = field("", "the data directory for train,eval,test,label")
    model_finetuned_dir: str = field("/app/models/finetuning",
                                     "The 'model_base_dir' generally is for the finetuned models."
                                     "Generally, the model is loaded from 'model_finetuned_dir' firstly."
                                     " If the model cannot be found, it will be loaded from the model_pretrained_dir.")

    model_pretrained_dir: str = field("/app/models/pretrained",
                                      "This folder is for the pretrained models downloaded from Internet.")
    model_name: str = field("bert-base-chinese", "the name of model: " + str(ALL_TASK_MODEL_PATHS))
