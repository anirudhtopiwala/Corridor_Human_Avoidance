#!/usr/bin/env python
# coding: utf-8

# In[21]:


# Importing Libraries
import numpy as np
import cv2
import heapq
import math
import sys

class Find_Dist():
    # Class to find clearance distance
    
    # load_image() = This will take user input
    def load_image(self):
        dir =sys.argv[1]
#         dir = './human_corridor_0.txt'
        img = np.loadtxt(dir)
        return img
    
    # get_centroid() = This will first threshold the image,
    # by removing everything above 4 meteres and less than
    # 2 m, as it is given that human is generally 2m away.
    # The seconnd step is to locate the humana and get the 
    # centroid. This is done by identifying the three largest 
    # areas after cropping the image from bottom.
    
    def get_centroid(self,img):
        # Thresholding
        img[img<2] = 0 
        img[img>4] = 0
        # Cropping the image
        img[-25:,:] = 0
        mask = img.copy()
        mask[mask>0] = 255
        mask = mask.astype(np.uint8)
        # Finding the countour areas
        image, contours, hierarchy = cv2.findContours(mask,
                cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
        # Finding the largest area
        px = heapq.nlargest(1, zip(Area, Cx,Cy))[0][1]
        py = heapq.nlargest(1, zip(Area, Cx,Cy))[0][2]
        return px,py     
    
    # get_dist() = Getting the Clearance Distance 
    def get_dist(self,px,py,img):
        mat = img[py,:]
        ileft= []
        iright = []
        pnew =0
        for i in range(25):
            if (abs(mat[px+i+1]- mat[px+i])>0.5):
                iright.append(px+i)

            if (abs(mat[px-i]- mat[px-i-1])>0.5):
                ileft.append(px-i)
        diffpixel = px - 88
        if diffpixel > 0:
            state = "left "
            pnew = ileft[0]
        else:
            state = "right "
            pnew = iright[0]
        dist =  0.75 + abs(img[py,pnew]*math.sin((70*math.pi*diffpixel)/(176*180)))
        return dist,state
    

if __name__ == '__main__':
    c= Find_Dist()
    img = c.load_image()
    px,py = c.get_centroid(img)    
    clearance, state = c.get_dist(px,py,img)
    print(state + str(clearance))

