from __future__ import division
import math
import string

doc2 = "The sky is blue."
doc3 = "The sun and sky are bright."

docSplit = doc2.split()
docSplit2 = doc3.split()

ignoredWords = ["is", "the", "and", "a", "to", "was", "are"]


#Remove punctuation from list of strings, and remove words that should be ignored
def setupStringList(stringList):
    newStrings = []
    for word in stringList:
        word = word.translate(None, string.punctuation).lower()
        if word not in ignoredWords:
            newStrings.append(word)
    return newStrings

#Get word frequency in the document
def getWordFreq(stringList):
    wordsCount = {}
    for word in stringList:
        newWord = word.translate(None, string.punctuation).lower()
        if newWord in wordsCount:
            wordsCount[newWord] += 1
        else:
            wordsCount[newWord] = 1
    return wordsCount
    
#Get tf for each word in document
def getTf(stringList, wordsCount):
    tfDict = {}
    for word in stringList:
        tf = wordsCount[word] / len(stringList)
        tfDict[word] = tf
    return tfDict
#From http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
def n_containing(word, documentList):
    return sum(1 for doc in documentList if word in doc)

#Get idf for each word in document
#From http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
def getIdf(documentList, stringList):
    idfList = {}
    for word in stringList:
        idf = math.log(len(documentList) / (n_containing(word, documentList)))
        idfList[word] = idf
    return idfList

def calculateTfidf(word, tfList, idfList):
    tfidf = tfList[word] * idfList[word]
    return tfidf


#Testing
stringList1 = setupStringList(docSplit)
stringList2 = setupStringList(docSplit2)
print stringList1
docList = [stringList1, stringList2]

doc1wordCount = getWordFreq(docList[0])
doc2wordCount = getWordFreq(docList[1])
doc1tf = getTf(docList[0], doc1wordCount)
doc2tf = getTf(docList[1], doc2wordCount)


doc1Idf = getIdf(docList, docList[0])
doc2Idf = getIdf(docList, docList[1])

print "TF: "
print doc1tf
print doc2tf
print "IDF: "
print doc1Idf
print doc2Idf

print "Document 1 tfidf: "
for word in docList[0]:
    tfidf = calculateTfidf(word, doc1tf, doc1Idf)
    print word + ": %f" % tfidf

print "Document 2 tfidf: "
for word in docList[1]:
    tfidf = calculateTfidf(word, doc2tf, doc2Idf)
    print word + ": %f" %tfidf


