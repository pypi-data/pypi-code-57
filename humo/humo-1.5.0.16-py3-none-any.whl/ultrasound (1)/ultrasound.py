try:
    import cv2
except ImportError:
    print("OpenCV is not installed.")
    pass
try:
    from google.colab.patches import cv2_imshow
except ModuleNotFoundError:
    pass
import matplotlib.pyplot as plt
import numpy as np

class Video(object):
    def __init__(self, name):
        self.video = cv2.VideoCapture(name)
        self.delay = 1

    def getframe(self, num):
        return self.video.read(num)[1]

    def showframe(self, num):
        plt.imshow(self.getframe(num), cmap="gray")

    def gabor(self, scale1,scale2, theta, sigma, lambd, gamma):
        return cv2.getGaborKernel((scale1,scale2), sigma, np.radians(theta),lambd,gamma,0)

    def gabors(self,scales, theta1, theta2, sigma, lambd, gamma):
        gabors = []
        for scale in scales:
            gabors.append([cv2.getGaborKernel((scale,scale), sigma, np.radians(i),lambd,gamma,0) for i in np.linspace(theta1,theta2,8)])
        return gabors

    def getAngle(self, theta1, theta2):
        return np.linspace(theta1,theta2,8)

    def showgabors(self, num, scales, theta1, theta2,sigma, lambd, gamma):
        gabors = self.gabors(scales, theta1, theta2,sigma, lambd, gamma)
        for num, i in enumerate(gabors[num]):
            plt.subplot(4,4,num+1)
            plt.imshow(i, cmap="gray")

    def gaborfilt1(self,num,gabor):
        img = self.getframe(num)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dst = cv2.filter2D(gray, -1, gabor)
        return dst

    def gaborfilt2(self, img, gabor):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dst = cv2.filter2D(gray, -1, gabor)
        return dst

    def play(self):
        while True:
            ret, frame = self.video.read()
            if ret:
                cv2.imshow("movie", frame)
                if cv2.waitKey(self.delay) & 0xFF == ord("q"):
                    break 
            else:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cv2.destroyWindow("movie")

def getGaborKernels(scales, theta, sigma, lambd, gamma):
    gabors = []
    for scale in scales:
        for j in np.linspace(theta[1],theta[0],8):
            gabors.append(cv2.getGaborKernel((scale, scale), sigma, np.deg2rad(j), lambd, gamma, 0))
    return gabors

def designKernel(scale,theta,sigma,lambd,gamma,frame,test,mesh=False):
    from mpl_toolkits.mplot3d import Axes3D
    kernels = getGaborKernels(scale,theta,sigma,lambd,gamma)
    imgs = []
    for i in kernels:
        imgs.append(test.gaborfilt1(frame, i))
    imgs = np.array(imgs)
    maxmod = np.array([i.mean() for i in imgs]).argmax()%8
    maxmod # 第0列が最大振幅応答を持つ
    candidate = np.array([imgs[i] for i in range(32) if i%8 == maxmod])
    mincandidate = np.array([i.mean() for i in candidate]).argmin()
    maxcandidate = np.array([i.mean() for i in candidate]).argmax()
    target = np.abs(candidate[maxcandidate].astype(int) - candidate[mincandidate].astype(int))

    plt.figure(figsize=(25,35))
    plt.subplot(2,2,1)
    plt.title("original image",fontsize=15)
    plt.imshow(cv2.cvtColor(test.getframe(frame),cv2.COLOR_RGB2GRAY),cmap="gray")
    plt.subplot(2,2,3)
    plt.title("Max amplitude response",fontsize=15)
    plt.imshow(candidate[maxcandidate],cmap="gray")
    plt.subplot(2,2,4)
    plt.title("Min amplitude response",fontsize=15)
    plt.imshow(candidate[mincandidate],cmap="gray")
    plt.subplot(2,2,2)
    plt.title("Weighted image",fontsize=15)
    plt.imshow(target*20,cmap="gray")

    if mesh == True:
        x, y = np.arange(test.getframe(0).shape[1]), np.arange(test.getframe(0).shape[0])
        X, Y = np.meshgrid(x,y)

        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        ax.plot_wireframe(X, Y, candidate[maxcandidate])
        plt.show()

        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        ax.plot_wireframe(X, Y, candidate[mincandidate])
        plt.show()

        fig = plt.figure(figsize=(10,10))
        ax = Axes3D(fig)
        ax.plot_wireframe(X, Y, target)
        plt.show()
    else:
        pass

    plt.figure(figsize=(15,5))
    #plt.plot(target[300],label="diff image")
    plt.title("line 300", fontsize=(15))
    plt.plot(candidate[maxcandidate][300],label="max amplitude")
    plt.plot(candidate[mincandidate][300],label="min amplitude")
    plt.plot(np.abs(candidate[maxcandidate][300].astype(int) - candidate[mincandidate][300].astype(int)),label="difference")
    plt.legend()