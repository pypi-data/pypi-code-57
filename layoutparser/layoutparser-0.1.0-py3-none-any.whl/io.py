from .elements import *
import json, base64, cv2
import numpy as np
import pandas as pd 

def _load_json(filename):

    with open(filename, 'r') as fp:
        res = json.load(fp)    
    return res

def _load_base64_image(image_data):
    image_data = base64.b64decode(image_data)
    return cv2.imdecode(
                    np.fromstring(image_data, np.uint8),
                    cv2.IMREAD_COLOR
             )
    
def load_labelme_annotations(json_filename, image_filename=None,
                 label_map={}):
    
    json_file = _load_json(json_filename)
    
    layout = Layout()
    for ele in json_file['shapes']:
        
        if ele["shape_type"] == "rectangle":
            (x_1, y_1), (x_2, y_2) = ele['points']
            block = Rectangle(x_1, y_1, x_2, y_2)
        
        elif ele['shape_type'] == 'polygon':
            points = np.array(ele['points'])
            if points.shape != (4,2):
                raise NotImplementedError
            
            block = Quadrilateral(points)
        
        layout.append(
            TextBlock(block, type=label_map.get(ele['label'], ele['label']))
        )
    
    image = _load_base64_image(json_file['imageData']) if image_filename is None \
                else cv2.imread(image_filename)
    
    return layout, image

def load_csv(filename):
    
    df = pd.read_csv(filename)
    return Layout.from_dataframe(df)