# Have to use custom impl of Hough Transform (separate from openCV) because
# of no access to the accumulator matrix
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
import sys

def setup(filename): 
    orig_img = cv2.imread(filename,)
    # get edges
    edges = cv2.Canny(orig_img, threshold1 = 0, threshold2 = 50, apertureSize = 3)

    return edges

def test2():
    print "hello"
# http://nabinsharma.wordpress.com/2012/12/26/linear-hough-transform-using-python/
def hough_transform(img_bin, theta_res=1.0, rho_res=1.0):
    nR, nC = img_bin.shape
    theta = np.linspace(-90, 0, int(np.ceil(90.0/theta_res)) + 1)
    theta = np.concatenate((theta, -theta[len(theta)-2::-1]))

    D = np.sqrt((nR - 1)**2 + (nC -1)**2)
    q = int(np.ceil(D/rho_res))
    nrho = 2*q + 1
    rho = np.linspace(-q*rho_res, q*rho_res, nrho)
    H = np.zeros((len(rho), len(theta)))

    for rowIdx in range(nR):
        for colIdx in range(nC):
            if img_bin[rowIdx, colIdx]:
                for thIdx in range(len(theta)):
                  rhoVal = colIdx * np.cos(theta[thIdx]*np.pi/180) + rowIdx*np.sin(theta[thIdx]*np.pi/180)
                  rhoIdx = np.nonzero(np.abs(rho-rhoVal) == np.min(np.abs(rho-rhoVal)))[0]
                  H[rhoIdx[0], thIdx] += 1

    return rho, theta, H


def gen_data(file_in, houghout):
    edges = setup(file_in)
    rho, theta, H = hough_transform(edges, theta_res=1.0, rho_res=1.0)
   
    # save accumulator matrix
    np.save(houghout, H)

if __name__ == '__main__':

    gen_data(sys.argv[1], 'hough.txt')
