import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
import cv2
import matplotlib.pyplot as plt


def circle_detect(image, rangeR=(200, 250), total_num_peaks=1):
    """
    :param rangeR: detected circles' Radius range
    :param total_num_peaks: detect circles number
    return (accums, cx, cy, radii)"""
    # image = cv2.bilateralFilter(image, 21, 75, 75)
    image = cv2.medianBlur(image, 15)
    edges = canny(image, low_threshold=3, high_threshold=10)  # sigma=3,
    # plt.imshow(edges)
    # plt.show()
    hough_radii = np.arange(rangeR[0], rangeR[1], 2)
    hough_res = hough_circle(edges, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res,
                                               hough_radii,
                                               total_num_peaks=total_num_peaks)
    return accums, cx, cy, radii


if __name__ == "__main__":
    from guang.cv.video import getFrame
    import matplotlib.pyplot as plt
    from skimage.draw import circle_perimeter
    from skimage import color

    # dst = cv2.pyrMeanShiftFiltering(image, 10, 100)   #边缘保留滤波EPF
    fps, size_17, img = getFrame(
        filename=r'C:\Users\beidongjiedeguang\Desktop\实验\62.avi',
        frameNum=723,
    )
    image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    accums, cx, cy, radii = circle_detect(image,
                                          rangeR=[100, 250],
                                          total_num_peaks=1)
    image = color.gray2rgb(image)
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius)
        image[circy, circx] = (220, 20, 20)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(20, 10))
    ax.imshow(image, cmap=plt.cm.gray)
    plt.show()
