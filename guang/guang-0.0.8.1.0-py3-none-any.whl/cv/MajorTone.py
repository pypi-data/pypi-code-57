# import sys,os
# sys.path.append(os.getcwd())
from guang.Utils.toolsFunc import sort_count

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
# from sklearn.cluster import k_means
from PIL import Image
import colorsys

import cv2


class MajorTones:
    @staticmethod
    def preProces(imgName):
        ''' 简单预处理下'''
        feature = Image.open(imgName)
        feature = feature.convert("RGB")
        try:
            # resize一下,提高速度
            feature = feature.resize((150, 150))
            feature = np.array(feature)
            # 因为有的图片色彩通道是4个
            feature = feature[:, :, :3]

            if feature.dtype == 'uint8':
                feature = feature / 255.
        except:
            print(f'打开图片失败, 跳过该图片：{imgName}')
            return []

        return feature

    @staticmethod
    def plot_simgle_sample(img_path, n_cls=2):
        '''测试k_means效果'''
        km = KMeans(n_clusters=n_cls)
        plt.subplot(1, 3, 1)
        plt.imshow(Image.open(img_path))
        # 主基调图片
        keynote = MajorTones.preProces(img_path)
        plt.subplot(1, 3, 2)
        plt.imshow(keynote)
        h, w, channel = keynote.shape
        keynote = km.fit(keynote.reshape(h * w, channel))

        plt.subplot(1, 3, 3)
        plt.imshow(keynote.cluster_centers_.reshape(n_cls, 1, 3))
        plt.show()
        print(keynote.cluster_centers_)

    @staticmethod
    def getCenters(feature, n_cls, m_cls):
        '''获得多个色彩聚类中心, n_cls = kmeans中的k个聚类
        m_cls： 它接受两中类型的值：
        如果它的值是整数，则表示返回k个聚类中的前m个聚类
        如果它的值是0~1之间的浮点数，如0.5,则它会返回前百分之五十的聚类结果
        output:
        key_centers: 返回前m个类的中心坐标
        key_percent: 返回的key_centers中各个元素所占的比例
        '''
        import warnings
        warnings.filterwarnings('ignore')
        (h, w, channel) = feature.shape
        feature = feature.reshape(h * w, channel)
        res = KMeans(n_clusters=n_cls).fit(feature)
        predict = res.predict(feature)
        cluster_centers = res.cluster_centers_
        predict = sort_count(predict)  # [(2,5),(cluster, counts)...]

        # 可能聚类结果没有达到n_cls设定值，这里重新赋值
        n_cls = len(predict)
        pred_idx, counts = [predict[i][0] for i in range(n_cls)
                            ], [predict[i][1] for i in range(n_cls)]
        Totle = sum(counts)
        # print(predict)
        if type(m_cls) == int:
            # 这里m_cls也是一样
            if m_cls > n_cls:
                m_cls = n_cls

            key_predict = predict[:m_cls]
            key_idx, _ = [key_predict[i][0] for i in range(m_cls)
                          ], [key_predict[i][1] for i in range(m_cls)]

        elif 0 < m_cls < 1:
            S = 0
            for i, _ in enumerate(counts):
                S += _
                if S / Totle >= m_cls:
                    break
            key_idx = pred_idx[:i + 1]
        else:
            raise ' '
        # print(key_idx)
        key_centers = cluster_centers[key_idx]
        count_percent = np.array(counts) / Totle
        key_percent = count_percent[:len(key_idx)]  # key_percent储存返回的类所占的比例
        return key_centers, key_percent

    @staticmethod
    def getCentroid(feature, n_cls=2):
        '''获取主色调的RGB值
        inputParam: 
        feature: 3D rgb array
        n_cls: Please keep it unchanged
        '''
        (h, w, channel) = feature.shape
        feature = feature.reshape(h * w, channel)
        res = KMeans(n_clusters=n_cls).fit(feature)
        L = len(res.labels_)

        #　选取较多的那个簇
        if L - np.count_nonzero(res.labels_) > L / 2: flag = 0
        else: flag = 1
        feature = feature[res.labels_ == flag]
        # 进行第二次聚类
        res = KMeans(n_clusters=n_cls).fit(feature)
        L = len(res.labels_)
        if L - np.count_nonzero(res.labels_) > L / 2: flag = 0
        else: flag = 1

        return res.cluster_centers_[flag]

    @staticmethod
    def get_dominant_color(image):
        '''从网上down来的,运算量较小,可能适用于某些场景,
        至于适用于哪些,我咋知道
        '''
        image = Image.open(image)
        #颜色模式转换，以便输出rgb颜色值
        image = image.convert('RGBA')
        #生成缩略图，减少计算量，减小cpu压力
        image.thumbnail((200, 200))
        max_score = 0
        dominant_color = 0
        for count, (r, g, b,
                    a) in image.getcolors(image.size[0] * image.size[1]):
            # 跳过纯黑色
            if a == 0:
                continue
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0,
                                             b / 255.0)[1]
            y = min(
                abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue
            # Calculate the score, preferring highly saturated colors.
            # Add 0.1 to the saturation so we don't completely ignore grayscale
            # colors by multiplying the count by zero, but still give them a low
            # weight.
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
        return np.array(dominant_color)

    @staticmethod
    def process_batch_image(img_list,
                            algorithm='centroid',
                            show_plot=0,
                            **dict):
        '''
        input: 
        output: img_list的聚类中心列表
        当algorithm = 'mult_centers'时， dict需要给到值 ，如n_cls = 12, m_cls = 5
        '''

        Center_batch_image = []
        for i, img in enumerate(img_list):
            try:
                feature = MajorTones.preProces(img)
            except:
                print(f'文件{img}处理出错，以跳过')
                Center_batch_image.append(np.array(
                    [2, 2, 2]))  # 添加一个(2,2,2)数组到Center中占位，以表示出错
                continue

            if len(feature) == 0:  # 无效图片
                Center_batch_image.append(np.array(
                    [2, 2, 2]))  # 添加一个(2,2,2)数组到Center中，以表示出错
                continue
            # ================================================================
            if algorithm == 'centroid':
                centroid = MajorTones.getCentroid(feature)
                Center_batch_image.append(centroid)
            elif algorithm == 'mult_centers':
                centers, percent_centers = MajorTones.getCenters(
                    feature, dict['n_cls'], dict['m_cls'])
                Center_batch_image.append(
                    (centers, percent_centers))  # 列表中每个元素是一个元组
            elif algorithm == 'other':
                centroid = MajorTones.get_dominant_color(img)  # other
                Center_batch_image.append(centroid)
            # ================================================================
            proces_percent = (i + 1) / len(img_list) * 100
            print(f'\r{proces_percent:.1f}%已完成', end='')
            if show_plot:
                plt.subplot(1, 2, 1)
                h, w, c = feature.shape
                plt.imshow(feature.reshape(h, w, c))
                plt.subplot(1, 2, 2)
                if algorithm == 'mult_centers':
                    plt.imshow(centers.reshape(len(centers), 1, 3))
                else:
                    plt.imshow(centroid.reshape(1, 1, 3))
                plt.title(f'{i}')
                plt.show()
                print(60 * '*')

        # print('processing complete')
        return Center_batch_image
