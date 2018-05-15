# -*- coding: utf-8 -*-
"""
Created on Thu May 10 21:21:14 2018

Laplace Pyramid Blending of images. 
"""
import cv2
import numpy as np

def constructGaussian(img, depth=6): 
    G = img.copy()
    GP = [G]
    for i in xrange(depth): 
        G = cv2.pyrDown(G)
        GP.append(G)
    return GP 
    
def constructLaplacian(gaussian_pyramid): 
    #Note, should be same as gaussian 
    lp = [gaussian_pyramid[-1]]
    for i in xrange((len(gaussian_pyramid) - 1), 0, -1): 
        GE = cv2.pyrUp(gaussian_pyramid[i])        
        try:
            L = gaussian_pyramid[i-1]- GE
        except:
            L = gaussian_pyramid[i-1]- GE[1:]
            print "fak"
        lp.append(L)
    return lp


def Laplacian_blend(image1, image2, blending_filter):
    # Gaussian pyr of images
    gp1 = constructGaussian(image1)
    gp2 = constructGaussian(image2)
    
    # Laplacians 

    lp1 = constructLaplacian(gp1)
    lp2 = constructLaplacian(gp2)
    
    #Apply filters ? 
    negative_filter = np.ones(blending_filter.shape)
    negative_filter_gaussian = constructGaussian(negative_filter)
    filter_gaussian = constructGaussian(blending_filter)
    LS = []
    for i in range(len(lp1)):
        ls = np.zeros(lp1[i].shape)
        filter_of_im1 = cv2.filter2D(lp1[i], -1,filter_gaussian[i])
        negative_of_im2 = cv2.filter2D(lp2[i],-1,negative_filter_gaussian[i]) 
        ls += filter_of_im1
        ls += negative_of_im2
        LS.append(ls)
    #Blending-pyramid ready: 
    #Reconstructino from pyramid 
    recons = LS[0]
    for i in xrange(1, len(LS)):
        recons = cv2.pyrUp(recons)
        
        try:
            recons +=  LS[i]
        except:
            recons =  recons[1:] + LS[i]
            print "fak"
    return recons
    
 
        