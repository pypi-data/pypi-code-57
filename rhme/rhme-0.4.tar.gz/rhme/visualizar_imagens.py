from rhme.config import Configuration
import numpy as np
import cv2
import os

config = Configuration()

number = np.load(config.package_path + '/tratamento/treated_data_three/not-number_testing_images.npz')
number = number['arr_0']
label_t = np.load(config.package_path + '/tratamento/treated_data_three/not-number_testing_labels.npz')
label_t = label_t['arr_0']
# label5 = label5['arr_0']

def exibir_imagem(image):
    for i in range(0, len(image), 100):
        cv2.imshow("Image", image[i])
        print(label_t[i])
        cv2.waitKey(0)

exibir_imagem(number)

cv2.destroyAllWindows()
