
#basics
from collections import Counter
import numpy as np
import warnings
import os
#warnings.filterwarnings("ignore")

#pytorch lightning
import pytorch_lightning as ptl

#pytroch
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from torch.optim.lr_scheduler import ReduceLROnPlateau


#sklearn
from sklearn.metrics import f1_score, precision_score, recall_score, precision_recall_fscore_support

#am 
import axlnlp.utils as u
from axlnlp import get_logger
from pprint import pprint



logger = get_logger("TRAINING")

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"



class PyToBase(ptl.LightningModule):

    def __init__(self, dataset:None, features:dict, hyperparams:dict):
        super().__init__()
        self.dataset = dataset
        self.features = features
        self.hyperparams = hyperparams
        self.training_outputs = []
        self.progress_bar_metrics = [   
                                        "train_mean_task_loss", 
                                        "val_mean_task_loss", 
                                        "train_mean_task_f1", 
                                        "val_mean_task_f1"
                                        ]
        self.split_id, self.split_set_ids = next(dataset.itersplits)


 
    ### NEEDS TO BE DEFINED FOR EACH MODEL
    def forward(self):
        raise NotImplementedError()


    ####### GENERAL ##################################

    #### FOR EVALUATION

    def _calc_epoch_score(self,outputs):
        collected_scores = {}
        nr_outputs = len(outputs)
        for output_dict in outputs:

            for k, v in output_dict.items():

                if k not in collected_scores:
                    collected_scores[k] = 0

                if torch.is_tensor(v):
                    v = v.cpu().detach().numpy()

                collected_scores[k] += v

            #collected_scores += Counter([o.cpu().detach().numpy() if torch.is_tensor(o) else o for o in output])
        mean_scores = {k:v/nr_outputs for k,v in collected_scores.items()}
        return mean_scores


    def _f1(self, targets, preds):
        return f1_score(targets, preds,average="macro")


    def _precision(self, targets, preds):
        return  precision_score(targets, preds, average="macro")


    def _recall(self, targets, preds):
        return recall_score(targets,preds,average="macro")


    def _p_r_f1(self,targets, preds):
        p = self._precision(targets, preds)
        r = self._recall(targets, preds)
        f1 = self._f1(targets,preds)
        return p,r,f1


    def _score_per_class(self,targets, preds):
        ## TODO
        pass


    def _cal_update_scores(self,score_log, batch, tasks_pred, step_type):


        for task, preds in tasks_pred.items():

            #TODO: need to remove pads?
            if len(preds.shape) > 1 or not isinstance(preds[0],int):
                preds = preds.flatten()
                        
            #np.array([p for sample in preds for p in sample])
            # else:
            #     print(LOL)

            targets = batch.get_flat(task, remove=self.dataset.task2padvalue[task]).cpu().detach().numpy()  #.cpu().detach().numpy()

            p, r, f1 = self._p_r_f1(targets,preds)
            score_log.update({
                                '{}_{}_f1'.format(task, step_type): f1, 
                                '{}_{}_precision'.format(task, step_type): p, 
                                '{}_{}_recall'.format(task, step_type): r
                                })

            if "_" not in task:
                score_log['{}_mean_task_f1'.format(step_type)].append(f1)
                score_log['{}_mean_task_precision'.format(step_type)].append(p)
                score_log['{}_mean_task_recall'.format(step_type)].append(r) 


    def _get_score_log(self, tasks_loss, batch, tasks_pred, step_type):

        # first we get the predictions for each subtask and add it to
        # the prediction dict
        for task, preds in tasks_pred.items():
            if "_" not in task:
                continue
            
            subtask_preds = self._get_subtask_preds(task, preds)
            tasks_pred.update(subtask_preds)


        # set up the score log
        score_log = {}
        score_log['{}_mean_task_f1'.format(step_type)] = []
        score_log['{}_mean_task_precision'.format(step_type)] = []
        score_log['{}_mean_task_recall'.format(step_type)] = []  

        # calculating and saving the task scores
        self._cal_update_scores(score_log, batch, tasks_pred, step_type)

        # calculating the average of all subtask, NOTE note the TASK
        score_log['{}_mean_task_f1'.format(step_type)] = np.mean(score_log['{}_mean_task_f1'.format(step_type)])
        score_log['{}_mean_task_precision'.format(step_type)] = np.mean(score_log['{}_mean_task_precision'.format(step_type)])
        score_log['{}_mean_task_recall'.format(step_type)] = np.mean(score_log['{}_mean_task_recall'.format(step_type)])

        # log loss
        for task in tasks_loss.keys():
            score_log['{}_{}_loss'.format(task, step_type)] = tasks_loss[task]

        # get total loss
        total_loss = 0
        for k,v in tasks_loss.items():
            total_loss += v

        score_log['{}_total_loss'.format(step_type)] = total_loss
        score_log['{}_mean_task_loss'.format(step_type)] = total_loss / len(tasks_loss)

        return score_log


    def _get_subtask_preds(self, task, preds):
        subtask_preds = {}
        decoded_preds = [self.dataset.decode(p,task) for p in preds]
        for subtask in task.split():

            # get the positon of the subtask in the joint label
            # e.g. for  labels following this, B_MajorClaim, 
            # BIO is at position 0, and AC is at position 1
            subtask_position = self.dataset.get_subtask_position(subtask)

            # remake joint labels to subtask labels
            subtask_preds = [   
                                self.dataset.encode(p.split("_")[subtask_position],subtask) 
                                for p in decoded_preds
                                ]

            subtask_preds[subtask] = subtask_preds
        return subtask_preds


    def _step(self, batch_ids, step_type):

        # fetches the device so we can place tensors on the correct memmory
        device = f"cuda:{next(self.parameters()).get_device()}" if self.on_gpu else "cpu"

        batch_ids = batch_ids.cpu().detach().numpy()


        # load our encoded and padded data into the Batch Class
        batch_features = None
        if self.features:
            batch_features = self.features.get(self.split_id, sample_ids=batch_ids)

        batch = Batch(
                        data=self.dataset[batch_ids],
                        features=batch_features,
                        device=device,
                    )

        #pass on the whole batch to the model
        tasks_loss, tasks_pred = self.forward(batch)

        # assert that the predictions are ints not one hots
        #assert np.mean([len(p.shape) for p in tasks_pred.values()]) == 1, "for each task a 1d array is expected"

        # calc all scores
        score_log = self._get_score_log(tasks_loss, batch, tasks_pred, step_type)

        # if we want test prediction we save them so we can easily access them
        if step_type=="test": #and self.params["save_test_preds"]:

            if not hasattr(self, 'test_task_preds'):
                self.test_task_preds = {task:[] for task in tasks_pred.keys()}

            ids = batch["ids"].cpu().detach().numpy()
            for task, preds in tasks_pred.items():
                self.test_task_preds[task].extend(list(zip(ids,preds)))
        
        return score_log


    def training_step(self, batch_ids, batch_idx):
        score_log = self._step(batch_ids, "train")
        self.training_outputs.append(score_log)
        return {'loss': score_log.get("train_total_loss")}


    def validation_step(self, batch_ids, batch_idx):
        score_log = self._step(batch_ids, "val")
        return score_log


    def validation_epoch_end(self, outputs):

        score_log_val = self._calc_epoch_score(outputs)

        #adding training scores
        if  len(self.training_outputs):
            score_log_train = self._calc_epoch_score(self.training_outputs)
            score_log_val.update(score_log_train)
            self.training_outputs = []

        #adding epoch number
        score_log_val["epoch"] = self.current_epoch

        return {
                "progress_bar": {k:v for k,v in score_log_val.items() if k in self.progress_bar_metrics},
                "log":score_log_val
                }


    def test_step(self, batch_ids, batch_idx):
        score_log = self._step(batch_ids, "test")
        return score_log


    def test_epoch_end(self, outputs):
        score_log_test = self._calc_epoch_score(outputs)

        #adding epoch number
        score_log_test["epoch"] = self.current_epoch

        return {
                "progress_bar": {k:v for k,v in score_log_test.items() if "f1" in k},
                "log":score_log_test
                }
     
    ## FOR LOADING DATA
    @ptl.data_loader
    def train_dataloader(self):
        return DataLoader(DataDriver(self.split_set_ids["train"]), batch_size=self.BATCH_SIZE, shuffle=False, num_workers=10)

    @ptl.data_loader
    def val_dataloader(self):
        return DataLoader(DataDriver(self.split_set_ids["dev"]), batch_size=self.BATCH_SIZE, shuffle=False, num_workers=10)

    @ptl.data_loader
    def test_dataloader(self):
        return DataLoader(DataDriver(self.split_set_ids["test"]), batch_size=self.BATCH_SIZE, shuffle=False, num_workers=10)


    def configure_optimizers(self):

        if self.OPT.lower() == "adadelta":
            opt = torch.optim.Adadelta(self.parameters(), lr=self.LR)
        elif self.OPT.lower() == "sgd":
            opt = torch.optim.SGD(self.parameters(), lr=self.LR)
        elif self.OPT.lower() == "adam":
            opt = torch.optim.Adam(self.parameters(), lr=self.LR)
        elif self.OPT.lower() == "rmsprop":
            opt = torch.optim.RMSprop(self.parameters(), lr=self.LR)
        else:
            raise KeyError(f'"{self.OPT}" is not a supported optimizer')
        
        scheduler = None
        if self.hyperparams["scheduler"]:
            if self.hyperparams["scheduler"] == "ROP":
                scheduler =  {
                                'scheduler': ReduceLROnPlateau( opt, 
                                                                mode='min' if "loss" in self.hyperparams["monitor"] else "max",
                                                                patience=3, 
                                                                factor=0.5,
                                                                min_lr=0.0001
                                                                ),
                                'monitor': self.hyperparams["monitor"],
                                'interval': 'epoch',
                                'frequency': 1
                            }
            else:
                raise KeyError(f'"{self.hyperparams["scheduler"]}" is not a supported optimizer')

        if scheduler:
            return [opt], [scheduler]
        else:
            return opt


    def optimizer_step(
            self,
            epoch: int,
            batch_idx: int,
            optimizer: int,
            optimizer_idx: int,
            second_order_closure:int = None
            )-> None:
        r"""
        Override this method to adjust the default way the
        :class:`~pytorch_lightning.trainer.trainer.Trainer` calls each optimizer.
        By default, Lightning calls ``step()`` and ``zero_grad()`` as shown in the example
        once per optimizer.

        Args:
            epoch: Current epoch
            batch_idx: Index of current batch
            optimizer: A PyTorch optimizer
            optimizer_idx: If you used multiple optimizers this indexes into that list.
            second_order_closure: closure for second order methods

        Examples:
            .. code-block:: python

                # DEFAULT
                def optimizer_step(self, current_epoch, batch_idx, optimizer, optimizer_idx,
                                   second_order_closure=None):
                    optimizer.step()
                    optimizer.zero_grad()

                # Alternating schedule for optimizer steps (i.e.: GANs)
                def optimizer_step(self, current_epoch, batch_idx, optimizer, optimizer_idx,
                                   second_order_closure=None):
                    # update generator opt every 2 steps
                    if optimizer_idx == 0:
                        if batch_idx % 2 == 0 :
                            optimizer.step()
                            optimizer.zero_grad()

                    # update discriminator opt every 4 steps
                    if optimizer_idx == 1:
                        if batch_idx % 4 == 0 :
                            optimizer.step()
                            optimizer.zero_grad()

                    # ...
                    # add as many optimizers as you want


            Here's another example showing how to use this for more advanced things such as
            learning rate warm-up:

            .. code-block:: python

                # learning rate warm-up
                def optimizer_step(self, current_epoch, batch_idx, optimizer,
                                    optimizer_idx, second_order_closure=None):
                    # warm up lr
                    if self.trainer.global_step < 500:
                        lr_scale = min(1., float(self.trainer.global_step + 1) / 500.)
                        for pg in optimizer.param_groups:
                            pg['lr'] = lr_scale * self.hparams.learning_rate

                    # update params
                    optimizer.step()
                    optimizer.zero_grad()

        """
        if self.trainer.use_tpu and XLA_AVAILABLE:
            xm.optimizer_step(optimizer)
        elif isinstance(optimizer, torch.optim.LBFGS):
            optimizer.step(second_order_closure)
        else:
            optimizer.step()


        # print("WEIGHTS AFTER OPTIMIZER")
        # print(self.lstm.weight_ih_l0)
        # print(self.lstm.weight_hh_l0)

        # clear gradients
        optimizer.zero_grad()


    def backward(self, trainer, loss: int, optimizer: int, optimizer_idx: int) -> None:
        """Override backward with your own implementation if you need to

        :param trainer: Pointer to the trainer
        :param loss: Loss is already scaled by accumulated grads
        :param optimizer: Current optimizer being used
        :param optimizer_idx: Index of the current optimizer being used

        Called to perform backward step.
        Feel free to override as needed.

        The loss passed in has already been scaled for accumulated gradients if requested.

        .. code-block:: python

            def backward(self, use_amp, loss, optimizer):
                if use_amp:
                    with amp.scale_loss(loss, optimizer) as scaled_loss:
                        scaled_loss.backward()
                else:
                    loss.backward()

        """
        if trainer.precision == 16:

            # .backward is not special on 16-bit with TPUs
            if not trainer.on_tpu:
                with amp.scale_loss(loss, optimizer) as scaled_loss:
                    scaled_loss.backward()
        else:
            loss.backward()

        # print("GRADIENTS AFTER BACKWARDS")
        # print(self.lstm.weight_ih_l0.grad)
        # print(self.lstm.weight_hh_l0.grad)


#Helper class used for pytorch batching
class DataDriver(Dataset):

    def __init__(self, ids):
        self.ids = ids

    #simple len
    def __len__(self):
        return len(self.ids)
        
    #Returns one instance of data and target
    def __getitem__(self, idx):
        return self.ids[idx]


class Batch:

    def __init__(self, data:np.ndarray, features:np.ndarray, device=None):
        self.device = device
        self.data = data
        self.data.reset_index(drop=True, inplace=True)
        self.data.sort_values("lengths", ascending=False, inplace=True)

        if features:
            self.features = features[self.data.index.to_numpy()] #lets not forget to sort embeddings by the new index of the df
            
        self.longest_seq = self.data["lengths"].values[0]
        self.mask = self.__get_mask()


        ##############################
        # TODO: create fucntion for getting words and labels
        # for debuggins and checking

        # print("IDS", batch["ids"])
        # ID = list(batch["ids"].cpu().detach().numpy())[1]
        # list_targets = list(target_tags.cpu().detach().numpy())[1]

        # wordids = list(batch["words"].cpu().detach().numpy())[1]
        # words = self.dataset.encoders["word"].decode_list(wordids)

        # print(ID)
        # print(list(zip(words,list_targets)))
        ######################


    def __len__(self):
        return self.data.shape[0]


    def __getitem__(self, key):

        if key in ["lengths", "ids"]:
            return torch.LongTensor(self.data[key].to_numpy()).to(self.device)

        elif key == "batch_ids":
            return torch.LongTensor(self.data.index.to_numpy()).to(self.device)

        elif key in ["embs"]:
            re_padded = self.features[:,:self.longest_seq]
            return torch.tensor(re_padded, dtype=torch.float, device=self.device)

        elif key in self.data:
            #remvoing paddings so it fits the batch
            re_padded = np.stack(self.data[key])[:,:self.longest_seq]
            return torch.tensor(re_padded, dtype=torch.long, device=self.device)
            
        else:
            raise KeyError(f"{key} is neither in feature or data table")


    def keys(self):
        keys = list(self.data.columns) + ["embs"]
        return keys


    def __get_mask(self):
        lengths = self.data["lengths"]
        mask = torch.zeros((len(lengths), self.longest_seq), dtype=torch.uint8)
        for i,length in enumerate(lengths): 
            mask[i][:length] = torch.ones((length,))
        return mask.to(self.device)


    def get_flat(self,key, remove=None):
        stacked = self[key]
        flatt = stacked.flatten()

        if remove:
            flatt = flatt[flatt != remove]

        return flatt
