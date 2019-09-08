#!/usr/local/anaconda3/bin/python

import sys

countsFile=sys.argv[1]
wordFile=sys.argv[2]

wordMap={}
with open(wordFile) as f:
	for line in f:
		word=line.split(',')[0]
		index=line.strip().split(',')[1]
		wordMap[word]=index

word1="V83M"
word2="V10M"

d1=0
d2=0
d12=0

with open(countsFile) as f:
	for line in f:
		both=0
		counts=line.split(' ')
		for pair in counts:
			word=pair.split(':')[0]
			if word==wordMap[word1]:
				both+=1
				d1+=1
			elif word==wordMap[word2]:
				both+=1
				d2+=1
			if both==2:
				d12+=1
				break

print(f'Coherence = {d12/(d1+d2)}')
print(f'd12 = {d12}')
print(f'd1 = {d1}')
print(f'd2 = {d2}')					
			
