# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:30:57 2020

@author: stvyh
as per: https://vagdevik.wordpress.com/2018/06/15/image-stitching/
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randrange

def stitching_two(img_1, img_2):
    """
    Parameters
    ----------
    img_1 : string 
         first image path+name
    img_2 : string
         second image path+name

    Returns
    -------
    stitched image if ok

    """
    img1 = cv2.imread(img_1)
 #   img1 = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)

    img2 = cv2.imread(img_2)
 #   img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    
    good = []
    for m in matches:
        if m[0].distance < 0.5*m[1].distance:
            good.append(m)
    matches = np.asarray(good)
    
    if len(matches[:,0]) >= 4:
        src = np.float32([ kp1[m.queryIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
        dst = np.float32([ kp2[m.trainIdx].pt for m in matches[:,0] ]).reshape(-1,1,2)
        H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        ok = 1
    else:       
        ok = 0
    
    dst = cv2.warpPerspective(img,H,(img.shape[1] + img.shape[1], img.shape[0]))
        
    return dst, ok

leftOne = 'C:/Temp/Data/Img/40v240h.bmp'
rightOne = 'C:/Temp/Data/Img/40v180h.bmp'
img = cv2.imread(leftOne)


dst, ok = stitching_two(rightOne, leftOne)
if ok:
    plt.subplot(122),plt.imshow(dst),plt.title("Warped Image")
    plt.show()
    plt.figure()
    dst[0:img.shape[0], 0:img.shape[1]] = img
    cv2.imwrite("C:/Temp/Data/Img/output.jpg",dst)
    plt.imshow(dst)
    plt.show()
else:
    print("Can’t find enough keypoints.") 