import cv2
import matplotlib.pyplot as plt
import numpy as np


class Dist:
    '''input: vec1 , vec2 均为列向量'''
    @staticmethod
    def euclidean_dist(vec1, vec2):
        """欧氏距离:
        我们现实所说的直线距离"""
        if type(vec1) == list:
            vec1, vec2 = np.array(vec1), np.array(vec2)
        assert vec1.shape == vec2.shape

        return np.sqrt((vec2 - vec1).T @ (vec2 - vec1))

    @staticmethod
    def manhattan_dist(vec1, vec2):
        """曼哈顿距离:
        城市距离"""
        if type(vec1) == list:
            vec1, vec2 = np.array(vec1), np.array(vec2)
        assert vec1.shape == vec2.shape

        return sum(abs(vec1 - vec2))


def get_gradient(coord, img, delta=2):
    '''coord: [x,y] numpy array, img: gray image, dtype: float, if not :img/255
    get image gradient at specified coordinates 
    有没有可能这里的delta应该等于R
    '''
    H, W = img.shape
    if coord[0] < W - delta and coord[1] < H - delta:
        dh = img[coord[1], coord[0] + delta] - img[coord[1], coord[0]]
        dw = img[coord[1] + delta, coord[0]] - img[coord[1], coord[0]]
        mag = np.sqrt(dw * dw + dh * dh)
        return dh / delta, dw / delta, mag
    else:
        return 0, 0, 0


def get_randomPoint(refImage):
    h, w = refImage.shape[:2]
    x, y = np.random.randint(0, h), np.random.randint(0, w)
    return x, y


def get_point_color(coord, image):
    '''image: bgra channel
        coord: w,h array
    return  bgr color array'''
    bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    h, w = image.shape[:2]
    coord[0] = np.clip(coord[0], 0, h - 1)
    coord[1] = np.clip(coord[1], 0, w - 1)
    b, g, r = bgr[coord[0], coord[1], 0], bgr[coord[0], coord[1],
                                              1], bgr[coord[0], coord[1], 2]
    return np.array([b, g, r])


def makeSplineStroke(x0, y0, R, refImage, canvas):
    '''refImage: bgra channel
    取落笔时的颜色，绘制一个stroke
    '''
    strokeColor = get_point_color([y0, x0], refImage)
    K = []
    K.append([x0, y0])
    [x, y] = [x0, y0]
    [lastDx, lastDy] = [1e-6, 1e-6]

    minStrokeLength, maxStrokeLength = 10, 30
    gray_img = cv2.cvtColor(refImage, cv2.COLOR_BGR2GRAY)
    for i in range(maxStrokeLength):

        refColor = get_point_color([y, x], refImage)
        #         diff_1 = Dist.euclidean_dist(refColor, get_point_color([y,x], canvas))
        #         diff_2 = Dist.euclidean_dist(refColor, strokeColor)
        diff_1 = Dist.manhattan_dist(refColor, get_point_color([y, x], canvas))
        diff_2 = Dist.manhattan_dist(refColor, strokeColor)

        if i > minStrokeLength and (diff_1 < diff_2):
            return K

        gx, gy, gradientMag = get_gradient([x, y], gray_img / 255)
        # detect vanishing gradient
        #         print('gradientMag', gradientMag)
        if gradientMag == 0:
            return K
        # compute a normal direction
        dx, dy = -gy, gx
        # if necessary, reverse direction
        if lastDx * dx + lastDy * dy < 0:
            dx, dy = -dx, dy
        # filter the stroke direction
        fc = 1.
        dx = fc * dx + (1 - fc) * lastDx
        dy = fc * dy + (1 - fc) * lastDy

        dx, dy = dx / np.sqrt(dx * dx + dy * dy), dy / np.sqrt(dx * dx +
                                                               dy * dy)
        x, y = int(x + R * dx), int(y + R * dy)

        lastDx, lastDy = dx, dy
        K.append([x, y])

    return K


from IPython import display


def test():
    refImage = cv2.imread('temp/nuannuan.png')

    img = cv2.blur(refImage, (10, 10))
    canvas = np.zeros(refImage.shape).astype('uint8')
    R = refImage.shape[0] / 70  # -----------------------------
    for i in range(1500):
        x0, y0 = get_randomPoint(img)
        K = makeSplineStroke(x0, y0, R, img, canvas)

        color = get_point_color([y0, x0], img)
        b, g, r = color[0], color[1], color[2]

        b, g, r = int(b), int(g), int(r)

        for coord in K:
            circle = cv2.circle(canvas, (coord[0], coord[1]), 12, (r, g, b),
                                -1)

        if i % 50 == 0:
            display.clear_output(wait=True)
            plt.figure(figsize=(6, 6))
            plt.imshow(circle)
            plt.show()

    return circle


if __name__ == '__main__':

    circle = test()
