#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import imutils
import numpy as np
import time
import random
import os
from matplotlib import pyplot as plt

def checkSize(object):
	list_X=[object[0][0],object[1][0],object[2][0],object[3][0]]
	list_Y=[object[0][1],object[1][1],object[2][1],object[3][1]]
	minX=min(list_X)
	minY=min(list_Y)
	maxX=max(list_X)
	maxY=max(list_Y)
	height=maxY-minY
	weight=maxX-minX
	if((weight>height)&(weight*height<45000)&(0.3<height/weight<1.8)):
		
		return True
	else:
		return False

def PerspectiveTransform(object,img):
	pts1 = np.float32([object[0], object[3], object[1], object[2]])
	
	pts2 = np.float32([[0,0], [300,0], [0,150], [300,150]])

	M = cv2.getPerspectiveTransform(pts1, pts2)
	dst = cv2.warpPerspective(img, M, (300,150))

	return dst

def resetPoint(object):
	point=[object[0][0],object[1][0],object[2][0],object[3][0]]
	temp=[]
	temp=point
	for i in range(0,4):
		for x in range(i+1,4):
			if(temp[i][0]>point[x][0]):
				t=temp[i]
				temp[i]=point[x]
				point[x]=t
				break
	cv2.waitKey(0)
	if(temp[0][1]>temp[1][1]):
		tt=temp[0]
		temp[0]=temp[1]
		temp[1]=tt
	if(temp[2][1]<temp[3][1]):
		tt=temp[2]
		temp[2]=temp[3]
		temp[3]=tt

	return temp

def location(img):
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 5, 21, 21)

	kernel=np.ones((3,3),np.uint8)
	c=cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel)
	
	blur=cv2.GaussianBlur(c,(3,3),0)
	edged = cv2.Canny(blur, 15, 200)


	cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
	
	screenCnt = []
	#mask = np.zeros(gray.shape,np.uint8)
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		
		if len(approx)==4:
			screenCnt=resetPoint(approx)
			if(len(screenCnt)!=0):
				if(checkSize(screenCnt)):
					result=PerspectiveTransform(screenCnt,img)

					pts = np.array(screenCnt, np.int32)
					return [pts]


					#cv2.polylines(img, [pts], True, (0, 0, 255), 3)
					#cv2.imshow("result",img)
					#cv2.imwrite("./result/result_"+time.strftime("%Y%m%d%H%M%S", time.localtime())+str(random.random()*10)+".jpg",result)
					#print('success')
		
	

if __name__ == '__main__':
	
	cap=cv2.VideoCapture("rtsp://admin:admin@211.23.106.143:554/media?profile=h264")
	while(True):
		ret,frame=cap.read()
		if(ret):
			pts=location(frame)
			if(pts==None):
				frame=cv2.resize(frame,(640,480), interpolation = cv2.INTER_CUBIC)
			else:
				frame=cv2.polylines(frame, [pts], True, (0, 0, 255), 3)
				frame=cv2.resize(frame,(640,480), interpolation = cv2.INTER_CUBIC)
			cv2.imshow("result",frame)
			cv2.waitKey(100)



		else:
			break
	"""
	img=cv2.imread('./car/01_0099D.jpg')
	location(img)
	
	for filename in os.listdir(r"./car/traningData"):
		cv2.imshow("test","./car/traningData/"+filename)
	"""