import torch
import numpy as np
# import matplotlib.pyplot as plt
from kmeans_pytorch import kmeans,kmeans_predict
import os
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans as sk_KMeans
from transformers import AlbertModel, BertTokenizer,AlbertConfig
import torch
import torch.nn as nn
import tkitText,tkitFile
import traceback
# from albert_kmeans import *
import pprint

device="cpu"


def load_albert(path):
    """
    加载模型
    """
    vocab_file = os.path.join(path,'vocab.txt')
    tokenizer = BertTokenizer.from_pretrained(vocab_file)
    # print(tokenizer)
    config = AlbertConfig.from_pretrained(path)
    model = AlbertModel.from_pretrained(path,config=config)
    return model,tokenizer
# text_list=["你好吗",'我很不错',"哈哈",'我喜欢吃肉','我喜欢猪肉',"哈哈",'我喜欢吃肉']
# path=
# model,tokenizer =load_albert(path)
# li=torch.tensor([])  # 现有list时尽量用这种方式
from sklearn.semi_supervised import LabelSpreading
import json

import pickle

import pymongo
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
KDB=client.kmeans

tt=tkitText.Text()
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
def search_content(keyword):
    client = Elasticsearch()
    q = Q("multi_match", query=keyword, fields=['title', 'body'])
    # s = s.query(q)

    # def search()
    s = Search(using=client)
    # s = Search(using=client, index="pet-index").query("match", content="金毛")
    s = Search(using=client, index="pet-index").query(q)
    response = s.execute()
    return response
def search_sent(keyword):
    client = Elasticsearch()
    q = Q("multi_match", query=keyword, fields=['title', 'content'])
    s = Search(using=client)
    # s = Search(using=client, index="pet-index").query("match", content="金毛")
    s = Search(using=client, index="pet-sent-index").query(q)
    response = s.execute()
    return response
def find_sent(keyword):
    text=''
    for sent in search_sent(keyword):
        # print(sent)
        text=text+sent.content
    text_list=tt.sentence_segmentation_v1(text)
    return text_list

def find_content(keyword):
    text=''
    for sent in search_content(keyword):
        # print(sent)
        text=text+sent.title+"。"+sent.content
    text_list=tt.sentence_segmentation_v1(text)
    return text_list


def get_embedding(text_list,labels,tokenizer,model):
    """
    获取文本特征
    """
    # text_list=["你好吗",'我很不错']
    # li=torch.tensor([])  # 现有list时尽量用这种方式

    presentence_embedding,text_list,labels=get_embedding_np(text_list,labels,tokenizer,model)

    presentence_embedding = torch.from_numpy(presentence_embedding)   #为numpy类型
    # print( "presentence_embedding",presentence_embedding.size())
    return presentence_embedding,text_list,labels


def get_embedding_np(text_list,labels,tokenizer,model):
    """
    获取文本特征
    """
    # text_list=["你好吗",'我很不错']
    # li=torch.tensor([])  # 现有list时尽量用这种方式
    # print(text_list)
    del_list=[]
    new_labels=[]
    new_text_list=[]
    # presentence_embedding=None
    if len(text_list)>=0:
        pass
    else:
        return
    for i,text in enumerate( text_list):
        # print(text)


        # print(input_ids)
        try:
            input_ids = torch.tensor(tokenizer.encode(text, add_special_tokens=False)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids) 
            x=outputs[0].double()
            # print('x',x)
            sentence_embedding = torch.mean(x, 1)
            # print(sentence_embedding)
            if i!=0:
                # presentence_embedding=torch.cat((sentence_embedding, sentence_embedding), 0)	# 在 0 维(纵向)进行拼接

                # presentence_embedding=presentence_embedding+sentence_embedding.detach().numpy()
                presentence_embedding=np.concatenate((presentence_embedding,sentence_embedding.detach().numpy()),axis=0)
                
            else:
                presentence_embedding=sentence_embedding.detach().numpy()
 
            new_text_list.append(text)
            if len(labels)>0:
                new_labels.append(labels[i])
 
        except:
            # traceback.print_exc()
            pass
    # print(presentence_embedding)
    # print(new_text_list,new_labels)
    # presentence_embedding = torch.from_numpy(presentence_embedding)   #为numpy类型
    # print( "presentence_embedding",presentence_embedding.size())
    return presentence_embedding,new_text_list,new_labels




def save_list(presentence_embedding,f='data/output.txt'):
    """
    保存np数据
    """
    with open(f, 'a') as f_handle:
        np.savetxt(f_handle,presentence_embedding)

def load_list(f='data/output.txt'):
    """
    加载np数据
    """
    return np.loadtxt(f)

def auto_add_labels(word,labels):
    """
    自动添加labels
    """
    new_labels={}
    for i in labels.keys():
        new_labels[labels[i]]=i
    if new_labels.get(word):
        new_labels=labels
        pass
    else:
        new_labels[word]=len(labels)
    l_labels={}
    for i in new_labels.keys():
        l_labels[new_labels[i]]=i
    return l_labels

    





# def bulid_pre_dict(text_list,output_labels):
#     """
#     将分类结果包装成词典
#     """
#     klist={}
#     for i,c in enumerate (output_labels):
#         # print(i,c,text_list[i])
#         if klist.get(c):
#             klist[c].append(text_list[i])
#         else:
#             klist[c]=[text_list[i]]
#     return klist

def bulid_pre_dict(text_list,output_labels):
    """
    将分类结果包装成词典
    """
    klist={}
    for i,c in enumerate (output_labels):
        # print(i,c,text_list[i])
        if klist.get(c):
            klist[c].append(text_list[i])
        else:
            klist[c]=[text_list[i]]
    return klist
def get_pre_label(text_list,output_labels):
    klist=bulid_pre_dict(text_list,output_labels)
    return klist,read_labels()
# def sk_KMeans(presentence_embedding,n_cluster=10):
#     kmeans = KMeans(n_clusters=n_cluster).fit(presentence_embedding)
#     # print kmeans
#     return kmeans

def find_k(presentence_embedding,max=10):
    """
    选择拐点
    https://stackoverflow.com/questions/19197715/scikit-learn-k-means-elbow-criterion
    
    """
    from sklearn.metrics import silhouette_score
    X=presentence_embedding
    p_y=[]
    p_x=[]
    for n_cluster in range(2, max):
        kmeans = sk_KMeans(n_clusters=n_cluster).fit(X)
        label = kmeans.labels_
        sil_coeff = silhouette_score(X, label, metric='euclidean')
        print("For n_clusters={}, The Silhouette Coefficient is {}".format(n_cluster, sil_coeff))
        p_y.append(sil_coeff)
        p_x.append(n_cluster)


    plt.figure()
    plt.plot(p_x, p_y)
    plt.xlabel("k ")
    plt.ylabel("SSE")
    plt.show()
# find_k(presentence_embedding,len(presentence_embedding)-2)



def bulid_t_data(mjson):
    data=[]
    labels=[]
    for it in mjson.auto_load():
        if len(it['sentence'])>2:
            data.append(it['sentence'])
            labels.append(int(it['label']))
    return data,labels
def auto_train(new_text_list,marked_text,marked_label,tokenizer,model,n_neighbors=10):
    # 训练

    labels=marked_label+[-1]*len(new_text_list)

    text_list=marked_text+new_text_list
    # print(text_list)
    # for i,it in enumerate(text_list) :
    #     if len(it)>5:
    #         pass
    #     else:
    #         del text_list[i]
    #         del labels[i]
    #         print('111')
    # print(len(labels)) 
    # print(len(text_list))

    presentence_embedding,text_list,labels=get_embedding_np(text_list,labels,tokenizer,model)
    labels=np.array(labels)
    if len(presentence_embedding)==len(labels):
        #https://github.com/scikit-learn/scikit-learn/blob/95d4f0841/sklearn/semi_supervised/_label_propagation.py#L302
        label_spread = LabelSpreading(kernel='knn', alpha=0.8)
        label_spread.fit(presentence_embedding, labels)
        # #############################################################################
        # Plot output labels
        output_labels = label_spread.transduction_

        # print("output_labels",output_labels)
        return output_labels[-len(new_text_list):].tolist()
    else:
        print("不一样长：",len(presentence_embedding),len(labels))
def auto_train_DBSCAN(new_text_list,tokenizer,model):
    # 训练
    presentence_embedding,text_list,_=get_embedding_np(new_text_list,[],tokenizer,model)
    # print(presentence_embedding[:1])
    y_pred = DBSCAN(eps = 0.1, min_samples = 2).fit_predict(presentence_embedding)
    return y_pred

def Pre_KMeans(new_text_list,tokenizer,model,n_cluster=10):
    presentence_embedding,text_list,_=get_embedding_np(new_text_list,[],tokenizer,model)
    kmeans = sk_KMeans(n_clusters=n_cluster).fit(presentence_embedding)
    # print kmeans
    return kmeans.labels_

def read_labels():
    try:
        with open("data/labels.json",'r') as f:
            c_list = json.load(f)
            return c_list
    except:
        return {}
def save_labels(c_list):
    with open("data/labels.json",'w') as f:
        json.dump(c_list,f)

def run_search_content_DBSCAN(keyword,tokenizer,model,num_clusters=20):
    """
    对搜索结果进行聚类
    基于sk的np数据
    """

    text_list=find_content(keyword)
    cluster_ids_x=Pre_KMeans(text_list,tokenizer,model)
    klist=bulid_pre_dict(text_list,cluster_ids_x.tolist())
    return klist

def kmeans_sk_content(text_list,tokenizer,model,num_clusters=20):
    # presentence_embedding,text_list,labels=get_embedding(text_list,[],tokenizer,model)
    # presentence_embedding=torch.tensor(presentence_embedding, dtype=torch.long)

    cluster_ids_x=Pre_KMeans(text_list,tokenizer,model,num_clusters)
    klist=bulid_pre_dict(text_list,cluster_ids_x.tolist())
    # klist={}
    # for i,c in enumerate (cluster_ids_x.tolist()):
    #     # print(i,c,text_list)
    #     if klist.get(c):
    #         klist[c].append(text_list[i])
    #     else:
    #         klist[c]=[text_list[i]]
    # # pprint.pprint(klist)
    return klist

def run_search_content_sk(keyword,tokenizer,model,num_clusters=20):
    """
    对搜索结果进行聚类
    基于sk的np数据
    """

    text_list=find_content(keyword)
    
    klist=kmeans_sk_content(text_list,tokenizer,model,num_clusters)
    return klist

 


def kmeans_content(text_list,tokenizer,model,num_clusters=20):
    presentence_embedding,text_list,labels=get_embedding(text_list,[],tokenizer,model)
    presentence_embedding=torch.tensor(presentence_embedding, dtype=torch.long)

    cluster_ids_x, cluster_centers = kmeans(
        X=presentence_embedding, num_clusters=num_clusters, distance='euclidean', device=torch.device('cpu'),tol=1e-8
    )
    klist=bulid_pre_dict(text_list,cluster_ids_x.tolist())
    # klist={}

    # for i,c in enumerate (cluster_ids_x.tolist()):
    #     # print(i,c,text_list)
    #     if klist.get(c):
    #         klist[c].append(text_list[i])
    #     else:
    #         klist[c]=[text_list[i]]
    # # pprint.pprint(klist)
    return klist

def run_search_content(keyword,tokenizer,model,num_clusters=20):
    """
    对搜索结果进行聚类
    """

    text_list=find_content(keyword)
    klist=kmeans_content(text_list,tokenizer,model,num_clusters)
    return klist

 

def run_search_sent(keyword,tokenizer,model,num_clusters=20):
    """
    对搜索结果进行聚类
    """

    text_list=find_sent(keyword)
    klist=kmeans_content(text_list,tokenizer,model,num_clusters)
    return klist
    # presentence_embedding,text_list,labels=get_embedding(text_list,[],tokenizer,model)
    # # print("总共数据：",len(presentence_embedding))
    # presentence_embedding=torch.tensor(presentence_embedding, dtype=torch.long)
    # # print(text_list,labels)
    
    # # # print('x',x )
    # # # # # kmeans
    # cluster_ids_x, cluster_centers = kmeans(
    #     X=presentence_embedding, num_clusters=num_clusters, distance='euclidean', device=torch.device('cpu'),tol=1e-8
    # )
    # # print('cluster_ids_x',cluster_ids_x)
    # # print("cluster_centers",cluster_centers)

    # # output_dir='./model'
    # # torch.save(cluster_centers, os.path.join(output_dir, 'Kmean.bin'))


    # klist={}

    # for i,c in enumerate (cluster_ids_x.tolist()):
    #     # print(i,c,text_list)
    #     if klist.get(c):
    #         klist[c].append(text_list[i])
    #     else:
    #         klist[c]=[text_list[i]]
    # # pprint.pprint(klist)
    # return klist




    # # #绘图

    # # x=presentence_embedding
    # # # plot
    # # plt.figure(figsize=(4, 3), dpi=160)
    # # plt.scatter(x[:, 0], x[:, 1], c=cluster_ids_x, cmap='cool')
    # # # plt.scatter(y[:, 0], y[:, 1], c=cluster_ids_y, cmap='cool', marker='X')
    # # plt.scatter(
    # #     cluster_centers[:, 0], cluster_centers[:, 1],
    # #     c='white',
    # #     alpha=0.6,
    # #     edgecolors='black',
    # #     linewidths=2
    # # )
    # # plt.axis([-1, 1, -1, 1])
    # # plt.tight_layout()
    # # plt.show()
