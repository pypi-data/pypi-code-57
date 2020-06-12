# coding=UTF-8
"""
import warnings
warnings.filterwarnings("ignore")
""" 
import os
import cv2
import json
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt

class Basic_CNN():

    def __init__(self, input_shape, output_label, hidden_layers=[32,-1,32,-1], dropout=0.3):
        """
        @input_shape    CNN输入数据形状，此处也可以写成input_shape=x.shape[:3]，默认(30,30,3)
        @hidden_layers  默认参数[32,-1,32,-1]，表示：第一层卷积units=32，第二层为最大池化（-1）或者平均池化（0），
                        第三层卷积units=32，第四层又是池化，这个参数用来指定中间的隐藏层
        @dropout        隐藏层后的flatten层与最后的全连接之间加入一个dropout层，这个参数用来指定dropout的比率
        @output_label   输出标签，可以用标签列表['null','ok','good'] 表示，也可以调用convertor.labels获取
        """
        self.input_shape = input_shape
        self.hidden_layers = hidden_layers
        self.dropout = dropout
        self.output_label = output_label
        self.model = None
        self._history = None
        self._h5_path = None
        # print("__init__ Basic_CNN")

    def train(self, train_data, data_split=[7,2,1], batch_rate=0.1, epochs=3):
        """
        @train_data     模型训练，指定训练参数,其实这里是接受一个元组，一起把图片与标签都给了，也可以写成train_data=(x,y)
        @data_split     根据data_split提供的三个数比例划分出训练集、验证集、测试集,默认[7,2,1]
        @batch_rate     相当于确定batch_size，根据比值计算出batch_size，
                        比如总共1000个训练集数据的话，0.1就是100的batch_size大小
        @epochs         训练轮次，默认3
        """
        self.train_data = train_data
        self.data_split = data_split
        self.batch_rate = batch_rate
        self.epochs = epochs

        self.model = keras.Sequential()

        self.model.add(keras.layers.Conv2D(filters=self.hidden_layers[0],kernel_size=(3,3),activation='relu',input_shape=self.input_shape,padding='same'))
        for h in self.hidden_layers[1:]:
            if h==-1:
                self.model.add(keras.layers.MaxPool2D())
            elif h==0:
                self.model.add(keras.layers.AvgPool2D())
            else:
                self.model.add(keras.layers.Conv2D(filters=h,kernel_size=(3,3),activation='relu',padding='same'))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(256,activation='relu'))
        self.model.add(keras.layers.Dropout(self.dropout))
        self.model.add(keras.layers.Dense(len(self.output_label),activation='softmax'))  # 最后的输出维度要按照标签个数来，即多少分类
        self.model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['acc'])

        X, Y = train_data                                        # 把所有数据都放到X，Y中
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

        # model.save("/home/khadas/labplus/garbage_classification_CNN/model.h5")
        # print("Basic_CNN.train")

    @property
    def history(self):
        """
        获取原history.history对象
        """
        return self._history

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
        config["labels"] = self.output_label
        with open(_path + "/config.json", 'w') as f:
            json.dump(config, f)
        # print("Basic_CNN.save")

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
        if "labels" in config: self.output_label = config["labels"]
        # print("Basic_CNN.load")
        
    @property
    def h5_path(self):
        """
        获取h5文件绝对路径
        ~./model/model.h5
        """
        return self._h5_path
    
    def predict(self, frame):
        """
        预测，返回结果是一个列表，每个列表元素是一个字典，示例如下：
        ->{"null":0.534,"ok":0.323,"good":0.143}
        """
        shape = frame.shape
        if len(shape) == 3:   # 如果是单张图片，则改为四向量结构
            shape = np.append([1], list(shape))
            frame = frame.reshape( shape )
        res = self.model.predict(frame)
        res = res.tolist()[0]
        # print(res)

        labels = self.output_label

        if len(res) != len(labels): return None

        result = {}
        for i in range(len(res)):
            result[labels[i]] = res[i]

        # print(result)
        return result


class History():

    def __init__(self, _history):
        """
       初始化原history.history对象
        """
        self._data = _history.history
        # print("__init__ History")
            
    @property
    def data(self):
        """
        获取原history.history中的数据，即训练历史数据
        """
        return self._data
        
    def plot(self):
        """
        提供plot方法，直接把历史数据绘制成折线图
        """
        if "acc" in self._data:
            plt.plot( self._data['acc'], label="acc" )
        if "val_acc" in self._data:
            plt.plot( self._data['val_acc'], label="val_acc" )
        plt.legend()
        plt.show()
