#!/home/the42nd/anaconda3/bin/python

import sys
import numpy as np

m=int(sys.argv[1])

n=10

c=np.random.uniform(-20,20,size=m+1)

x=np.random.uniform(-10,10,size=n)

e=np.random.normal(0,1,size=n)

y=e
for i in range(m+1):
	y+=int(c[i])*x**i

with open('data.csv','w') as out:
	for i in range(n):
		out.write("{},{}\n".format(x[i],y[i]))
