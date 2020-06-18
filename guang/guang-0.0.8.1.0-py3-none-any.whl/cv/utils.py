import numpy as np
import cv2
import matplotlib.pyplot as plt


def rotate(image, angle, center=None, scale=1.0):
    """Rotate the image angle degrees.
    if the center is None, initialize it as the center of
    the image
    """
    (h, w) = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


def rotate_bound(image, angle):
    """Keep the boundary and rotate angle degrees clockwise"""
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    return cv2.warpAffine(image, M, (nW, nH))


def auto_canny(image, sigma=0.33):

    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    return edged


def cvtBlackWhite(fileName):
    '''
    convert image's black color to white and meanwhile convert white to black.
    '''
    img = cv2.imread(fileName, 0)
    img = 255 - img
    cv2.imwrite('convert_' + fileName, img)


def cvt2rgb(img, channel='bgr'):
    '''it can convert image channel BGR,BGRA,HLS,HSV to RGB'''
    if channel == 'bgr' or channel == 'BGR' or channel == 'BGRA':
        print('bgr', img.shape)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif channel == 'HLS' or channel == 'hls':
        img = cv2.cvtColor(img, cv2.COLOR_HLS2RGB)
    elif channel == 'HSV' or channel == 'hsv':
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    else:
        return 'bad channel'
    return img


def myplot(img, channel='bgr'):
    ''' can show image channel BGR,BGRA,HLS,HSV.
    if RGB, set channel = 0'''
    if channel:
        img = cvt2rgb(img, channel)
    plt.figure(figsize=(7, 7))
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    pass
