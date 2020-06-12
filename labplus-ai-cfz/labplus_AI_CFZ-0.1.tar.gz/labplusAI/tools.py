# coding=UTF-8
"""
import matplotlib.pyplot as plt
from skimage import io as skio
from skimage import transform
import pandas as pd
import shutil
import keras
from keras import layers
import time
import warnings
warnings.filterwarnings("ignore")
"""
import os, zipfile
import cv2
import json
import math
import requests
import time, datetime
import numpy as np
import pandas as pd
from PIL import Image
from skimage import io as skio

class video2image():

    def __init__(self, name='', image_resize=(30,30)):
        """
        video2image构造函数，传入名称name和目标图片尺寸image_resize
        """
        if name == '':
            self.name = str(int(time.time()))
        else:
            self.name = name
        self._path = self.name + "_imgs"
        self.image_resize = image_resize
        self.video_index = -1
        
        if os.path.exists(self._path):
            os.remove( self._path + "/config.json" )
            if os.path.exists(self._path + "/images"):
                for f in os.listdir( self._path + "/images" ):
                    fp = os.path.join( self._path, "images", f)
                    if os.path.isfile(fp):  os.remove( fp )
            else:
                os.mkdir( self._path + "/images" )
        else:
            os.mkdir( self._path )
            os.mkdir( self._path + "/images" )

        config = {}
        config["image_resize"] = self.image_resize

        with open(self._path + "/config.json", 'w') as f:
            json.dump(config, f)


    def set_video_label(self, source, label):
        """
        在当前目录下生成一个以 video2image.name 命名的文件夹,如./sig,文件夹结构如下：
        ./
            sig/
                config.json     # config文件中存储一些配置信息，如当前的image_resize值，label文本（按set_video_label执行顺序确定0、1、2....）
                images/
                    null_2020-5-12-10-10-10-0.png   # 考虑同一个标签多个视频文件，因此最终图片的命名规则为:  label_时间日期戳_序号.png
                    null_2020-5-12-10-10-10-1.png
                    .............................
        """
        if not os.path.exists(source):
            print("[video2image.set_video_label] file does not exist")
            return

        config = {}
        has_label = False
        if os.path.exists(self._path + "/config.json"):
            with open(self._path + "/config.json", 'r') as f:
               config = json.load(f)
            for index in range(self.video_index, -1, -1):
                key = "label_" + str(index)
                if key in config:
                    if label == config[key]:
                        has_label = True
                        break
        else:
            config["image_resize"] = self.image_resize
        
        if not has_label:
            self.video_index += 1
            config["label_" + str(self.video_index)] = label

        with open(self._path + "/config.json", 'w') as f:
            json.dump(config, f)

        cap = cv2.VideoCapture( source )
        frame_count = int(cap.get(7))

        now = datetime.datetime.now()
        timestamp = now.strftime("_%Y-%m-%d-%H-%M-%S_")
        temp_path = self.path() + "/images/" + label + timestamp
        for c in range(frame_count):
            ret,frame = cap.read()
            save_path = temp_path + str(c) + ".jpg"
            cv2.imencode('.jpg', frame)[1].tofile(save_path)
            img = Image.open(save_path)

            ratio = (img.size[0] * self.image_resize[1]) / (img.size[1] * self.image_resize[0])
            if ratio > 1:
                # 裁切x轴
                crop_len = int( (img.size[0] - (self.image_resize[0] * img.size[1] / self.image_resize[1]) ) / 2 )
                img = img.crop((crop_len, 0, img.size[0] - crop_len, img.size[1]))
            elif ratio < 1:
                # 裁切y轴
                crop_len = int( (img.size[1] - (self.image_resize[1] * img.size[0] / self.image_resize[0]) ) / 2 )
                img = img.crop((0, crop_len, img.size[0], img.size[1] - crop_len))
           
            img = img.resize( self.image_resize, Image.ANTIALIAS)
            img.save(save_path)
            print( "\r"+"progress label:[{}] {}/{}".format(label, c+1, frame_count), end="" ,flush=True)
        print("")

        
    def labels(self):
        """
        通过config获取标签文本列表
        """
        if os.path.exists(self._path + "/config.json"):
            with open(self._path + "/config.json", 'r') as f:
                config = json.load(f)
                _labels = []
                for index in range(self.video_index + 1):
                    key = "label_" + str(index)
                    if key in config: _labels.append(config[key])
                return _labels
        else:
            return []
        
    def path(self):
        """
        获取之前生成的文件夹绝对路径
        """
        return os.path.abspath(self._path)
        
    def data(self, shuffle=True):
        """
        将images文件夹下的图片读取为ndarray格式，最终返回一个元组(x,y),x、y都是ndarray
        shuffle参数默认为True，即需要打乱顺序
        """
        config = None
        with open(self._path + "/config.json", 'r') as f:
            config = json.load(f)
        
        if config is None: return None, None

        _dict = {}
        for index in range(self.video_index + 1):
            key = "label_" + str(index)
            if key in config: _dict[config[key]] = index

        imglist = []
        labellist = []
        for imgpath in os.listdir(self._path + "/images"):
            img = skio.imread(os.path.join(self._path, "images", imgpath))
            imglist.append(img)
            _label = imgpath.split("_")[0]
            if _label in _dict: labellist.append(_dict[_label])

        x_data = np.array(imglist)
        y_data = np.array(pd.get_dummies(np.array(labellist)))
        x_data = x_data/255

        if shuffle:
            indices = np.arange(x_data.shape[0])
            np.random.shuffle(indices)
            x_data = x_data[indices]
            y_data = y_data[indices]

        return x_data, y_data


class npu_predict():

    def unzip_single(self, src_file, dest_dir, password):
        """
        解压单个文件到目标文件夹。
        """
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()

    def unzip_all(self, source_dir, dest_dir, password):
        if not os.path.isdir(source_dir):    # 如果是单一文件
            self.unzip_single(source_dir, dest_dir, password)
        else:
            it = os.scandir(source_dir)
            for entry in it:
                if entry.is_file() and os.path.splitext(entry.name)[1]=='.zip' :
                    self.unzip_single(entry.path, dest_dir, password)

    def __init__(self, h5_model, test_image):
        """
        传入h5文件和一张图片，完成模型转换
        模型转换完成后，在当前目录下生成一个文件夹：npu_[modelname],把二进制文件保存到该文件夹下，具体结构如下：
        ./
            npu_modelname/  #其中modelname通过传入h5_path的文件名确定
                test_image.png
                config.json #保存模型输入尺寸信息
                xxxxxx      #转换好的模型以及可执行程序文件等
        """
        self.h5_model = h5_model
        self.test_image = test_image

        modelname,_ = os.path.splitext(os.path.basename(h5_model))
        npu_path = modelname + "_npu"

        if not os.path.exists(npu_path):
            os.mkdir( npu_path )
        
        img = Image.fromarray(np.uint8(test_image*255))
        img.save( npu_path + "/test_image.jpg")

        config = {}
        config["image_size"] = img.size

        with open( npu_path + "/config.json", 'w') as f:
            json.dump(config, f)

        url = 'http://cfz.labplus.cn:8089/api/uploadConvertModel'
        data = {
            "model_name": modelname,
            "dateTime": int(time.time())
        }
        img_file = open( npu_path + "/test_image.jpg", "rb")
        model_file = open( h5_model, "rb")
        print(img_file)
        print(model_file)
        files = [
            ("file", ("0_0.png", img_file)), 
            ("file", ("model.pb", model_file))
        ]

        # headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        response = requests.post(url, data, files=files, timeout=50)
        response.encoding = "utf-8"
        with open(npu_path + '/{}.zip'.format(modelname), "wb") as f:
            for bl in response.iter_content(chunk_size=1024):
                if bl:
                    f.write(bl)
        #print(response.text)

        # 判断源路径是否合法
        if not os.path.exists(npu_path):
            print("压缩文件或压缩文件所在路径不存在！")
            exit()
        if not os.path.isdir(npu_path) and not zipfile.is_zipfile(npu_path):
            print("指定的源文件不是一个合法的.zip文件！")
            exit()
    
        # 如果解压到的路径不存在，则创建     
        if not os.path.exists(npu_path):
            os.mkdir(npu_path)

        self.unzip_all(npu_path, npu_path, '')
        # print('转换成功!')
        print("__init__ npu_predict")

    def predict(self, frame):
        """
        执行二进制文件进行前向预测。传入的是frame，即ndarray格式
        ->[0.534,0.323,0.143}]
        对于传入的frame，需要先根据模型输出尺寸进行resize，然后进行前向预测，最后输出向量即可
        """
        print("Basic_CNN.predict")
        return {}
