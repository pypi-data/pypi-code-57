from rhme.reconhecimento import reconhecimento as reconhecimento
from rhme.processamento_imagem import preprocessamento as preprocessamento
from rhme.processamento_imagem import posprocessamento as posprocessamento
from rhme import helpers
import os
import re
import json
import numpy as np
import json
import cv2 as cv

helpers_labels = helpers.get_labels()
labels = helpers_labels['labels_parser']

class Recognize:

    def __init__(self, image):
        self.prediction=[]
        self.image = None

        try:
            if isinstance(image,str):
                nparr = np.fromstring(image, np.uint8)
                img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            else:
                img = image.copy()
            self.image = img
        except Exception as e:
            print("[recognize.py] __init__ | Exception:")
            raise e

    def __recognize(self, img):
        img = img.reshape(1, 28, 28, 1)
        return reconhecimento.fit(img)

    def to_recognize(self):

        expression = {}

        helpers.debug("[recognize.py] to_recognize | Exibindo imagem da expressão...\n")
        helpers.exibir_imagem(self.image)

        helpers.debug("[recognize.py] to_recognize | Iniciando pré-processamento de imagem...\n")
        p = preprocessamento.ProcessamentoImagem()
        segmentacao, normalized_image = p.tratamento(self.image)

        helpers.debug("[recognize.py] to_recognize | Exibindo imagem pré-processada\n")
        helpers.exibir_imagem(normalized_image)

        helpers.debug("[recognize.py] to_recognize | Pré-processamento de imagem finalizado.\n")

        helpers.debug("[recognize.py] to_recognize | Iniciando classificação dos símbolos...\n")
        try:
            for s in segmentacao:
                helpers.exibir_imagem(s['image'])
                reconhecer = self.__recognize(s['image'])
                reconhecer['label'] = str(reconhecer['label'])

                s['label'] = reconhecer['label']
                s['prediction'] = reconhecer['prediction']        

                symbol_prediction = {
                    'identity': labels[s['label']]
                }
                symbol_prediction.update(reconhecer)
                self.prediction.append(symbol_prediction)

                helpers.debug('[recognize.py] to_recognize | Símbolo: %s ' % labels[s['label']])
            helpers.debug("\n[recognize.py] to_recognize | << Classificação dos símbolos finalizada.\n")
        except Exception as e:
            print("[recognize.py] to_recognize | Exception:")
            raise e
            

        pos = posprocessamento.PosProcessamentoImagem(normalized_image)
        new = pos.segmentar_igualdade(segmentacao)

        # teste
        for n in new:
            print('label: ', n['label'])

        expression['symbols'] = new

        return (expression, normalized_image)
