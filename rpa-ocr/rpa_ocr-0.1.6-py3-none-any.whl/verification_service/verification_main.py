# -*- coding:utf-8 -*-
# @author :adolf
import os
import yaml

from Identify_English.inference import CRNNInference


def ocr_pipeline_main(image_with_base64, scenes):
    config_path = os.path.join('verification_service/config', scenes + '.yaml')
    with open(config_path, 'r') as fp:
        config = yaml.load(fp.read(), Loader=yaml.FullLoader)

    with open(config['_BASE_'], 'r') as fp:
        base_config = yaml.load(fp.read(), Loader=yaml.FullLoader)

    # print(base_config)
    # print(config)
    # for key, value in base_config.items():
    #     base_config[key] = config[key]

    # print(base_config)
    res_str = CRNNInference(base_config).predict(image_with_base64)
    return res_str


if __name__ == '__main__':
    import base64
    import random

    img_path = '/home/shizai/adolf/data/jindie/EHHf.png'
    with open(img_path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), 'utf-8')

    ocr_predict = ocr_pipeline_main(image_base64, 'jindie')
    print(ocr_predict)

    img_p = '/home/shizai/adolf/data/jindie/'
    img_list = os.listdir(img_p)
    random.shuffle(img_list)
    total = 200
    positive = 0
    for img_name in img_list[:total]:
        with open(os.path.join(img_p,img_name), 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), 'utf-8')

        ocr_predict = ocr_pipeline_main(image_base64, 'jindie')
        # print(ocr_predict)
        # print(img_name)
        # print('---------')
        if ocr_predict == img_name.split('.')[0]:
            positive += 1
        else:
            print(img_name)
            print(ocr_predict)

    print('accuracy', positive / total)
