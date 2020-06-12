import cv2
import numpy as np
import os
#轮廓检测
def Contour_Detection(img_file):
	img = img_file
	'''
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #转为灰度值图
	ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) #转为二值图
	#cv2.imshow('',binary)
	image , contours, hierarchy = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) #寻找轮廓
	#cv2.imshow("img",img) #显示原图像
	n=len(contours)       #轮廓个数
	#print('找到轮廓数量：',n)
	contoursImg=[]
	result = []
	for i in range(n):
		length = cv2.arcLength(contours[i], True)  #获取轮廓长度
		area = cv2.contourArea(contours[i])        #获取轮廓面积
		#print(type(contours))
		#print(contours)xcx
		#print('第{}个轮廓'.format(i)+'length['+str(i)+']长度=',length)
		#print('第{}个轮廓'.format(i)+"contours["+str(i)+"]面积=",area)
		tmp = {'contours':contours[i],'length':int(length) ,'area':int(area)}
		result.append(tmp)
		#temp=np.zeros(img.shape,np.uint8) #生成黑背景
		#contoursImg.append(temp)
		#contoursImg[i]=cv2.drawContours(contoursImg[i],contours,i,(0,255,255), 3)  #绘制轮廓
		#cv2.imshow("contours[" + str(i)+"]",contoursImg[i])   #显示轮廓
	print(result)
	cv2.waitKey()
	cv2.destroyAllWindows()
	return(result)
	'''
	imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh=cv2.threshold(imgray,127,255,0)
	image,contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#cv2.imshow('imageshow',image)  # 显示返回值image，其实与输入参数的thresh原图没啥区别
	#cv2.waitKey(0)
	return contours
_path = os.path.abspath( "resources/models" )

#实物轮廓检测
def Physical_Contour_Detection(img_file):
	#img = cv2.imread(img_file)
	img = img_file
	cv2.imshow("img",img)   #显示原图像
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      #转为灰度图
	ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  #转为二值图
	image, contours , opt= cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)#寻找轮廓
	print(len(contours))
	print(type(contours))
	print(contours)
	mask=np.zeros(img.shape,np.uint8)  #生成黑背景，即全为0
	mask=cv2.drawContours(mask,contours,-1,(255,255,255),-1)  #绘制轮廓，形成掩膜
	cv2.imshow("mask" ,mask)        #显示掩膜
	result=cv2.bitwise_and(img,mask)   #按位与操作，得到掩膜区域
	cv2.imshow("result" ,result)     #显示图像中提取掩膜区域
        
	cv2.waitKey()
	cv2.destroyAllWindows()
	return(contours)
        



