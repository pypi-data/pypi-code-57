import numpy as np
import pandas as pd
import torch
from sklearn import metrics
from tqdm import tqdm
from torch.autograd import Variable
from matplotlib import pyplot as plt
from IPython.display import clear_output
from matplotlib.animation import FuncAnimation
from matplotlib import style
plt.style.use('dark_background')
import sys
sys.tracebacklimit = 0


log=[]
train_list=[]
val_list=[]
class Trainer:
    @staticmethod
    def __init__():
        global epoch,val_loss,train_loss,log,train_list,val_list,lr
        log=[]
        train_list=[]
        val_list=[]

    def reset():
        global epoch,val_loss,train_loss,log,train_list,val_list
        epoch=0
        val_loss=0.0
        train_loss=0.0
        log=[]
        train_list=[]
        val_list=[]


    @staticmethod
    def train(model,data_loader,optimizer,device):
        global train_loss,lr,train_list
        model.train()
        optimizer.zero_grad()
        train_loss=0.0
        lr=optimizer.param_groups[0]['lr']
        tk = tqdm(data_loader, total=len(data_loader), position=0, leave=True)
        for idx,data in enumerate(tk):
            optimizer.zero_grad()
            for key, value in data.items():
                data[key] = value.to(device)
            outputs, loss = model(**data)
            loss.backward()
            optimizer.step()
            train_loss+=float((loss.data).item())/len(data_loader.dataset)
            tk.set_postfix(loss=train_loss)
        train_list.append(train_loss)

    @staticmethod
    def evaluate(model,data_loader,device,scheduler=None,metric=metrics.accuracy_score,plot=True):
        global epoch,val_loss,train_loss,log,train_list,val_list,lr
        final_predictions=[]
        targets=[]
        model.eval()
        val_loss=0.0
        with torch.no_grad():
            tk = tqdm(data_loader, total=len(data_loader), position=0, leave=True)
            for idx,data in enumerate(tk):
                for key, value in data.items():
                    data[key] = value.to(device)
                outputs, loss = model(**data)
                val_loss+=float((loss.data).item())/len(data_loader.dataset)
                final_predictions.append(outputs.cpu())
                targets.extend(data['targets'].detach().cpu().numpy())
        val_list.append(val_loss)
        pred = np.vstack((final_predictions))
        if metric==metrics.f1_score or metric==metrics.precision_score or metric==metrics.recall_score:
            if pred.shape[1]>1:
                preds=np.argmax(pred,axis=1)
            else:
                preds=np.round_(np.maximum(pred.ravel(),0))
            metric_score=metric(y_true=targets,y_pred=preds,average='micro') #Used micro as this is better option for imbalanced datas.
            if scheduler is not None:
                scheduler.step(metric_score)
            print(f'-------Validation metric_score:{metric_score}')
        elif metric==metrics.accuracy_score:
            if pred.shape[1]>1:
                preds=np.argmax(pred,axis=1)
            else:
                preds=np.round_(np.maximum(pred.ravel(),0))
            metric_score=metrics.accuracy_score(y_true=targets,y_pred=preds)
            if scheduler is not None:
                scheduler.step(metric_score)
            print(f'-------Validation accuracy_score:{metric_score}')
        elif metric==metrics.roc_auc_score:
            if pred.shape[1]>1:
                pred=torch.nn.functional.softmax(torch.from_numpy(pred))
                targets=onehot((pred.shape[0],pred.shape[1]),targets)
                metric_score=metrics.roc_auc_score(targets,pred,average='macro',multi_class='ovo')
            else:
                metric_score=metric(targets,pred,average='micro')
            if scheduler is not None:
                scheduler.step(metric_score)
            print(f'-------Validation roc_auc_score:{metric_score}')
        else:
            if pred.shape[1]>1:
                pred=torch.nn.functional.softmax(torch.from_numpy(pred))
                targets=onehot((pred.shape[0],pred.shape[1]),targets)
                metric_score=metric(targets,pred)
            else:
                metric_score=metric(targets,pred)
            if scheduler is not None:
                scheduler.step(metric_score)
            print(f'-------Validation metric_score:{metric_score}')
        log.append([train_loss,val_loss,metric_score,lr])
        clear_output(wait=True)
        print(pd.DataFrame(log,columns=['Train_Loss','Valid_Loss','Metric_Score','Current_LR']),flush=True)
        if plot:
            Trainer.Plotit()
        return metric_score
    
    @staticmethod
    def predict(model,data_loader,device):
        model.eval()
        final_predictions = []
        with torch.no_grad():
            tk = tqdm(data_loader, total=len(data_loader), position=0, leave=True)
            for idx,data in enumerate(tk):
                for key, value in data.items():
                    data[key] = value.to(device)
                outputs, loss = model(**data)
                final_predictions.append(outputs.data.cpu())
        pred=np.vstack(final_predictions)
        return pred
    
    def get_log():
        return pd.DataFrame(log,columns=['Train_Loss','Valid_Loss','Metric_Score','Current_LR'])

    def animate():
        plt.plot(np.arange(len(train_list)),train_list,color='blue' )
        plt.plot(np.arange(len(val_list)),val_list,color='orange' )
        plt.xlabel('Epochs------>')
        plt.ylabel('Losses------->')
        plt.title('Train and Val Loss Analysis')
        plt.legend(['Train_loss','Val_loss'])
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    def Plotit():
        ani = FuncAnimation(plt.gcf(), Trainer.animate(), 5000)
        plt.tight_layout()
        plt.show()

    def onehot(size, target):
        vec = torch.zeros(size, dtype=torch.float32)
        vec[target] = 1
        return vec




