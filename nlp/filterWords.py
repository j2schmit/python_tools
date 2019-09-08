#!/usr/local/anaconda3/bin/python                        

import sys
import argparse
import operator
from collections import defaultdict
import subprocess                  

parser = argparse.ArgumentParser(description='A script that acts as a filter on STDIN, counts words after first filtering, filters low count words, and produces document word count file for input into cpTrain. Note, the user must defined the filters for each field in a seperate file named filterDict.py. There must be a dictionary of filters containg a filter for each field from the input line as the value and the key is the order in which the fields will be appended. Additionally, there must be a filter to get the pan/document identifier from the input line that is named panFilter. Also low count words will be filtered again by fieldFilter2, which should be defined to take the word and filter to a broader word, as desired.')                                                                                                        

parser.add_argument('-m','--minCount',type=int,
            help='Minimum count per word, default is 10. Words with smaller counts will be filtered by fieldFilter2.',
            default=10)                                                                                              
parser.add_argument('-n','--noFilter',action='store_true',                                                            
            help='Do not filter any fields')                                                                          

args=parser.parse_args()

noFilter=args.noFilter
minCount=args.minCount

import filterDict

def identityFilter(field):
    return field.strip()  

panFilter=filterDict.panFilter

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
        pan=panFilter(line)      
        word=''                  
        for field in fields:    
            word+=fieldFilter[field](line)
        wordCounts[word]+=1              
        out.write(pan+'|'+word+'\n')      

subprocess.call('sort temp.txt -o temp.txt'.split())

print(count)
print('First pass complete.')
wordList=[pair[0] for pair in sorted(wordCounts.items(), key=operator.itemgetter(1),reverse=True)]
print('There are {} unique words.'.format(len(wordList)))                                        

with open('wordCounts.txt','w') as out:
    for word,count in sorted(wordCounts.items(), key=operator.itemgetter(1),reverse=True):
        out.write('{}, {}\n'.format(word,count))

aboveMinCount=True
topList=[]        
index=0          
#while aboveMinCount:
#    if wordCounts[wordList[index]]>=minCount:
#        topList.append(wordList[index])      
#        index+=1                            
#    else:                                    
#        aboveMinCount=False                  

#wordList=topList

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
with open('temp.txt') as f, open('pans.txt','w') as outPan, open('cpTrainInput.dat','w') as out:
    for line in f:                                                                              
        count+=1
        if (count%100000==0):
            print(count, end='\r')
        splitLine=line.split('|')
        pan=splitLine[0]
        if pan!=oldPAN:
            outPan.write('{}\n'.format(pan))
        word=splitLine[1].replace('\n','')
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

