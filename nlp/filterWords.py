#!/apps/usr/local64/anaconda-appfraud/bin/python                                                                           

import sys
import argparse
import operator
from collections import defaultdict
import subprocess                  

parser = argparse.ArgumentParser(description='_FA_VERSION_MESSAGE'+"\n\n"+'A script that acts as a filter on STDIN and sends filtered words to STDOUT.')                                                                                                

parser.add_argument('-m','--minCount',type=int,
            help='Minimum count per word, default is 10. Words with smaller counts will be filtered by fieldFilter2.',
            default=10)                                                                                               
parser.add_argument('-n','--noFilter',action='store_true',                                                            
            help='Do not filter any fields')                                                                          
parser.add_argument('-d','--delimiter',                                                                               
            help='Set delimiter, DEFAULT is pipe-delimited',default='|')                                              
parser.add_argument('-p','--panField',required=True,type=int,                                                         
            help='Field/column containing the PAN. (Indexing starts at zero.)')                                       

args=parser.parse_args()

delimiter=args.delimiter
noFilter=args.noFilter  
minCount=args.minCount  
panField=args.panField  

import filterDict

def identityFilter(field):
    return field.strip()  

fieldFilter=filterDict.fieldFilter

fields=sorted(fieldFilter.keys())

if args.noFilter==True:
    for field in fields:
        fieldFilter[field]=identityFilter

wordCounts=defaultdict(int)

print("Starting first pass, for intitial word filtering and counts...")

count=0
with open('temp.txt','w') as out:
    for line in sys.stdin:       
        count+=1                 
        if (count%100000==0):    
            print(count, end='\r')
        splitLine=line.split(delimiter)
        pan=splitLine[panField].strip()
        word=''                        
        for field in fields:           
            word+=fieldFilter[field](splitLine)
        wordCounts[word]+=1                    
        out.write(pan+'|'+word+'\n')           

subprocess.Popen('sort temp.txt -o temp.txt'.split())

print(count)
print('First pass complete.')
wordList=[pair[0] for pair in sorted(wordCounts.items(), key=operator.itemgetter(1),reverse=True)]
print('There are {} unique words.'.format(len(wordList)))                                         

aboveMinCount=True
topList=[]        
index=0           
while aboveMinCount:
    if wordCounts[wordList[index]]>=minCount:
        topList.append(wordList[index])      
        index+=1                             
    else:                                    
        aboveMinCount=False                  

wordList=topList

wordsAboveCount=len(wordList)

wordIndexDict={wordList[i]:i for i in range(wordsAboveCount)}

print('Only {} words have {} or more counts.'.format(wordsAboveCount,minCount))

fieldFilter2=filterDict.fieldFilter2

if args.noFilter==True:
    fieldFilter2=identityFilter

print('Starting second pass, and creating PAN/document word count dictionary.')

def writeDict(countsDict):
    countsList=[str(pair[0])+':'+str(pair[1]) for pair in sorted(countsDict.items(), key=operator.itemgetter(0))]
    dictString=' '.join(countsList)+'\n'                                                                         
    return dictString                                                                                            

panDict=defaultdict(int)
oldPAN=''               
count=0                 
with open('temp.txt','r') as f, open('pans.txt','w') as outPan, open('cpTrainInput.dat','w') as out:
    for line in f:                                                                                  
        count+=1                                                                                    
        if (count%100000==0):                                                                       
            print(count, end='\r')                                                                  
        splitLine=line.split('|')                                                                   
        pan=splitLine[0]
        if pan!=oldPAN:
            outPan.write('{}\n'.format(pan))
        try:
            word=splitLine[1].replace('\n','')
        except IndexError:
            print('Bad line at line {}'.format(count))
            print('{}, {}'.format(pan,line))
        if wordCounts[word]<minCount:
            word=fieldFilter2(word)
        if pan!=oldPAN and oldPAN!='':
            outLine=writeDict(panDict)
            out.write(outLine)
            panDict=defaultdict(int)
        if wordIndexDict.get(word)==None:
            wordIndexDict[word]=wordsAboveCount
            wordsAboveCount+=1
        panDict[wordIndexDict[word]]+=1
        oldPAN=pan
    outLine=writeDict(panDict)
    out.write(outLine)

print(count)
print('Completed second pass filtering of words. There are {} unique words after filtering.'.format(wordsAboveCount))
print('cpTrain input file created.')

with open('wordList.csv','w') as out:
    for word,index in wordIndexDict.items():
        out.write('{},{}\n'.format(word,index))

print('Word list created.')

subprocess.Popen('rm temp.txt'.split())

print('Finished.')
