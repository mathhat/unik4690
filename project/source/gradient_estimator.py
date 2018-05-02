import cv2
import numpy as np
 
def human_canny(edges,im_bw):
    '''
    edges = np.multiply(edges,im_bw)
    edges = cv2.threshold(edges, 0, 255, cv2.CV_8UC1)[1]
    edges = np.asarray(edges,dtype=np.uint8)
    edges, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in xrange(len(contours)):
        if len(contours[i])<10:
            contours[i]*=0
    '''
    im_bw = cv2.threshold(im_bw, 0, 255, cv2.CV_8UC1)[1]
    im_bw = np.asarray(im_bw,dtype=np.uint8)
    im_bw, contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours