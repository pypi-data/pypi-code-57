# coding=UTF-8
import os
import cv2
import json
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt


class Basic_DNN():

    def __init__(self, input_dim=1, output_dim=1, purpose=None, hidden_layers=[1]):
        #input_dim 输入数据维度，也是第一层的units
        #output_dim 输出层维度，如果是分类问题，相当于各分类的可能性
        #purpose 目的，"REGRESS"或"CLASSIFY"，即回归问题或分类问题,如果是回归问题，最后一层不激活，如果是分类问题：
        if purpose is None:
            if output_dim == 1:
                purpose = "REGRESS"
            else:
                purpose = "CLASSIFY"
        self.output_dim = output_dim
        self.purpose = purpose
        # 如果output_dim为1，则用sigmoid激活，如果大于1，则用softmax激活。
        #hidden_layers 数组，每个元素数值表示一个层,这里规则比较灵活，举例说明：
        #比如hidden_layers=[16,(32),(32,"sigmoid"),0.3]，则表示：
        #16个神经元全连接层不激活---》32个神经元全连接层不激活--》32个神经元全连接sigmoid激活--》dropput层丢弃率0.3
        # 可以通过以下语句建立神经网络模型
        self._history = None
        self._h5_path = None
        
        model = keras.models.Sequential()
        for h in range(len(hidden_layers)):
            l=hidden_layers[h]
            if isinstance(l,int):
                u=l
                if l==0:
                    model.add(keras.layers.Dense(units=u,activation=None,input_dim=input_dim))
                else:
                    model.add(keras.layers.Dense(units=u,activation=None))
            if isinstance(l,tuple):
                if len(l)==1:
                    u=l[0]
                    act=None
                else:
                    u=l[0]
                    act=l[1]
                if l==0:
                    model.add(keras.layers.Dense(units=u,activation=act,input_dim=input_dim))
                else:
                    model.add(keras.layers.Dense(units=u,activation=act))
            if isinstance(l,float):
                if l<1:
                    pass
                else:
                    model.add(keras.layers.Dropout(l))
        if self.purpose=="REGRESS":
            act = None
            loss="mse"
        elif self.purpose == "CLASSIFY" and self.output_dim == 1:
            act = "sigmoid"
            loss="binary_crossentropy"
        else:
            act = "softmax"
            loss="categorical_crossentropy"

        model.add(keras.layers.Dense(units=self.output_dim,activation=act))
        model.compile(optimizer='adam',loss=loss,metrics=['acc'])
        self.model=model
        #     
    def train(self, train_data, data_split=[7,2,1], batch_rate=0.1, epochs=10):
        #按原Basic_CNN方式进行训练

        self.train_data=train_data
        self.data_split = data_split
        self.batch_rate = batch_rate
        self.epochs = epochs
        

        
        X, Y = train_data                                        # 把所有数据都放到X，Y中
        permutation=np.random.permutation(len(X))
        X,Y=X[permutation],Y[permutation]
        split_len = sum(data_split)                              # 计算data_split中的和
        train_index = int(len(X)*data_split[0]//split_len)       # 确定训练集的分界点
        validation_index = int(len(X)*(data_split[0]+data_split[1])//split_len)  # 确定验证集分界点，假设data_split=(5,3,2),train_data有100个，那么前50个为训练集，中间30个为验证集，最后的都为测试集

        # 根据边界分割出训练集、验证集、测试集
        train_x = X[:train_index]
        train_y = Y[:train_index]
        val_x = X[train_index:validation_index]
        val_y = Y[train_index:validation_index]
        test_x = X[validation_index:]
        test_y = Y[validation_index:]

        batch_size = np.int(np.ceil(self.batch_rate * len(train_x)))  # 计算batch_size

        print( "开始训练模型,训练次数:%d,单次数据量:%d" % (epochs, batch_size) )

        history = self.model.fit(
            x=train_x, y=train_y,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(val_x, val_y)
        )

        # print(history)
        self._history = History(history)

        if len(test_x) > 0:  # 如果测试集有数据，就用evaluate方法统计测试集数据
            test = self.model.evaluate(test_x, test_y, batch_size)
            print( "测试集偏差:%f,测试集准确率:%f" % tuple(test) )




    @property
    def history(self):
        return self._history

    @property
    def h5_path(self):
        return self._h5_path

    def predict(self, xdata):
        return self.model.predict(xdata)


    def save(self, modelname):
        """
        保存，在当前目录生成一个"modelname"的文件夹，文件夹结构如下：
        ./
            modelname/
                modelname.h5        #标准h5文件
                config.json          #包括input_shape（输入图片形状）、labels（标签文本列表）信息
        """
        if self.model is None: return

        _path = modelname + "_model"
        if not os.path.exists(_path):
            os.mkdir( _path )

        self.model.save( _path + "/" + modelname + ".h5" )
        self._h5_path = os.path.abspath(_path) + "/" + modelname + ".h5"

        config = {}
        config["input_shape"] = self.input_shape
        #config["labels"] = self.output_label
        with open(_path + "/config.json", 'w') as f:
            json.dump(config, f)

    def load(self, modelname):
        """
        通过modelname加载模型，除了加载h5文件外，还要加载input_shape（输入图片形状）、labels（标签文本列表）信息
        """
        _path = modelname + "_model"
        if not os.path.exists(_path): return
        if not os.path.exists(_path + "/config.json"): return
        if not os.path.exists(_path + "/" + modelname + ".h5"): return

        config = None
        with open(_path + "/config.json", 'r') as f:
            config = json.load(f)
        if config is None: return

        self.model = keras.models.load_model(_path + "/" + modelname + ".h5")
        if "input_shape" in config: self.input_shape = config["input_shape"]
        #if "labels" in config: self.output_label = config["labels"]


class History():

    def __init__(self, _history):
        self._data = _history.history
            
    @property
    def data(self):
        return self._data
        
    def plot(self):
        if "acc" in self._data:
            plt.plot( self._data['acc'], label="acc" )
        if "val_acc" in self._data:
            plt.plot( self._data['val_acc'], label="val_acc" )
        if "loss" in self._data:
            plt.plot( self._data['loss'], label="loss" )
        if "val_loss" in self._data:
            plt.plot( self._data['val_loss'], label="val_loss" )
        plt.legend()
        plt.show()
