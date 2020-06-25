import sys,os,random
import cv2
import uiautomator2 as u2
import wda
import random
from PIL import Image
global img,original_img,img_path,Scale
global point1,point2,devices

def screen_shot(devices,save_img_path):
    global img_path
    img_path=save_img_path
    u=devices
    screen_image = 'image' + str(random.randint(1, 1000000)) + '.png'
    u.screenshot(screen_image)
    fullimage = cv2.imread(screen_image, 0)  # 去颜色
    a='fullscreen.png'
    b=save_img_path+a
    cv2.imwrite(b, fullimage)

    # hight, width = fullimage.shape
    # halfimage = fullimage[int(hight / 2):hight, 0:width]  # 扔掉屏幕上半部分
    # cv2.imwrite('F:/halfscreen.png', halfimage)
    #
    # os.remove(screen_image)


def on_mouse(event, x, y, flags, param):
    global img,original_img, point1, point2,img_path,Scale
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN: #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON): #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (200,0,0), 2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP: #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 2)
        cv2.imshow('image', img2)
        a = int(point1[0]) / Scale
        b = int(point2[0]) / Scale
        c = int(point1[1]) / Scale
        d = int(point2[1]) / Scale
        a = int(a)
        b = int(b)
        c = int(c)
        d = int(d)
        min_x = min(a, b)
        min_y = min(c, d)
        width = abs(a - b)
        height = abs(c - d)
        cut_img = original_img[min_y:min_y + height, min_x:min_x + width]
        a=random.randint(0, 100)
        a=str(a)
        b=img_path+'k'+a+'.png'
        print(b+'---------生成成功！')
        cv2.imwrite(b, cut_img)
        # cv2.imwrite('F:/k%s.png' % random.randint(0, 100), cut_img)
def crop():
    global img,original_img, point1, point2,img_path,Scale
    a='fullscreen.png'
    b=img_path+a
    img = cv2.imread(b,0)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    original_img=img
    # cv2.imshow('image', original_img)
    # cv2.waitKey(0)
    img=cv2.resize(img, (0, 0), fx=Scale, fy=Scale, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('image', img)
    cv2.waitKey(0)


def get_image(devices,save_img_path,scale):
    global Scale
    Scale=float(scale)
    screen_shot(devices,save_img_path)
    crop()

def element_click(devices,Prop,Value):
    if Prop=='xpath' or Prop=='XPath':
        devices.xpath(Value).click()
    else:
        a='devices('
        b='=Value).click()'
        c=a+Prop+b
        eval(c)

def element_is_exist(devices,Prop,Value):
    if Prop=='xpath' or Prop=='XPath':
        d=devices.xpath(Value).exists
    else:
        a='devices.exists('
        b='=Value)'
        c=a+Prop+b
        d=eval(c)
    return str(d)

def run_if(key,value):
    z='.'
    y=z in value
    y=str(y)
    if y=='True':
        x = value.split(".", 1)
        if key=='True':
            eval(x[1])
    else:
        if key=='True':
            print(value)
            eval(value)

def send_keys(devices,Prop,Value,msg):
    if Prop=='xpath' or Prop=='XPath':
        devices.xpath(Value).click()
    else:
        a='u2.connect_usb()('
        b='=Value).click()'
        c=a+Prop+b
        eval(c)
    u2.connect_usb().send_keys(msg,clear=True)


def devices_connect(device_type,devices):
    if device_type == 'android':
        if devices is None:
            u = u2.connect_usb()
        else:
            u = u2.connect(sys.argv[1])
    else:
        u = wda.Client(devices)
    return  u



# devices=devices_connect('android',None)
# save_img_path='F:/'
# get_image(devices,save_img_path,0.5)




# devices=devices_connect('android',None)
# a=element_is_exist(devices,'xpath','//*[@text="相机"]')
# # element_click('xpath','//*[@text="相机"]')
# run_if(a,'element_click("xpath","//*[@text="相机"]")')
# eval('element_click(device,"text","相机")')
# send_keys('xpath','//*[@resource-id="com.android.mms:id/embedded_text_editor"]','1777712')