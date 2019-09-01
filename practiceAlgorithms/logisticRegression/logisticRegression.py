#!/home/the42nd/anaconda3/bin/python

import numpy as np
import sys

dataFile=sys.argv[1]

data=np.loadtxt(dataFile,delimiter=',')

y=data[:,-1]

X=data[:-1,:]

del data


def logit(x,beta):
	exp=np.exp(-1*np.dot(x,beta))
	return(1/(1+exp))

def binaryCrossEntropy(X,y,beta):
	predictions=np.array([y.shape[0],1])
