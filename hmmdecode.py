# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:58:26 2017

@author: Sagar Makwana
"""
from  sys import argv
import pickle
import codecs
import math
import json

#--------------------Function Definitions-------------------------------------

def makeProbColumns(tags,columnList):
    for i in range(0,len(columnList)):
        for tag in tags:
            columnList[i][tag] = 0.0
                      
    return columnList
                  

def makeBackPointerColumns(tags,columnList):
    for i in range(0,len(columnList)):
        for tag in tags:
         columnList[i][tag] = '' 
                   
    return columnList

def safe_ln(x):
    if x <= 0:
        return float('-inf')
    elif x > 1:
        return 0.0
    else:
        return math.log(x)
    

#-----------------------------------------------------------------------------
fileName = argv[-1]
outputFile = codecs.open('hmmoutput.txt','w', "utf-8")

#Importing the model 
superDict = {}
with open('hmmmodel.txt', 'r') as fp:
    superDict = pickle.load(fp)


transitionProb = superDict['transitionProb']
emmisionProb = superDict['emmisionProb']


tagCount = len(transitionProb) - 1
tags = transitionProb.keys()
tags.remove('start')



lineCount = 0
for line in codecs.open(fileName,'r','utf-8'):
    
    probTable = []
    backPointer = []
    
    words = line.split(" ")
    for word in words:
        word = word.strip()
        if word != '':
            probTable.append({})
            backPointer.append({})
            
    probTable = makeProbColumns(tags,probTable)
    backPointer = makeBackPointerColumns(tags,backPointer)
    
    count = 0
    prevTags = [] # This contains all the valid tags from the previous cycle
    for word in words:
        word = word.strip()
        if word != '':
            if count == 0: #If it is the initial state
                for tag in tags:
                    #temp = emmisionProb[tag]
                    #bo =  word in temp
                    probTable[count][tag] = safe_ln(transitionProb['start'][tag]) + safe_ln(emmisionProb[tag].get(word,2.0))
                    
                    if probTable[count][tag] != float('-inf'):
                        prevTags.append(tag)
                    
                    backPointer[count][tag] = 'start'
                    
            else: # if it is not the initial state
                currTags = []
                for tag1 in tags:
                    maxProb  = float("-inf")
                    maxTag = ''
                    #Find the most probable transition
                    for tag2 in prevTags:
                        prob = probTable[count-1][tag2] + safe_ln(transitionProb[tag2][tag1]) + safe_ln(emmisionProb[tag1].get(word,1.0))
                        if prob > maxProb:
                            maxProb = prob
                            maxTag = tag2
                    
                    probTable[count][tag1] = maxProb
                    
                    if probTable[count][tag1] != float('-inf'):
                        currTags.append(tag1)
                        
                    backPointer[count][tag1] = maxTag
                               
                prevTags  = currTags
                               
            count += 1
    
    maxProb = float("-inf")
    maxTag = ''          
    for tag in probTable[count-1].keys():
        if probTable[count - 1][tag] > maxProb:
            maxProb = probTable[count - 1][tag]
            maxTag = tag
    

    prev = maxTag        
    resultLine = ''
    wordCount = count -1
    for word in words[::-1]:
        word = word.strip()
        if word != '':
            resultLine = word + '/' + prev + ' ' + resultLine
            prev = backPointer[wordCount][prev]
            wordCount -= 1
        else:
            resultLine = ' ' + resultLine
    
    outputFile.write(resultLine[:-1] + '\n')
    print str(lineCount)
    lineCount += 1
    
outputFile.close()
print 'Done'        


    