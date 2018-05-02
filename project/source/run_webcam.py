import argparse
import logging
import time
import sys
sys.path.append("/home/joe/Documents/tf-pose-estimation/src/") 
sys.path.append("/home/user12/PROJECT2018/tf-openpose/src/")
from gradient_estimator import human_canny 
#from draw import draw_humans

import cv2
import numpy as np

from estimator import TfPoseEstimator
from draw import draw_humans
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
    parser.add_argument('--resolution', type=str, default='480x640', help='network input resolution. default=432x368')#def 432 368
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cam = cv2.VideoCapture(args.camera)
    ret_val, image0 = cam.read()
    #humans = e.inference(image)
    while True:
        ret_val, image = cam.read()
        #imgrad = (cv2.cvtColor(image0, cv2.COLOR_BGR2GRAY)+1.) - (cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        
        humans = e.inference(image)

        image2,centers = draw_humans(image, humans,imgcopy=False)

        image2= cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(image,150,120)
        
        #kernel = np.ones((5,15),np.int8)
        #im_gray = cv2.filter2D(im_gray,-1,kernel)


        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)
        
        
        if len(centers)>1:  #where the contouring happens (see gradient_estimator.py)
            contours = human_canny(edges,image2)
            cv2.drawContours(image, contours, -1, (0,255,0), 3)
            cv2.imshow('tf-pose-estimation result', image)
        
        #cv2.imshow('tf-pose-estimation result', image2)

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        #image0 = cam.read()[1]
    cv2.destroyAllWindows()
