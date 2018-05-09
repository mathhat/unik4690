import argparse
import logging
import time
import ast

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
    parser.add_argument('--image', type=str, default='../../../Downloads/midorya.jpg')  #../images/p2.jpg')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--scales', type=str, default='[None]', help='for multiple scales, eg. [1.0, (1.1, 0.05)]')
    args = parser.parse_args()
    scales = ast.literal_eval(args.scales)

    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))

    # estimate human poses from a single image !
    image = common.read_imgfile(args.image, None, None)
    # image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    t = time.time()
    humans = e.inference(image, scales=scales)

    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    # cv2.imshow('tf-pose-estimation result', image)
    # cv2.waitKey()
