import xml.etree.ElementTree as ET


def read_objects(file_path):
    # print(file_path)
    tree = ET.parse(file_path)
    label_items = {}
    object_items = []
    for elem in tree.iter():
        # 属性值
        if 'filename' in elem.tag:
            label_items['file_name'] = elem.text
        elif 'object' in elem.tag:
            xmin = -100
            ymin = -100
            xmax = -100
            ymax = -100
            name = None
            find = False
            for attr in list(elem):
                if 'bndbox' in attr.tag:
                    xmin = int(round(float(attr.find('xmin').text)))
                    ymin = int(round(float(attr.find('ymin').text)))
                    xmax = int(round(float(attr.find('xmax').text)))
                    ymax = int(round(float(attr.find('ymax').text)))
                    find = True
                elif 'name' in attr.tag:
                    name = attr.text
            if find:
                object_item = {'box': (xmin, ymin, xmax, ymax), 'name': name}
                object_items.append(object_item)
    label_items['object'] = object_items
    return label_items
