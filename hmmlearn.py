# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 00:01:33 2017

@author: Sagar Makwana
"""
from  sys import argv
import codecs
import json

trainFileName = argv[-1]

#Transition Probabilities
#print 'Initialization..'
transitionProb = {}
emmisionProb = {}
totalTransitionTagcount = {}
totalEmmisionTagCount = {}

#print 'Generating counts'
count  = 0
for line in codecs.open(trainFileName,'r','utf-8'):
    wordTagPairs = line.split(" ")
    
    prevTag = 'start'
    for wordTagPair in wordTagPairs:
        if wordTagPair == '':
            continue
        
        word = wordTagPair.strip()[:-3]
        tag = wordTagPair.strip()[-2:] 
        

        #Generating the transition counts
        if prevTag not in transitionProb:
            transitionProb[prevTag] = {}
            
        if tag not in transitionProb:
            transitionProb[tag] = {}
            
        if tag in transitionProb[prevTag]:
            transitionProb[prevTag][tag] += 1
        else:
            transitionProb[prevTag][tag] = 1
                          
        if prevTag in totalTransitionTagcount:
            totalTransitionTagcount[prevTag] += 1
        else:
            totalTransitionTagcount[prevTag] = 1
                          
        prevTag = tag
        
        #Generating the emmision count
        if word not in emmisionProb:
            emmisionProb[word] = {}
        
        if tag in totalEmmisionTagCount:
            totalEmmisionTagCount[tag] += 1
        else:
            totalEmmisionTagCount[tag] = 1
        
        if tag in emmisionProb[word]:
            emmisionProb[word][tag] += 1
        else:
            emmisionProb[word][tag] = 1
              
                                
    #count  += 1    
    #print 'line ' + str(count)
#print 'Generating probabilities'
#Generating transition probabilities        
tagCount = len(transitionProb) - 1
tags = transitionProb.keys()
tags.remove('start')

#print 'Generating transition prob'              
for tag1 in transitionProb.keys():
    for tag2 in tags:
        if tag2 in transitionProb[tag1]:
            transitionProb[tag1][tag2] = (transitionProb[tag1][tag2] + 1)*1.0/(totalTransitionTagcount[tag1] + tagCount)
        else:
            transitionProb[tag1][tag2] = 1.0/(totalTransitionTagcount[tag1] + tagCount)

#print 'Generating emmision prob'
#Genearting emmision probabilities
for word in emmisionProb.keys():
    for tag in emmisionProb[word]:
        emmisionProb[word][tag] = emmisionProb[word][tag]*1.0/totalEmmisionTagCount[tag]
     
superDict = {'transitionProb':transitionProb,'emmisionProb':emmisionProb}

#print 'Writing to model'
#Writing the model to nbmodel.txt
with open('hmmmodel.txt', 'w') as fp:
    json.dump(superDict, fp)  
                                     
#print 'Done'


