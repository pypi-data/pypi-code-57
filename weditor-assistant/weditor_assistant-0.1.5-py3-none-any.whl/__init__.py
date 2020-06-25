import sys,os,random
import cv2
import uiautomator2 as u2
import wda
import random

global img
global point1, point2

def screen_shot(device_type,devices):
    if device_type == 'android':
        if devices is None:
            u = u2.connect_usb()
        else:
            u = u2.connect(sys.argv[1])
    else:
        u = wda.Client(devices)

    screen_image = 'image' + str(random.randint(1, 1000000)) + '.png'
    u.screenshot(screen_image)
    fullimage = cv2.imread(screen_image, 0)  # 去颜色
    cv2.imwrite('fullscreen.png', fullimage)

    hight, width = fullimage.shape
    halfimage = fullimage[int(hight / 2):hight, 0:width]  # 扔掉屏幕上半部分
    cv2.imwrite('halfscreen.png', halfimage)

    os.remove(screen_image)

def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN: #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON): #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (200,0,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP: #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5)
        cv2.imshow('image', img2)
        min_x = min(point1[0],point2[0])
        min_y = min(point1[1],point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] -point2[1])
        cut_img = img[min_y:min_y+height, min_x:min_x+width]
        cv2.imwrite('k%s.png'%random.randint(0,100), cut_img)
def crop():
    global img
    img = cv2.imread('halfscreen.png',0)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    cv2.waitKey(0)

def get_iamge():
    screen_shot('android',None)
    crop()

def element_click(Prop,Value):
    if Prop=='xpath' or Prop=='XPath':
        u2.connect_usb().xpath(Value).click()
    else:
        a='u2.connect_usb()('
        b='=Value).click()'
        c=a+Prop+b
        eval(c)


