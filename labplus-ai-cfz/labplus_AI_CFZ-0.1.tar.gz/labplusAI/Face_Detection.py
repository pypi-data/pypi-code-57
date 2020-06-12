import cv2
import numpy as np
import os
def Face_Detection(img):
    _path = os.path.dirname(__file__)+'/resources/haarcascade_frontalface_default.xml'
    #print(_path)
    faceCascade = cv2.CascadeClassifier(_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,      
            minSize=(10, 10)
        )
    if(len(faces)==0):
        return []
    face_area = []
    result = []
    for i in range(faces.shape[0]):
        area = faces[i][2]*faces[i][3]
        face_area.append((i,area))
        face_area = sorted(face_area,key=lambda x: x[1],reverse=True)
    for i in face_area:
        index = i[0]
        result.append(faces[index].tolist())
    return result
