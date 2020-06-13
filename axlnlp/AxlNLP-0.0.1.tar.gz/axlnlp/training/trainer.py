#basic
import os
import copy

#torch
import torch

#pytorch lightning 
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning import Trainer as PLTrainer
#pytorch_lightning.loggers

#am
#from am.modules.ml.custom_loggers import CustomCometLogger

# am general
from axlnlp import get_logger
from axlnlp.utils import timer
#from am.config import COMET_API_KEY, COMET_WORKSPACE

#set up logger
logger = get_logger(__name__)

#self.model = self.__setup_ml_model()

# if self.cv:
#     self.n_fold = self.dataset._n_folds


# def __setup_ml_model(self):

#     model = get_model(self.params["model_name"])(  
#                                                     dataset=self.dataset,
#                                                     embeddings=self.embeddings, 
#                                                     params=self.params,
#                                                 )
    
#     return model

# def __cv_train(self):
#     for cv_id in range(self.n_folds):
#         logger.info("Starting Training CV: {}/{}".format(self.model.split_id, self.n_folds))

#         self.pyto_trainer.fit(self.model)

#         # break if we are just testing to overfit on small amount of the data
#         if self.params["of_percent"]:
#             break
        
#         # we reset the model
#         self.model = self.__setup_ml_model(
#                                             params=self.params, 
#                                             dataset=self.dataset, 
#                                             embeddings=self.embeddings
#                                             )

#     if not self.params["of_percent"]:
#        self.exp_logger.log_average_metrics()



class Trainer:

    """
    GPU,
    logger,
    save dir
    of_percent
    checkpoint loader

    """
    def __init__(self, 
                        hyperparams:dict, 
                        gpu:int=None,
                        of_percent:float=None,
                        model_save_path:str=None,
                        model_load_path:str=None,
                        monitor:str="val_mean_task_f1",
                        logger=None
                        ):
        self.gpu = gpu
        self.of_percent = of_percent
        self.model_save_path = model_save_path
        self.model_load_path = model_load_path
        self.hyperparams = hyperparams
        self.monitor = monitor
        self.logger = logger
        self.gpu_available, self.device = self.__check_gpu()
        self.exp_logger = self.__setup_exp_logger()
        self.pyto_trainer = self.__setup_pyto_trainer()


    def __check_gpu(self):
        gpu_available = torch.cuda.is_available()
        device = torch.device(f'cuda:{self.gpu}' if gpu_available and isinstance(self.gpu,int) else 'cpu')
        logger.info("----------------------")
        logger.info(f"nr GPUs found: {torch.cuda.device_count()}")

        if "cuda" in str(device):
            logger.info(f"Will use GPU number: {self.gpu}")
        else:
            logger.info("will use CPU")
        logger.info("----------------------")
        return gpu_available, device


    def __setup_exp_logger(self):

        if self.logger == "comet":
            exp_logger = CustomCometLogger(
                                            api_key=COMET_API_KEY, #"VMe0Q2GYAEwwpImCpIqwU1X4a", 
                                            project_name=self.params["comet_project_name"], 
                                            workspace=COMET_WORKSPACE,
                                            experiment_name=self.params["experiment_name"],
                                            cv=self.cv
                                            )
            exp_logger.log_hyperparams(self.hyperparams)
        else:
            logger.warning(f"No logger will be used")
            exp_logger = False

        return exp_logger
    

    def __setup_pyto_trainer(self):

        checkpoint_callback = False
        if self.model_save_path:

            #dir_path = os.path.join(self.params["save_location"], self.params["dataset"], "_".join(self.params["subtasks"]), self.params["model_name"])
            
            if not os.path.exists(self.model_save_path):
                os.makedirs(self.model_save_path)

            checkpoint_callback = ModelCheckpoint(
                                                    filepath=os.path.join(self.model_save_path, '{val_mean_task_f1:.2f}'),
                                                    save_top_k=True,
                                                    verbose=True,
                                                    monitor=self.monitor,
                                                    mode='min' if "loss" in self.monitor else "max",
                                                    prefix=self.params["experiment_name"].replace(".","")
                                                    )

        #early stopping
        earlystopping = False
        if self.hyperparams["patience"]:
            earlystopping = EarlyStopping(
                                            monitor=self.monitor, 
                                            patience=self.hyperparams["patience"],
                                            mode='min' if "loss" in self.monitor else "max"
                                            )


        if self.of_percent:
            # if we want to overfit on a small portion of the data
            trainer = PLTrainer(  
                                logger=False,
                                progress_bar_refresh_rate=1,
                                check_val_every_n_epoch=1,
                                gpus=[self.gpu] if self.gpu_available and isinstance(self.gpu, int) else None,
                                #gradient_clip_val=self.hyperparams["gradient_clip"],    
                                overfit_pct=self.of_percent,
                                #train_percent_check=0.05,
                                max_epochs=20,
                                num_sanity_val_steps=1,
                                #track_grad_norm=2,
                                #weights_summary="top",
                                #profiler=True
                                )
        else:
            trainer = PLTrainer(  
                                logger=self.exp_logger,
                                checkpoint_callback=checkpoint_callback,
                                early_stop_callback=earlystopping,
                                progress_bar_refresh_rate=1,
                                check_val_every_n_epoch=1,
                                gpus=[self.gpu] if self.gpu_available and isinstance(self.gpu, int) else None,
                                #distributed_backend="dp" if gpus_available else None
                                gradient_clip_val=self.hyperparams["gradient_clip"],  
                                num_sanity_val_steps=5,  
                                max_epochs=self.hyperparams["max_epoch"],
                                resume_from_checkpoint=self.model_load_path,
                                #profiler=True

                                )

        return trainer


    def train(self, model):

        if self.exp_logger:
            self.exp_logger.log_tags(self.params["tags"])
            
        # if self.cv:
        #     self.__cv_train()  
        # else:
        self.pyto_trainer.fit(model)


    def test(self, model, return_preds=False):
        if self.exp_logger:
            self.exp_logger.log_tags(self.params["tags"] + ["test"])

        self.pyto_trainer.test(model)

        if return_preds:
            return self.model.test_task_preds


