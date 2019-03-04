#!/home/the42nd/anaconda3/bin/python

import argparse
import numpy as np
import random
import string

parser=argparse.ArgumentParser()
parser.add_argument('-n','--number',type=int,
		    help='Number of lines of fake text to create')
parser.add_argument('-f','--file',default='fakeText.txt',
		    help='Name of new text file')
args=parser.parse_args()

numLines=args.number
outFile=args.file

amts=np.random.lognormal(3,1,numLines)
posEntryModes=random.choices(['M','C','X','E','V','U','S'],k=numLines)
mccs=np.random.randint(0,9999,numLines)

with open(outFile,'w') as out:
	for i in range(numLines):
		pan=''.join(random.choices(string.ascii_letters +string.digits,k=19))
		line='{}|{}|{:4d}|{:10.2f}|'.format(pan,posEntryModes[i],mccs[i],amts[i])
		out.write(line+'\n')
