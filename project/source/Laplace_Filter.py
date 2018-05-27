# -*- coding: utf-8 -*-
"""
Created on Thu May 10 21:21:14 2018

Laplace Pyramid Blending of images. 
"""
import cv2
import numpy as np
from skimage.transform import resize as skresize

def constructGaussian(img, depth=6): 
    G = img.copy()
    GP = [G]
    for i in xrange(depth): 
        G = cv2.pyrDown(G)
        GP.append(G)
    return GP 
    
def constructLaplacian(gaussian_pyramid): 
    #Note, should be same as gaussian 
    lp = [gaussian_pyramid[-2]]
    for i in xrange((len(gaussian_pyramid) - 2), 0, -1): 
        GE = cv2.pyrUp(gaussian_pyramid[i])
        L = cv2.subtract(gaussian_pyramid[i-1], GE)
        lp.append(L)
    return lp


def Laplacian_blend(image1, image2, blending_filter):
    # filtrerer fra im1 til im2 ved hjelp av blending_filter
    # Gaussian pyr of images
    gp1 = constructGaussian(image1)
    gp2 = constructGaussian(image2)
    
    # Laplacians 
    lp1 = constructLaplacian(gp1)
    lp2 = constructLaplacian(gp2)
   
    
    #Apply filters ? 
    negative_filter = np.ones(blending_filter.shape) - blending_filter
    negative_filter_gaussian = constructGaussian(negative_filter)
    filter_gaussian = constructGaussian(blending_filter)
    LS = []
    for i in range(len(lp1)):
        ls = np.zeros(lp1[i].shape)
        filter_of_im1 = np.multiply(lp1[i], filter_gaussian[-(i+2)])
        negative_of_im2 = np.multiply(lp2[i],negative_filter_gaussian[-(i+2)]) 
        ls = cv2.add(ls, filter_of_im1)
        ls = cv2.add(ls, negative_of_im2)
        LS.append(ls)
    #Blending-pyramid ready: 
    #Reconstructino from pyramid 
    recons = LS[0]
    for i in xrange(1, len(LS)):
        recons = cv2.pyrUp(recons)
        recons = cv2.add(recons, LS[i])
        
    return recons, [lp1,lp2], [gp1,gp2]
    
 
def get_LaplaceDetail(laplace_pyr,detail=2, dim=[480,640]):
     """
     Provide Laplacian Pyramid of image to extract details from. 
     dim; shape of the image size you wish. (typically the 
          shape of the image you'll be using it in.)
     Using skimage for resizing. 
     detail = which detail space. 
     # assuming skimage - resize. 
     """
     return skresize(laplace_pyr[detail], dim), laplace_pyr[detail].shape

import skimage.measure as skm 
def er_dil_filter(image, erode_dilate="erode", dim=(5,5)):
    """
    local minima of pixels. 
    """
    if erode_dilate == "erode":
        return skm.block_reduce(image, dim, np.min)
    elif erode_dilate == "dilate": 
        return skm.block_reduce(image, dim, np.max)

    