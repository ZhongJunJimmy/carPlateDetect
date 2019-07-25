#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np
img = cv2.imread('./W22207.jpg',cv2.COLOR_BGR2GRAY)
import matplotlib.pyplot as plt
import pdb

def verticalProjector(img):
	
	ret,thresh=cv2.threshold(GrayImage,130,255,cv2.THRESH_BINARY)  #圖片二值化（130,255）之間的點變為255（背景）
	(h,w)=thresh.shape
	a = [0 for z in range(0, w)] 

	#垂直投影
	for j in range(0,w):
		for i in range(0,h):
			if  thresh[i,j]==0:
				a[j]+=1
				thresh[i,j]=255
	for j  in range(0,w):
		for i in range((h-a[j]),h):
			thresh[i,j]= 0
	average=[]
	for k in range(4,len(a)):
		sum=0
		for l in range(k-4,k+1):
			sum+=a[l]

		average.append(sum/5)
	print(average)
	trough_point=[]
	crest_point=[]

	for m in range(0,len(average)):
		if m<len(average)-2:
			if((average[m-1]>average[m-2]) & (average[m]>average[m-1]) & (average[m]>average[m+1]) & (average[m+2]<average[m+1])):
				crest_point.append(m)

			if((average[m-1]<average[m-2]) & (average[m]<average[m-1]) & (average[m]<average[m+1]) & (average[m+2]>average[m+1])):
				#pdb.set_trace()
				trough_point.append(m)

	for n in range(0,len(trough_point)):
		print(n,a[n])
	for o in range(0,len(crest_point)):
		print(o,a[o])

	return thresh





	

def horizontalProjector(img):
	ret,thresh=cv2.threshold(GrayImage,130,255,cv2.THRESH_BINARY)  #圖片二值化（130,255）之間的點變為255（背景）
	(h,w)=thresh.shape
	#水平投影
	a = [0 for z in range(0, h)]
	for j in range(0,h):  
		for i in range(0,w):
			if  thresh[j,i]==0: 
				a[j]+=1 
				thresh[j,i]=255
	for j  in range(0,h):
		for i in range(0,a[j]):
			thresh[j,i]=0

	start=0
	start_state=0
	end=0
	end_state=0
	for i in range(0,len(a)):
		if (start_state==0) & (a[i]==0):
			if(a[i+1]!=0):
				start=i
				start_state=1
				i+=1

		if (start_state==1) & (end_state==0) & (a[i]==0):
			if(a[i+1]==0):
				end=i
				end_state=1
	crop_img = img[start:end, 0:300]
	return crop_img



GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #RGB 2 Gray


plt.figure(figsize=(10,5)) 
plt.suptitle('compare') 
plt.subplot(3,2,1), plt.title('GrayImage')
plt.imshow(GrayImage,cmap ='gray'), plt.axis('off')
plt.subplot(3,2,2), plt.title('horizontal')
plt.imshow(horizontalProjector(GrayImage),cmap ='gray'), plt.axis('off')
plt.subplot(3,2,3), plt.title('vertical')
plt.imshow(verticalProjector(horizontalProjector(GrayImage)),cmap ='gray'), plt.axis('off')

plt.show()