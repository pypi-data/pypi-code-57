



from transformers import BertConfig, BertForTokenClassification
import torch
import torch.nn.functional as F
from axlnlp.models.base import PyToBase


class BertTok(PyToBase):

    def __init__(self,dataset:None, features:dict, hyperparams:dict):
        super().__init__(dataset=dataset, features=features, hyperparams=hyperparams)

        self.BATCH_SIZE = hyperparams["batch_size"]
        self.OPT = hyperparams["optimizer"]
        self.LR = hyperparams["hidden_dim"]
        config = BertConfig()
        config.num_labels = len(dataset.encoders["seg"])
        self.model = BertForTokenClassification.from_pretrained('bert-base-uncased', config=config)


    def forward(self, batch):
        bert_tok_encs = batch["bert"]
        mask = batch.mask

        tasks_preds = {}
        tasks_loss = {}
        for task in self.dataset.tasks:
            
            labels = batch[task]
            loss, outputs = self.model(
                                        input_ids=bert_tok_encs,
                                        labels=labels,
                                        attention_mask=mask,
                                        #encoder_attention_mask=mask
                                        )

            print("OUTPUT", outputs.shape)
            preds = torch.argmax(F.softmax(outputs, dim=-1), dim=-1).cpu().detach().numpy()

            mask_filter = labels.flatten() != self.dataset.encoders[task].pad_value
            preds = preds.flatten()[mask_filter]        
            
            tasks_preds[task] = preds
            tasks_loss[task] = loss

        return tasks_loss, tasks_preds
