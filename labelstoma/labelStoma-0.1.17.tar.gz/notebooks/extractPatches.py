import xml.etree.ElementTree as ET
from xml.dom import minidom
from imutils import paths
import os
import cv2
from sklearn.externals.joblib import Parallel, delayed
import numpy as np
import imutils


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generateXML(filename,outputPath,w,h,d,boxes):
    top = ET.Element('annotation')
    childFolder = ET.SubElement(top, 'folder')
    childFolder.text = 'images'
    childFilename = ET.SubElement(top, 'filename')
    childFilename.text = filename[0:filename.rfind(".")]
    childPath = ET.SubElement(top, 'path')
    childPath.text = outputPath + "/" + filename
    childSource = ET.SubElement(top, 'source')
    childDatabase = ET.SubElement(childSource, 'database')
    childDatabase.text = 'Unknown'
    childSize = ET.SubElement(top, 'size')
    childWidth = ET.SubElement(childSize, 'width')
    childWidth.text = str(w)
    childHeight = ET.SubElement(childSize, 'height')
    childHeight.text = str(h)
    childDepth = ET.SubElement(childSize, 'depth')
    childDepth.text = str(d)
    childSegmented = ET.SubElement(top, 'segmented')
    childSegmented.text = str(0)
    for box in boxes:
        (category, (x,y,wb,hb)) = box
        childObject = ET.SubElement(top, 'object')
        childName = ET.SubElement(childObject, 'name')
        childName.text = category
        childPose = ET.SubElement(childObject, 'pose')
        childPose.text = 'Unspecified'
        childTruncated = ET.SubElement(childObject, 'truncated')
        childTruncated.text = '0'
        childDifficult = ET.SubElement(childObject, 'difficult')
        childDifficult.text = '0'
        childBndBox = ET.SubElement(childObject, 'bndbox')
        childXmin = ET.SubElement(childBndBox, 'xmin')
        childXmin.text = str(x)
        childYmin = ET.SubElement(childBndBox, 'ymin')
        childYmin.text = str(y)
        childXmax = ET.SubElement(childBndBox, 'xmax')
        childXmax.text = str(x+wb)
        childYmax = ET.SubElement(childBndBox, 'ymax')
        childYmax.text = str(y+hb)
    return prettify(top)


def detectBox(image,box,xM,yM,wM,hM):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    (category,(x,y,w,h)) = box
    cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
    newmask = mask[yM:yM+hM,xM:xM+wM]

    cnts = cv2.findContours(newmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() or imutils.is_cv4()  else cnts[1]
    if(len(cnts)==0):
        return None

    brect = cv2.boundingRect(cnts[0])
    (_, _, wB, hB) = brect
    if float(wB)<0.3*float(w) or float(hB)<0.3*float(h):
        return None
    return (category,brect)


# Boxes is a list of boxes with the following format: (category,(x,y,w,h))
def detectBoxes(image,boxes,xM,yM,wM,hM):
    return [detectBox(image,box,xM,yM,wM,hM) for box in boxes if detectBox(image,box,xM,yM,wM,hM) is not None]


#
def readAndGenerateImage(imagePath,outputPath,sizeW,sizeH,stepW,stepH):


    image = cv2.imread(imagePath)
    (hI, wI) = image.shape[:2]
    name = imagePath.split(os.path.sep)[-1]
    labelPath = '/'.join(imagePath.split(os.path.sep)[:-1]) + "/"+name[0:name.rfind(".")] + ".xml"
    tree = ET.parse(labelPath)
    root = tree.getroot()
    objects = root.findall('object')
    #if(len(objects)<1):
    #    raise Exception("The xml should contain at least one object")
    mask = np.zeros(image.shape[:2], dtype="uint8")

    boxes = []
    for object in objects:
        category = object.find('name').text
        bndbox = object.find('bndbox')
        x = int(bndbox.find('xmin').text)
        y = int(bndbox.find('ymin').text)
        h = int(bndbox.find('ymax').text) - y
        w = int(bndbox.find('xmax').text) - x
        boxes.append((category, (x, y, w, h)))

    startY = 0
    i=0
    while (startY < hI):
        startX = 0
        while (startX < wI):
            if startX+sizeW<wI:
                if startY + sizeH < hI:
                    newboxes = detectBoxes(mask,boxes,startX,startY,sizeW,sizeH)
                    newimage = image[startY:startY+sizeH,startX:startX+sizeW]
                else:
                    newboxes = detectBoxes(mask, boxes,startX, hI-sizeH, sizeW, sizeH)
                    newimage = image[hI-sizeH:hI, startX:startX + sizeW]
            else:
                if startY+sizeH<hI:
                    newboxes = detectBoxes(mask,boxes, wI-sizeW, startY, sizeW, sizeH)
                    newimage = image[startY:startY + sizeH, wI-sizeW:wI]
                else:
                    newboxes = detectBoxes(mask,boxes, wI - sizeW, hI-sizeH, sizeW, sizeH)
                    newimage = image[hI-sizeH:hI, wI - sizeW:wI]
            cv2.imwrite(outputPath + "/" + str(i) + "_" + name[0:name.rfind(".")] + ".jpg",newimage)
            if (len(image.shape) == 3):
                d = 3
            else:
                d = 1
            file = open(outputPath + "/" + str(i) + "_" + name[0:name.rfind(".")] + ".xml", "w")
            file.write(generateXML(str(i) + "_" + name, outputPath, sizeW, sizeH, d, newboxes))
            file.close()
            i+=1
            startX += stepW
        startY += stepH
    os.remove(imagePath)
    os.remove(labelPath)


def generatePatches(inputPath,outputPath,sizeW,sizeH,stepW,stepH):
    imagePaths = list(
        paths.list_files(inputPath, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")))
    labelPaths = list(paths.list_files(inputPath, validExts=(".xml")))
   
    if (len(imagePaths) != len(labelPaths)):
        raise Exception("The number of images is different to the number of annotations")
    [readAndGenerateImage(x,outputPath,sizeW,sizeH,stepW,stepH) for x in imagePaths]
