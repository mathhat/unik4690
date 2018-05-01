import argparse
import logging
import time
import sys
sys.path.append("/home/joe/Documents/tf-pose-estimation/src_mine/")
from gradient_estimator import human_canny 
import cv2
import numpy as np

from estimator import TfPoseEstimator
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
    #ret_val, image = cam.read()
    #humans = e.inference(image)

    while True:
        ret_val, image = cam.read()
        humans = e.inference(image)
        image2,centers = TfPoseEstimator.draw_humans(image, humans,imgcopy=False)

        #imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(image,120,400)/120.
        #edges = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)[1]  

        im_gray = cv2.convertScaleAbs(np.sum(image2, axis=2))
        #kernel = np.ones((10,10),np.int8)
        #im_gray = cv2.filter2D(im_gray,-1,kernel)/120.
        
        #im_bw = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY)[1]  
        
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)
        
        
        if len(centers)>1:
            contours = human_canny(edges,im_gray)
            cv2.drawContours(image, contours, -1, (0,255,0), 3)
            cv2.imshow('tf-pose-estimation result', image)
        
        #cv2.imshow('tf-pose-estimation result', image2)

        
        

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
