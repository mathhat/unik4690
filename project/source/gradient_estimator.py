import cv2
import numpy as np
 
def human_canny(edges,im_bw,kernel,kernel2,tol):
    edges2 = np.multiply(im_bw,edges)
    #edges3 = np.multiply(im,edges3)


    edges = np.asarray(edges2,dtype=np.uint8)
    edges, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #image = cv2.dilate(image,kernel)          
    #image = cv2.erode(image,kernel2)          
    #image = cv2.filter2D(image,-1,kernel2)
   
    
    
    #print contours[0]
    if len(contours)>1:
        for i in xrange(len(contours)):
            if len(contours[i])<tol:
                contours[i]*=0
    #im_bw = cv2.threshold(im_bw, 0, 255, cv2.CV_8UC1)[1]
    #im_bw = np.asarray(im_bw,dtype=np.uint8)
    #im_bw, contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours
