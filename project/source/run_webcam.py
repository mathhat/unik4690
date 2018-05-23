# -*- coding:utf-8 -*-
import argparse
import logging
import time
import sys
import common
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
    parser.add_argument('--back', type=str, default='Images/back.jpg')  #../images/p2.jpg')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')#def 432 368
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    args = parser.parse_args()

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cam = cv2.VideoCapture(args.camera)
    ret_val, image = cam.read()
    back  = common.read_imgfile(args.back,None,None)
    
    tol1,tol2,tol = read.Tol()
    humans = e.inference(image)
    image2,centers = draw_humans(image.copy(), humans,1)

    while True:
        ret_val, image = cam.read()
        humans = e.inference(image)
        image2_tmp,centers = draw_humans(image.copy(), humans,1)
        if np.any(image2_tmp > 0):
            image2=image2_tmp
        image3 = Laplacian_blend(image/255., back/255.,image2/255.)
        
        cv2.putText(image3,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)
        image3 = images.cpp_normalize(image3)
        cv2.imshow('tf-pose-estimation result',image3)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
       
    cv2.destroyAllWindows()
    cam.release()