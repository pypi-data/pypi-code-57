# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyolov3']

package_data = \
{'': ['*'], 'pyolov3': ['data/*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'torch==1.4.0',
 'torchvision==0.5.0',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'pyolov3',
    'version': '0.1.1',
    'description': 'A PyTorch implementation of the YOLO v3 object detection algorithm',
    'long_description': '# A PyTorch implementation of a YOLO v3 Object Detector\n\n[YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf)のPyTorch実装版です。  \n[ayooshkathuria/pytorch-yolo-v3](https://github.com/ayooshkathuria/pytorch-yolo-v3)の実装を活用させていただいています。\n\n## 導入方法\n\n```bash\npip install pyolov3\n```\n\n## 使い方\n\n- Webカメラを使ったサンプルコード\n\n```python\nimport cv2\n\nfrom pyolov3 import get_detector\n\nyolo = get_detector("coco", 0.5) # 使用したい学習済みモデルとConfidenceの閾値を設定\ncap = cv2.VideoCapture(0)\n\nwhile True:\n    ret, frame = cap.read()\n\n    detimg, result = yolo.detect(frame)\n    print(result)\n\n    cv2.imshow("test", detimg)\n\n    key = cv2.waitKey(1)\n    if key == ord("q"):\n        break\n\ncap.release()\ncv2.destroyAllWindows()\n```\n\n## 使用できる学習済みモデル\n\n現状は以下のモデルを指定できます。\n\n- [MS COCO](http://cocodataset.org/)\n  - 80クラス検出モデル\n  - `Detector("coco", confidence)`と指定\n- [Open Images Dataset](https://storage.googleapis.com/openimages/web/index.html)\n  - 600クラス検出モデル\n  - `Detector("openimages", confidence)`と指定\n- [WIDER FACE](http://shuoyang1213.me/WIDERFACE/)\n  - 顔検出モデル\n  - `Detector("widerface", confidence)`と指定\n',
    'author': 'reeve0930',
    'author_email': 'reeve0930@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reeve0930/pyolov3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
