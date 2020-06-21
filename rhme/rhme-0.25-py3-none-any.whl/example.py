from rhme.api import *
from rhme.config import Configuration
from rhme.helpers.exceptions import *
import base64
import numpy as np
import cv2

configs = Configuration()

class Example:

    def __init__(self):
        hme_recognizer = HME_Recognizer()

        # images = [configs.package_path + '/images/numbers/teste3.png', configs.package_path + '/images/numbers/teste4.png', configs.package_path + '/images/numbers/teste8.png', configs.package_path + '/images/numbers/teste10.png', configs.package_path + '/images/numbers/teste11.png']
        images = [
            # configs.package_path + '/images/validacao/5.png'
            # configs.package_path + '/images/validacao/21.png'
            # configs.package_path + '/images/validacao/24.png'
            # configs.package_path + '/images/validacao/25.png'
            # configs.package_path + '/images/validacao/28.png'
            # configs.package_path + '/images/validacao/29.png'
            # configs.package_path + '/images/validacao/40.png'
            # configs.package_path + '/images/validacao/41ue.png'
            # configs.package_path + '/images/validacao/42.png'
            # configs.package_path + '/images/validacao/44.png'
            # configs.package_path + '/images/validacao/45.png'
            # configs.package_path + '/images/validacao/46.png'
            # configs.package_path + '/images/validacao/47.png'
            configs.package_path + '/images/validacao/48.png'
            # configs.package_path + '/images/validacao/49.png'
            # configs.package_path + '/images/validacao/50.png'
            # configs.package_path + '/images/validacao/51.png'
        ]

        # with open(config.package_path + '/image.json') as json_file:
        #     labels_json = json_file.read()
        #     data = json.loads(labels_json)
        # img_data = data['image']
        # img_data = img_data.split(',')[1]
        # im_bytes = base64.b64decode(img_data)
        # im_arr = np.frombuffer(im_bytes, dtype=np.uint8) 
        # img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        expression=""
        for image in images:
            try:
                expression, img = hme_recognizer.recognize(image)
            except (GrammarError, SintaticError, LexicalError) as e:
                if 'latex_string_original' in e.data:
                    expression = e.data['latex_string_original']

            print("\nExpressão: ", expression)
Example()
