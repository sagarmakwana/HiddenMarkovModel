# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 00:01:33 2017

@author: Sagar Makwana
"""
from  sys import argv
import codecs
import pickle
import json

trainFileName = argv[-1]

#Transition Probabilities
print 'Initialization..'
transitionProb = {}
emmisionProb = {}
bagOfwords = set()

print 'Generating counts'
count  = 0
for line in codecs.open(trainFileName,'r','utf-8'):
    wordTagPairs = line.split(" ")
    
    prevTag = 'start'
    for wordTagPair in wordTagPairs:
        if wordTagPair == '':
            continue
        
        word = wordTagPair.strip()[:-3]
        tag = wordTagPair.strip()[-2:] 
        
        #add words to the bag of words
        if word not in bagOfwords:
            bagOfwords.add(word)
            
            
        #Generating the transition counts
        if prevTag not in transitionProb:
            transitionProb[prevTag] = {}
            
        if tag in transitionProb[prevTag]:
            transitionProb[prevTag][tag] += 1
        else:
            transitionProb[prevTag][tag] = 1
                          
        prevTag = tag
        
        #Generating the emmision count
        if tag not in emmisionProb:
            emmisionProb[tag] = {}
            
        if word in emmisionProb[tag]:
            emmisionProb[tag][word] += 1
        else:
            emmisionProb[tag][word] = 1
                        
        
    #count  += 1    
    #print 'line ' + str(count)
print 'Generating probabilities'
#Generating transition probabilities        
tagCount = len(transitionProb) - 1
tags = transitionProb.keys()
tags.remove('start')

print 'Generating transition prob'              
for tag1 in transitionProb.keys():
    sumCount = 0 
    for tag2 in transitionProb[tag1].keys():
        sumCount += transitionProb[tag1][tag2]
    for tag2 in tags:
        if tag2 in transitionProb[tag1]:
            transitionProb[tag1][tag2] = (transitionProb[tag1][tag2] + 1)*1.0/(sumCount + tagCount)
        else:
            transitionProb[tag1][tag2] = 1.0/(sumCount + tagCount)

print 'Generating emmision prob'
#Genearting emmision probabilities
for tag in emmisionProb.keys():
    #print tag
    sumCount = 0
    for word in emmisionProb[tag].keys():
        sumCount += emmisionProb[tag][word]
    wordSetInTag = set(emmisionProb[tag].keys())
    for word in bagOfwords:
        if word in wordSetInTag:
            emmisionProb[tag][word] = emmisionProb[tag][word]*1.0/sumCount 
        else:
            emmisionProb[tag][word] = 0.0

 
superDict = {'transitionProb':transitionProb,'emmisionProb':emmisionProb}

print 'Writing to model'
#Writing the model to nbmodel.txt
with open('hmmmodel.txt', 'w') as fp:
    pickle.dump(superDict, fp)  
                                     
print 'Done'


