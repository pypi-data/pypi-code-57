from rhme.api import *
from rhme.config import Configuration
import base64
import numpy as np
import cv2

configs = Configuration()

class Example:

    def __init__(self):
        hme_recognizer = HME_Recognizer()

        # images = [configs.package_path + '/images/numbers/teste3.png', configs.package_path + '/images/numbers/teste4.png', configs.package_path + '/images/numbers/teste8.png', configs.package_path + '/images/numbers/teste10.png', configs.package_path + '/images/numbers/teste11.png']
        images = [
            configs.package_path + '/images/validacao/1.png', 
            configs.package_path + '/images/validacao/2.png', 
            configs.package_path + '/images/validacao/3.png'
        ]
        # with open(config.package_path + '/image.json') as json_file:
        #     labels_json = json_file.read()
        #     data = json.loads(labels_json)
        # img_data = data['image']
        # img_data = img_data.split(',')[1]
        # im_bytes = base64.b64decode(img_data)
        # im_arr = np.frombuffer(im_bytes, dtype=np.uint8) 
        # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    
        for image in images:
            try:
                expression, img = hme_recognizer.recognize(image)
                print("\nExpressão: ", expression)
            except Exception as e:
                print('Exception: ', e)

Example()
