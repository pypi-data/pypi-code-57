import os
from random import sample
import pickle

import torch

from .models.mtcnn import MTCNN
from .models.inception_resnet_v1 import InceptionResnetV1

class FaceDetection():
    def __init__(self, mtcnn=None, inception_net=None, db=None):

        self.facedb = FaceDatabase(db)
        # path of pretrained weights
        self.saved_models = './saved_models'

        # in models are not passed through init, load it
        # from the saved_models dir.
        if mtcnn is not None:
            self.mtcnn = mtcnn
        else:
            self.mtcnn = MTCNN()

        if inception_net is not None:
            self.inception_net = inception_net
        else:
            self.inception_net = InceptionResnetV1(pretrained='vggface2',
                                                   path=self.saved_models)

    def detect_faces(self, img):
        """
        Detect all faces in PIL image and return the
        bounding boxes and facial landmarks
        """

        boxes, probs, points = self.mtcnn.detect(img, landmarks=True)
        return boxes, probs, points


    def add_person(self, name, img):
        """
        Add a person for detection
        """

        # crop the face using mtcnn
        face_img = self.mtcnn(img)
        self.facedb.add(name, face_img)

    def recognise_face(self, img, threshold=1.3):
        input_face = self.mtcnn(img).unsqueeze(0)
        faces_in_db, names = self.facedb.get_batched()
        faces_stacked = torch.stack(faces_in_db)
        concat = torch.cat((input_face, faces_stacked), dim=0)
        face_vectors = self.inception_net(concat)

        input_face_vec, faces_from_db_vec = face_vectors[:1], face_vectors[1:]

        # calculate the norm and then create a mask of the vectors that
        # are less than the threshold.
        mask = (input_face_vec - faces_from_db_vec).norm(dim=1) < threshold
        vals, indx = mask.view(-1, 5).sum(dim=1).topk(k=1)

        accuracy = vals.item()/5
        name = names[indx.item()]
        return name, accuracy

    def all_names(self, only_incomplete=False):
        complete, incomplete = self.facedb.all_names()
        if only_incomplete:
            return incomplete
        return complete, incomplete


class FaceDatabase():
    """
    Class that acts as the database to store
    the saved aligned faces
    """
    def __init__(self, db_file=None):
        if db_file is None:
            print('init new db')
            self.db_file = './faces_db.fdb'
            self.database = dict()
        else:
            print('loading db...')
            self.db_file = db_file
            self._load()

    def _save(self):
        with open(self.db_file, 'wb') as f:
            pickle.dump(self.__dict__, f)
            print('saved db')

    def _load(self):
        with open(self.db_file, 'rb') as f:
            state_dict = pickle.load(f)
            self.__dict__.update(state_dict)
            print(f'loaded {self.db_file}')

    def add(self, name, img_tensor):
        if name in self.database:
            self.database[name].append(img_tensor)
            print(f'Face {name} updated with new image')
        else:
            self.database[name] = [img_tensor]
            print(f'New face {name} added!')
        self._save()

    def get_batched(self):
        names = list()
        all_faces = list()
        for people in self.database.keys():
            faces = self.database[people]
            if len(faces) < 5:
                continue
            all_faces.extend(sample(faces, 5))
            names.append(people)
        return all_faces, names

    def all_names(self):
        # names with more than 5 pics
        names_complete = list()
        # names with less
        names_incomplete = list()

        for people in self.database.keys():
            faces = self.database[people]
            if len(faces) < 5:
                names_incomplete.append((people, len(faces)))
            else:
                names_complete.append((people, len(faces)))

        return names_complete, names_incomplete
