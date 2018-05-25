import matplotlib.pyplot as plt
from numpy import *
from numba import njit
# Generic image functionality

def imread( filename, format=''):
    return plt.imread(filename) #*255

def imwrite(data, filename, format=''):
    dims = data.shape
    if len(dims)==3:
        plt.imsave(filename, data/255., origin='upper')
    else:
        plt.imsave(filename, data/255., origin='upper',cmap='gray')

def imshow(data):
    if ndim(data) == 2:
        plt.imshow(data, cmap = 'gray')
    else :
        plt.imshow(data)
    plt.show()


# Functions for image manipulation
        
def mapto01(X):
    minval, maxval = X.min(), X.max()
    X -= minval
    X /= (maxval-minval)

@njit #c++ boi
def cpp_normalize(image):
    mex = 0
    h,w = image.shape[:2]
    for i in range(w):
        for j in range(h):
            it = image[j,i,0]+image[j,i,2]+image[j,i,2]
            if it > mex:
                mex = it
    return mex
@njit #c++ boi
def cpp_normalize_grey(image):
    mex = 0
    h,w = image.shape[:2]
    for i in range(w):
        for j in range(h):
            it = image[j,i]
            if it > mex:
                mex = it
    return mex


def contrastadjust(X,epsilon):
    """
    Assumes that the values are in [0,255]
    """
    X /= 255.
    X += epsilon
    log(X, X) 
    X -= log(epsilon)
    X /= (log(1+epsilon)-log(epsilon))
    X *= 255
  
def contrastadjust0(X,n):
    """
    Assumes that the values are in [0,255]
    """
    X /= 255.
    X -= 1/2.
    X *= n
    arctan(X, X)
    X /= (2*arctan(n/2.)) 
    X += 1/2.0
    X *= 255 # Maps the values back to [0,255]
