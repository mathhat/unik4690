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
from draw3 import draw_humans          #gives gradient image
from draw2 import draw_humans_original #gives slim dummy
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
    kernel = np.ones((7,7))

    #bruk disse til å endre på Canny sine toleranser
    #vi bruker nemlig canny til å definere conturene som vi så bruker fillconvexpoly på
    '''
    tol1 - thresh for hvor lett punkter lar seg sammenkobles i canny, (lav verdi = lange streker, sett mellom 50 og 300) 
    tol2 - thresh for hvor lett punkter lar seg tegnes til å begynne med, (lav verdi = mye støy, sett mellom 100 og 300) 
    '''

    while True:
        #back = cam2.read()[-1]

        #run neural network that finds humans, then draw humans
        ret_val, image = cam1.read()
        humans = e.inference(image)
        image2_tmp = draw_humans(image.copy(), humans,1,tol1,tol2) #here's the grad/poly image
        image3 = draw_humans_original(image.copy(), humans,1) #here our dummy
    
        #freeze dummy if no human is spotted
        if np.any(image2_tmp > 0):
            image2=image2_tmp
        #blend background
        #image3 = Laplacian_blend(image/255., back/255.,image2/255.)

        #cv2.putText(image3,
        #            "FPS: %f" % (1.0 / (time.time() - fps_time)),
        #            (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #            (0, 0, 255), 2)
        #print edges
        #image2 = cv2.dilate(image2,kernel) #If you wanna try to fill the gaps, I've played with the idea here
        #image2 = cv2.dilate(image2,kernel)
        #image2 = cv2.dilate(image2,kernel)
        cv2.imshow('tf-pose-estimation result',image2) #polydraw
        cv2.imshow('tf-pose-estimation result2',image3) #dummy
        
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
       
    cv2.destroyAllWindows()
    cam1.release()    
    #cam2.release()