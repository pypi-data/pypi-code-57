from guang.cv.MajorTone import *
import cv2
import matplotlib.pyplot as plt
from skimage import data
from skimage.transform import match_histograms


def histogramMatching():
    reference = data.coffee()
    image = data.chelsea()

    matched = match_histograms(image, reference, multichannel=True)

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1,
                                        ncols=3,
                                        figsize=(8, 3),
                                        sharex=True,
                                        sharey=True)
    for aa in (ax1, ax2, ax3):
        aa.set_axis_off()

    ax1.imshow(image)
    ax1.set_title('Source')
    ax2.imshow(reference)
    ax2.set_title('Reference')
    ax3.imshow(matched)
    ax3.set_title('Matched')

    plt.tight_layout()
    plt.show()


def generateBackGround(img, show_plot=1):
    '''
    input: BGR image array
    return: a background image ,has the same shape with input image.
    '''
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w, _ = img.shape
    feature = cv2.resize(img, dsize=(40, 40))
    color1 = MajorTones.getCenters(feature, n_cls=2, m_cls=1)[0][0]
    #     color2 = MajorTones.getCentroid(feature, n_cls = 2)

    color = color1.astype('uint8')
    #     color = color2.astype('uint8')

    if show_plot:
        plt.figure()
        plt.subplot(121)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_HSV2RGB))
        plt.subplot(122)
        plt.imshow(
            cv2.cvtColor(color.reshape(1, 1, 3),
                         cv2.COLOR_HSV2RGB).reshape(1, 1, 3))
        plt.show()
    H, W = 55, 55
    gener_backg = np.ones((H, W, 3)).astype('uint8')
    gener_backg[:, :, 0] = gener_backg[:, :, 0] * color[0]  # H
    gener_backg[:, :, 1] = gener_backg[:, :, 1] * color[1]  # S
    gener_backg[:, :, 2] = gener_backg[:, :, 2] + 250  # V

    if show_plot:
        plt.figure()
        plt.imshow(cv2.cvtColor(gener_backg, cv2.COLOR_HSV2RGB))
        plt.show()

    i = 1
    c_max = gener_backg[i].max()
    R2 = H**2 + W**2
    for x in range(W):
        for y in range(H):
            r2 = (x - W / 2)**2 + (y - H / 2)**2  # 圆心转移到中心
            c = c_max * r2 // R2
            gener_backg[y, x, i] = c

    gener_backg = cv2.cvtColor(gener_backg, cv2.COLOR_HSV2RGB)
    gener_backg = cv2.resize(gener_backg, (h, w),
                             interpolation=cv2.INTER_NEAREST)
    if show_plot:
        plt.figure()
        plt.imshow(gener_backg)
        plt.show()

    return gener_backg


if __name__ == "__main__":

    def test_generateBackGround():
        img = cv2.imread("pic/hue1.png")
        generateBackGround(img, show_plot=1)

    # test_generateBackGround()
    histogramMatching()
