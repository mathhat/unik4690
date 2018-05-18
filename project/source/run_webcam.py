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


import cv2
import numpy as np

from estimator import TfPoseEstimator
from draw2 import draw_humans
from networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--zoom', type=float, default=1)
    parser.add_argument('--back', type=str, default='Images/back.jpg')  #../images/p2.jpg')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')#def 432 368
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cam = cv2.VideoCapture(args.camera)
    ret_val, image = cam.read()
    back  = common.read_imgfile(args.back,None,None)
    back= cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)/255.

    #back[:w,:h]
    kernel = np.ones((2,2))
    kernel2 = np.ones((4,4))

    tol1,tol2,tol = read.Tol()
    #humans = e.inference(image)
    while True:
        ret_val, image = cam.read()
        humans = e.inference(image)
        imbw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)/255.
        image2,centers = draw_humans(image.copy(), humans,1)
        #edges = cv2.Canny(image,tol1,tol2)
        #im = cv2.bilateralFilter(im,3,75,75)
        
        #image2 = cv2.GaussianBlur(image2,(21,21),100,)
        
        image2= cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)/255.
        '''        
        if len(centers)>1:  #where the contouring happens (see gradient_estimator.py)
            contours = human_canny(edges,image2,tol)#returns contours
            image = cv2.drawContours(image*0, contours, -1, (0,255,255), 1)/255.#draws contours

            cv2.putText(image,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)

            cv2.imshow('tf-pose-estimation result', image)
        
        '''
        #background = np.zeros_like(image2)
        # image2 burde her være "dukka" eller masken til hele greia. 
        # dersom den ikke er der vil man bare få det ene bildet diretke 
        
        #image3 = Laplacian_blend(imbw,np.zeros_like(back),image2)
        #image3 = cv2.threshold(image3,0.,255,cv2.THRESH_TOZERO)[1]
        #image3 = Laplacian_blend(imbw,image3-back,image2)
        
        cv2.imshow('tf-pose-estimation result',image2)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
