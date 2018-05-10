import cv2
import numpy as np
def human_canny(edges,im_bw,tol):
    
    edges2 = np.multiply(im_bw,edges)
    edges = np.asarray(edges2,dtype=np.uint8)
    edges, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #image = cv2.dilate(image,kernel)          
    #image = cv2.erode(image,kernel2)          
    #image = cv2.filter2D(image,-1,kernel2)
    i = 0
    if len(contours)>1:
        while 1: 
            try:
                if len(contours[i])<tol:
                    del contours[i]
                else:
                    i+=1
            except:
                break
    

    
    #im_bw = cv2.threshold(im_bw, 0, 255, cv2.CV_8UC1)[1]
    #im_bw = np.asarray(im_bw,dtype=np.uint8)
    #im_bw, contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours


"""
def hull_generation_code():
    import sys 
    hull = np.array(contours.size())
    module = sys.modules[__name__]
    for i in range(len(contours)):
        if (cv2.contourArea(contours[i])) > 0: 
            setattr(module, "hull_%s"%i, cv2.convexHull(contours[i]))

"""