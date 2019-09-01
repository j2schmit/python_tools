#!/home/the42nd/anaconda3/bin/python
import pandas as pd

dataFile='/home/the42nd/data/iris/iris.data'

df=pd.read_csv(dataFile)

print(df.head())

def setosaFilter(irisClass):
	if irisClass=='Iris-setosa':
		return(1)
	else:
		return(0)

df['class']=df['class'].map(setosaFilter)

df.to_csv('iris.csv',index=False,header=False)
