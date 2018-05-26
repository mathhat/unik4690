# -*- coding:utf-8 -*-
import argparse
import logging
import time
import sys
import common
from skimage import data, color
from skimage.transform import rescale, resize, downscale_local_mean
sys.path.append("/home/joe/Documents/tf-pose-estimation/src/") 
sys.path.append("/home/user12/PROJECT2018/tf-openpose/src/")
#from gradient_estimator import human_canny 
from Laplace_Filter_Deprecated import Laplacian_blend, constructGaussian,constructLaplacian
import read
import images

import cv2
import numpy as np

from estimator import TfPoseEstimator
from draw2 import draw_humans
from networks import get_graph_path, model_wh

fps_time = 0
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--back', type=str, default='Images/black.png')  #../images/p2.jpg')
    parser.add_argument('--resolution', type=str, default='640x480', help='network input resolution. default=432x368')#def 432 368
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    args = parser.parse_args()

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cam1 = cv2.VideoCapture(args.camera)
    #cam2 = cv2.VideoCapture(2)
    ret_val, image = cam1.read()
    back  = common.read_imgfile(args.back,None,None)
    back = resize(back,(h,w),1)
    tol1,tol2,tol = read.Tol()
    humans = e.inference(image)
    image2 = draw_humans(image.copy(), humans,1)
    kernel = np.ones((6,6))
    while True:
        #back = cam2.read()[-1]

        #run neural network that finds humans, then draw humans
        ret_val, image = cam1.read()
        humans = e.inference(image)
        image2_tmp = draw_humans(image.copy(), humans,1)
    
        #freeze dummy if no human is spotted
        if np.any(image2_tmp > 0):
            image2=image2_tmp

        #blend background
        image3 = Laplacian_blend(image/255., back/255.,image2/255.)

        cv2.putText(image3,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)
        imagee = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)/255.
        imagee = cv2.GaussianBlur(imagee,(41,41),40)
        #imagee = cv2.GaussianBlur(imagee,(21,21),20)
        edges = cv2.Canny(image,tol1,tol2)
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1:]
        edges = cv2.fillConvexPoly(edges,np.asarray(contours),[0,0,255],8)
        
        
        #edges = cv2.dilate(edges,kernel)
        #edges = cv2.dilate(edges,kernel)
        #mask = np.zeros((h+2, w+2), np.uint8)
        #Floodfill from point (0, 0)
        #cv2.floodFill(edges, mask, (h/2,w/2), 255)
 
        
        #k = cv2.matchShapes(imagee,edges,1,0.0)
        edges = np.multiply(imagee,edges)
        #print edges
        cv2.imshow('tf-pose-estimation result',edges)
        
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
       
    cv2.destroyAllWindows()
    cam1.release()    
    #cam2.release()