from rhme import helpers
import numpy as np
import cv2
import imutils
import os

class ProcessamentoImagem:

    def __init__(self, configs={}):
        self.configs = {
            'black': False,
            'dilate': False,
            'dataset': False,
            'erode': False,
            'resize': 'smaller'
        }

        if configs:
            self.configs.update(configs)

    def print_bounding_box(self, image, coordinates):
        image_rect = image
        x, y, w, h = coordinates
        cv2.rectangle(image_rect,(x,y),(x+w,y+h),(100,100,100),2)
        # helpers.exibir_imagem(image_rect)
        return image_rect
        
    def save_image_255(self, image, name):
        img = cv2.convertScaleAbs(image, alpha=(255.0))
        cv2.imwrite('%s.jpg' % name, img)

    def to_gray_denoise(self, image):
        img = image.copy()

        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.fastNlMeansDenoising(img, None, 5, 9)
        img = np.array(img)

        return img

    def invert(self, image):
        img = image.copy()
        return 255-img

    def binarization(self, image):
        img = image.copy()
        img = self.invert(img)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        img = self.invert(img)
        return img

    def normalizar(self, image):
        img = image.copy()
        img = self.to_gray_denoise(image)

        if not self.configs['black']:
            img = self.invert(img)

        kernel = np.ones((2,2),np.uint8)

        if 'dilate' in self.configs:
            if self.configs['dilate']:
                img = cv2.dilate(img, kernel, iterations = 2)

        if 'erode' in self.configs:
            if self.configs['erode']:
                img = cv2.erode(img, kernel, iterations = 1)

        return img

    def _255_to_1(self, image):
        img = image.copy()
        return (img / 255)

    def redimensionar(self, image):
        old_size = image.shape[:2] # (height, width)
        height, width = old_size[0], old_size[1]

        ratio = float(26) / max(old_size)
        size = tuple([int(x*ratio) for x in old_size])

        size_height, size_width = size[0], size[1]

        division_height = int(height/2)
        division_width = int(width/2)

        middle_height = [
            image[division_height-1][division_width],
            image[division_height][division_width],
            image[division_height+1][division_width]
        ]
        middle_width = [
            image[division_height][division_width-1],
            image[division_height][division_width],
            image[division_height][division_width+1]
        ]

        if size_height <= 14 and size_width >= 20 and \
            (any(i > 0.0000 for i in middle_height) or any(i > 0.0000 for i in middle_width)):
            # For horizontal line
            nsize = 5 if size_height < 5 else size_height
            new_size = tuple([int(nsize), 26])
        else:
            if size_width / size_height >= 2:
                # For rectangle (sqrt)
                print('ractangle')
                kernel = np.ones((2,2),np.uint8)
                image = cv2.dilate(image, kernel, iterations = 20)
                xinit = int(width * 2 / 100)
                xend = int(width * 65 / 100)
                image = image[0:height, xinit:xend]

            new_size = size

        if self.configs['resize'] == 'smaller':
            image = cv2.resize(image.copy(), (new_size[1], new_size[0]), interpolation=cv2.INTER_AREA)
        elif self.configs['resize'] == 'bigger':
            image = cv2.resize(image.copy(), (new_size[1], new_size[0]), interpolation=cv2.INTER_LINEAR)

        # Cria borda ao redor do símbolo e normaliza para 28x28 px
        delta_w = 28 - new_size[1]
        delta_h = 28 - new_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)
        color = [0, 0, 0]
        image = cv2.copyMakeBorder(image.copy(), top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return image

    def resize_full_image(self, image):
        h, w = image.shape[:2]
        if w > 4000:
            width = w * 20 / 100
            r = width / float(w)
            size = (width, int(h * r))
            image = cv2.resize(image, size)
        return image

    def segmentar(self, img):
        image = img.copy()
        symbols = []
        cnts, somethingElse = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(cnts)):
            if(cv2.contourArea(cnts[i]) < 0):
                continue

            if(self.configs['dataset'] and len(cnts) > 1):
                continue

            try:
                # Draw contour in new image (mask)
                mask = np.zeros_like(image)
                cv2.drawContours(mask, cnts, i, (255, 255, 255), -50)
                out = np.zeros_like(image)

                # nas posições onde a máscara é 255, pinta as posições de normalized com as mesmas de mask 255
                # mask tem a parte interna do "2" pintada, mas o normalized não tem
                # mudei para > 0 em vez de 255 - isso evita que a imagem precise ser binarizada
                out[mask > 0] = image[mask > 0]

                # # Get bounding box coordinates
                _x, _y, _w, _h = cv2.boundingRect(cnts[i])

                # Por enquanto, não serve pra nada. Já tenho a informação ali em cima
                list_y, list_x = np.where(out > 0) #Diz TODOS os pontos onde a máscara == 255 | > 0
                (topx, topy) = (np.min(list_x), np.min(list_y))
                (bottomx, bottomy) = (np.max(list_x), np.max(list_y))

                # Crop image
                ycrop = _y + _h + 1
                xcrop = _x + _w + 1
                cropped = out[_y: ycrop, _x: xcrop]

                resized = self.redimensionar(cropped)
                result_image = self._255_to_1(resized)

                attributes = {
                    'index': i,
                    'image': result_image.copy(),
                    'xmin': _x,
                    'xmax': _x+_w,
                    'ymin': _y,
                    'ymax': _y+_h,
                    'w': _w,
                    'h': _h,
                    'centroid': [(_x + (_x+_w))/2, (_y + (_y+_h))/2]
                }

                symbols.append(attributes)

                mask = None
                out = None
                cropped = None
                resized = None
                binarized = None
                result_image = None

                self.image = self.print_bounding_box(image, (_x, _y, _w, _h))

            except BaseException as e:
                print(e)
                continue

        return (symbols, self.image)

    def mnist(self, img):
        try:
            if type(img) is str:
                image = cv2.imread(img)
            else:
                image = img

            normalizard = self.normalizar(image)
            result_image = self._255_to_1(normalizard)
            return result_image
        except BaseException as e:
            print(e)
            return None

    def tratamento_sem_segmentar(self, img):
        try:
            if type(img) is str:
                image = cv2.imread(img)
            else:
                image = img

            normalizard = self.normalizar(image)
            resized = self.redimensionar(normalizard)
            result_image = self._255_to_1(resized)
            return result_image
        except BaseException as e:
            print(e)
            return None

    def tratamento(self, img):
        try:
            if type(img) is str:
                image = cv2.imread(img)
            else:
                image = img

            original = image.copy()
            image = self.resize_full_image(image)
            normalizard = self.normalizar(image)
            self.image = normalizard.copy()

            symbols = self.segmentar(normalizard)

            return symbols
        except BaseException as e:
            print(e)
            return []

if __name__ == "__main__":

    p = ProcessamentoImagem()
    segmentacao, image = p.tratamento('images/numbers/teste10.png')

    try:
        for s in segmentacao:
            s.__delitem__('image')
    except Exception as identifier:
        print(identifier)

    print(segmentacao)
