#!/usr/bin/env python
# coding: utf-8

# In[49]:


import os
import numpy as np
# import matplotlib.pyplot as plt
import cv2
import heapq
import math
import sys


# In[50]:


class Find_Dist():
    # Finding clearance distance
    def load_image(self):
        dir =sys.argv[1]
        img = np.loadtxt(dir)
#         img = np.loadtxt('./human_corridor_1.txt')
#         plt.imshow(img)
        return img
#      Thresholfing image based on distance. Since human 
#         is almost always 2 m away. Removing any pixel information
#         less than 1.8 m and further away from 4m 
    def threshold_image(self,img):
        img[img<2] = 0 # make this in one line
        img[img>4] = 0
        img[-25:,:] = 0
#         plt.imshow(img)
        mask = img.copy()
        mask[mask>0] = 255
        mask = mask.astype(np.uint8)
#         plt.imshow(mask)
        image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        Area = []
        Cx = []
        Cy=[]
        for i in contours:
            # compute the center of the contour
            M = cv2.moments(i)
            if (M["m00"]!=0):
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if (cx>45 and cx< 122):
                    Cx.append(cx)
                    Cy.append(cy)
                    area = cv2.contourArea(i)
                    Area.append(area)
        px = heapq.nlargest(1, zip(Area, Cx,Cy))[0][1]
        py = heapq.nlargest(1, zip(Area, Cx,Cy))[0][2]
        return px,py     
    # getting the obstacle distance based on Horizontal FOV of 70 degrees
    def get_dist(self,px,py):
#         side = "right" if px < 88 else "left"
        diffpixel = px - 88
        dist = img[py,px]*math.sin((70*math.pi*diffpixel)/(176*180))
        return dist
if __name__ == '__main__':
    c= Find_Dist()
    img = c.load_image()
    px,py = c.threshold_image(img)
    dist = c.get_dist(px,py)
    state = []
    if (dist> 0):
        state = "left "
        clearance = 0.75+ abs(dist)
    else:
        state = "right "
        clearance = 0.75+abs(dist)
    print(state + str(clearance))
    


# In[ ]:




