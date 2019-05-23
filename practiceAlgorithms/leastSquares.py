#!/home/the42nd/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sns.set()

m=int(sys.argv[1])

dataFile=sys.argv[2]

print("We will be fitting a degree {} polynomial.".format(m))

data=np.loadtxt(dataFile,delimiter=',')

x=data[:,0]

y=data[:,1]

n=x.shape[0]

print("Read in {} data points.".format(n))

A=np.zeros(shape=(n,m+1))

### Creating Vandermonde Matrix ###
for i in range(m+1):
	A[:,i]=x**i

### Normal Equations solve for east squares coefficients ###
beta=np.linalg.inv(A.T.dot(A)).dot(A.T).dot(y)

y_hat=A.dot(beta)

print(y_hat)

### Mean Squared Error ###
mse=np.sum((y_hat-y)**2)/n

print("The mean-squared error is {}.".format(mse))

plt.scatter(x,y_hat,label='Least Square Fit',color='red',marker='x')

plt.scatter(x,y,label='Truth',color='blue',marker='o',alpha=0.2)

plt.legend()

plt.show()
