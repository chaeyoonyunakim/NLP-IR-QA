# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 06:27:01 2020
#Name: Chaeyoon Kim
#City Email: Chaeyoon.Kim@city.ac.uk
"""

data = open('WhatsAppChat.txt', 'r', encoding='utf-8', errors='ignore')
stop = open('stopwords.txt','r')
def countWord(data,stop):
    word = {}
    for line in stop:
        words = line.split()
        for i in words:
            if i in word:
                word[i] = word[i] + 1
            else:
                word[i] = 1
    wordDict = {}
    for line in data:
        lines = line.split()
        for i in lines:
            i = i.lower().replace("'", "")
            if i in wordDict and i not in word:
                wordDict[i] = wordDict[i] + 1
            else:
                wordDict[i] = 1
    return (wordDict)
wordDict = countWord(data, stop)

def printTop100(wordDict):
    words = list(wordDict.keys())
    words.sort(reverse=True, key=lambda v:wordDict[v])
    for i in range(100):
        word = words[i]
        print(i+1, ':', word, '=', wordDict[word])

#---------------------------------------------
top100 = printTop100(wordDict)
print(top100)