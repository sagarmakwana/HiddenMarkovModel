# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:58:26 2017

@author: Sagar Makwana
"""
from  sys import argv
import codecs
import math
import json

#--------------------Function Definitions-------------------------------------

def safe_ln(x):
    if x > 1:
        return 0.0
    else:
        return math.log(x)
    
def getCorrectEmmisionProb(emmisionProb,word, tag):
    if word not in emmisionProb:
        return 2.0
    else:
        return emmisionProb[word][tag]
#-----------------------------------------------------------------------------
fileName = argv[-1]
outputFile = codecs.open('hmmoutput.txt','w', "utf-8")

#Importing the model 
superDict = {}
with open('hmmmodel.txt', 'r') as fp:
    superDict = json.load(fp)


transitionProb = superDict['transitionProb']
emmisionProb = superDict['emmisionProb']


tagCount = len(transitionProb) - 1
tags = transitionProb.keys()
tags.remove('start')



lineCount = 0
for line in codecs.open(fileName,'r','utf-8'):
    #Initializing the probability and back pointer tables    
    probTable = []
    backPointer = []
    
    #Tokenizing the line
    words = line.split(" ")
 
    count = 0
    prevTags = [] # This contains all the valid tags from the previous cycle
    for word in words:
        word = word.strip()
        if word != '':
            probTable.append({})
            backPointer.append({})
            #Check if the word exists in emmisionprob table and asign the relevant tags to be considered for it
            tagsInConsideration = emmisionProb.get(word, None )
            if tagsInConsideration == None:
                tagsInConsideration  = tags
            else:
                tagsInConsideration = tagsInConsideration.keys()
            
            if count == 0: #If it is the initial state
                for tag in tagsInConsideration:
                    probTable[count][tag] = safe_ln(transitionProb['start'][tag]) + safe_ln(getCorrectEmmisionProb(emmisionProb,word,tag))
                    backPointer[count][tag] = 'start'
                    
            else: # if it is not the initial state
                for tag1 in tagsInConsideration:
                    maxProb  = float("-inf")
                    maxTag = ''
                    #Find the most probable transition
                    for tag2 in prevTags:
                        prob = probTable[count-1][tag2] + safe_ln(transitionProb[tag2][tag1]) + safe_ln(getCorrectEmmisionProb(emmisionProb,word,tag1))
                        if prob > maxProb:
                            maxProb = prob
                            maxTag = tag2
                    
                    probTable[count][tag1] = maxProb
                    backPointer[count][tag1] = maxTag
                               
            
            prevTags = tagsInConsideration                   
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
    #print str(lineCount)
    lineCount += 1
    
outputFile.close()
#print 'Done'        


    