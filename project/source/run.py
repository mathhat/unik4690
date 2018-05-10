import argparse
import logging
import time
import ast
import sys
sys.path.append("/home/joe/Documents/tf-pose-estimation/src/") 
sys.path.append("/home/user12/PROJECT2018/tf-openpose/src/")
from gradient_estimator import human_canny 

import common
import cv2
import numpy as np
from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh
from draw import draw_humans

from lifting.prob_model import Prob3dPose
from lifting.draw import plot_pose

logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--image', type=str, default='Images/1.jpg')  #../images/p2.jpg')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--scales', type=str, default='[None]', help='for multiple scales, eg. [1.0, (1.1, 0.05)]')
    args = parser.parse_args()
    scales = ast.literal_eval(args.scales)
    
    def nothing(x):
        pass

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))

    kernel = np.ones((2,2))
    kernel2 = np.ones((4,4))
    tol1 = 500
    tol2 = 50
    tol = 20
    k1=k2=k3=k4=k5=k6=k7=k8=1
    # estimate human poses from a single image !
    image = common.read_imgfile(args.image, None, None)
    cv2.namedWindow('image')
    # Create a black image, a window
    # create trackbars for color change
    cv2.createTrackbar('canny1','image',0,500,nothing)
    cv2.createTrackbar('canny2','image',0,500,nothing)
    cv2.createTrackbar('Contour Length','image',0,500,nothing)
    cv2.createTrackbar('k1_headsize','image',10,500,nothing)
    cv2.createTrackbar('k2_headpos','image',10,500,nothing)
    cv2.createTrackbar('k3_headpos','image',10,500,nothing)
    cv2.createTrackbar('k4_headsize','image',10,500,nothing)
    cv2.createTrackbar('k5_earring_width','image',10,500,nothing)
    cv2.createTrackbar('k6_earring_width','image',10,500,nothing)
    cv2.createTrackbar('k7_headx','image',10,500,nothing)
    cv2.createTrackbar('k8_earringx','image',10,500,nothing)
    # create switch for ON/OFF functionality
    minusswitch = '0 : OFF \n1 : ON'
    cv2.createTrackbar('minusk3k4', 'image',0,1,nothing)
    humans = e.inference(image, scales=scales)

        #cv2.imshow('image',img)
        
        # get current positions of four trackbars
    print 'variables will not be saved, writing functions are commented out, check bottom of run.py'
    #try:
    while(1):
        image2 = np.copy(image)
        image2,centers = draw_humans(image2, humans,k1,k2,k3,k4,k5,k6,k7,k8)
        minusswitch = cv2.getTrackbarPos('minusk3k4', 'image')
        k1 = cv2.getTrackbarPos('k1_headsize','image')*0.01
        k2 = cv2.getTrackbarPos('k2_headpos','image')*0.01
        k3 = cv2.getTrackbarPos('k3_headpos','image')*0.01
        k4 = cv2.getTrackbarPos('k4_headsize','image')*0.01
        if minusswitch:
            k3*=-1
            k2*=-1
        k5 = cv2.getTrackbarPos('k5_earring_width','image')*0.01
        k6 = cv2.getTrackbarPos('k6_earring_width','image')*0.01
        k7 = cv2.getTrackbarPos('k7_headx','image')*0.01
        k8 = cv2.getTrackbarPos('k8_earringx','image')*0.01
        #image2 = cv2.GaussianBlur(image2,(31,31),100)
        image2= cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)/2#/255.


        tol1 = cv2.getTrackbarPos('canny1','image')
        tol2 = cv2.getTrackbarPos('canny2','image')
        tol = cv2.getTrackbarPos('Contour Length','image')

        edges = cv2.Canny(image,tol1,tol2)
        #contours = human_canny(edges,image2,tol)#returns contours
        #image3 = cv2.drawContours(image*0, contours, -1, (0,255,255), 1)

        cv2.imshow('image1',edges+image2)
        cv2.imshow('image',np.zeros((100,1000)))
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    #except:
    #    print "maybe there are no people in the image?"
    cv2.destroyAllWindows()
    '''
    if k2 > 0.01*10:
        with open('k126data.txt','a') as File:
            File.write("%f %f %f \n"%(k1,k2,k6))
    if abs(k3) > 0.01*10:
        with open('k34578data.txt','a') as File:
            File.write("%f %f %f %f %f\n"%(k3,k4,k5,k7,k8))
    '''