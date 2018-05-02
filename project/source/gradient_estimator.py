import cv2
import numpy as np
 
def human_canny(edges,im_bw):
    #
    '''
    edges = np.multiply(edges,im_bw)
    edges = cv2.threshold(edges, 0, 255, cv2.CV_8UC1)[1]
    edges = np.asarray(edges,dtype=np.uint8)
    edges, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    '''
    
    '''
    print contours[0]
    for i in xrange(len(contours)):
        if len(contours[i])<40:
            contours[i]*=0
    
    try:
        cunts = contours[0]
    except:
        pass
    '''



    '''    
    #im = im_bw*0 #weird
    for cnt in contours[1:]:
        #cv2.fillConvexPoly(im,cnt,[255,255,255]) #weird
        cunts= np.append(cunts,cnt[:],axis=0) #hulls

    hull = cv2.convexHull(np.asarray(cunts))
    '''
    
    ''' #just a matplotlib plot based on the contour line
    import sys 
    import matplotlib.pyplot as plt 
    plt.plot([cunts[i][0,0] for i in range(len(cunts))],[-cunts[i][0,1] for i in range(len(cunts))],'r-o')
    plt.show()
    sys.exit()
    '''
    im_bw = cv2.threshold(im_bw, 0, 255, cv2.CV_8UC1)[1]
    im_bw = np.asarray(im_bw,dtype=np.uint8)
    im_bw, contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours