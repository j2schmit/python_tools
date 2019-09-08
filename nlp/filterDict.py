#!/usr/local/anaconda3/bin/python

def panFilter(line):
	return(line.strip().split('|')[0].strip())

def mccFilter(line):
	mcc=line.split('|')[2]
	return(mcc[:2])

def posFilter(line):
	pos=line.split('|')[1]
	return(pos)

def amtFilter(line):
	amt=float(line.split('|')[3])
	if amt<10:
		bin='L'
	elif amt<50:
		bin='M'
	elif amt<200:
		bin='H'
	else:
		bin='X'
	return(bin)

fieldFilter={1:posFilter,
	    2:mccFilter,
	    3:amtFilter}

def fieldFilter2(word):
	return(word)
