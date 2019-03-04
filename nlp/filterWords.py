#!/home/the42nd/anaconda3/bin/python

import sys
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('-n','--noFilter',action='store_true',
		    help='Do not filter any fields')
parser.add_argument('-d','--delimiter',
		    help='Set delimiter',default='|')
args=parser.parse_args()

delimiter=args.delimiter
noFilter=args.noFilter

def mccMap(mcc):
	mcc=int(mcc.strip())
	if mcc<3000:
		mcc=mcc
	elif mcc<4000:
		mcc=3000
	else:
		mcc=mcc
	mcc='{:4d}'.format(mcc)
	return mcc

def mccFilter(mcc):
	return mccMap(mcc)

def amtFilter(amt):
	amt=float(amt.strip())
	if amt<4:
		bin='L'
	elif amt<20:
		bin='M'
	elif amt<100:
		bin='H'
	elif amt<500:
		bin='E'
	elif amt>=500:
		bin='X'
	return bin

def posEntryFilter(pos):
	return pos.strip()

def identityFilter(field):
	return field.strip()

fieldFilter={1: posEntryFilter,
	     2: mccFilter,
	     3: amtFilter}

fields=sorted(fieldFilter.keys())

if args.noFilter==True:
	for field in fields:
		fieldFilter[field]=identityFilter

for line in sys.stdin:
	splitLine=line.split(delimiter)
	pan=splitLine[0].strip()
	word=''
	for field in fields:
		word+=fieldFilter[field](splitLine[field])
	sys.stdout.write(pan+'|'+word+'\n')
