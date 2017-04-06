# This is the "coordinator" module that calls on other modules to process a client request

import csv
from words.models import Document_Data
import words.dataretrieval
import words.dataanalyzer
from words.emailsending import *
filePath = '/mnt/vol/csvs/'

from threading import Thread

import os
import zipfile
import sys
import shutil

# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory/
def zipMatrices(matricesPath, hashStr):
    return (shutil.make_archive(matricesPath+hashStr, 'zip', matricesPath, hashStr))
    #zf = zipfile.ZipFile(hashStr+".zip", "w")
    #for dirname, subdirs, files in os.walk(matricesPath):
        #print(dirname)
        #sys.stdout.flush()
        #zf.write(dirname)
        #for filename in files:
            #print(filename)
            #sys.stdout.flush()
            #zf.write(os.path.join(dirname, filename))
    #zf.close()

class RequestsExecuteThread(Thread):
    def __init__(self, requests, email):
        Thread.__init__(self)
        self.requests = requests
        self.email = email
    def run(self):
        urlList = []
        csvList = []
        matrixList = []
        errorDict = {} # Map a hashStr (representing an analysis) to a list of strings (representing errors for an analysis)
        allhashstr = ''
        for req in self.requests:
            print('thread start')
            try:
                res = req.execute()
                errorDict[req.hashStr] = res.errors # List of strings in the format: "Error at x = someDate: chunk did not contain someWord". List is empty or None if there are no errors
                res.generateCSV(req.hashStr)
                url = "http://199.116.235.204/words/success/graph/" + req.hashStr
                csv = "/mnt/vol/csvs/" + req.hashStr + ".csv"
                csvList.append(csv)
                urlList.append(url)
                # if the request involved word2vec, email the user a zip file containing matrices for the analysis
                matrixPath = '/mnt/vol/matrices/' + req.hashStr
                if (os.path.isdir(matrixPath)):    
                    matrices = zipMatrices(matrixPath, req.hashStr)
                    matrixList.append(matrices)
                #emailUser(req.hashStr)
            except:
                pass
            print('thread done')
        send_mail(self.email, urlList, csvList, errorDict, matrixList)
# make a list of requests
# requests = RequestsExecuteThread(requests)
# requests.run()

class Request(object):
    def execute(self):
        return Result(None)
    
class OverTimeRequest(Request):
    def __init__(self, dateRange, granularity):
        Request.__init__(self)
        self.dateRange = dateRange
        self.granularity = granularity
    def execute(self):
        return Result(None)

class WordFrequencyOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
        
    def execute(self):
        # get documents in time range and split by granularity
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        for word in self.wordList:
            xValues = []
            yValues = []
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                xValues.append(k)
                yValues.append(words.dataanalyzer.wordFrequency(chunk, word))
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
            
        return Result(self.granularity, 'Word Frequency Over Time', xValues, yDict)

class RelativeWordFrequencyOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
        
    def execute(self):
        
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        errors = []
        for word in self.wordList:
            xValues = []
            yValues = []
            
            # freqneucy of word in full corpus
            wordData = words.dataretrieval.getWordData(word)
            #if (len(wordData) == 0):
            #    errors.append(word+" does not appear in the corpus") # DO EXCEPTION HANDLING
            #else: # modified to use full frequency in a chunk instead of the whole corpus
                #fullFreq = 0.0
                #for thing in wordData:
                #    fullFreq = fullFreq + thing.word_count
                    
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                xValues.append(k)
                #yValues.append(words.dataanalyzer.relativeWordFrequency(chunk, word, fullFreq))
                yValues.append(words.dataanalyzer.relativeWordFrequency(chunk, word))
                
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
            
        return Result(self.granularity, 'Relative Word Frequency Over Time', xValues, yDict, errors)
  
class TfidfOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
        
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        errors = []
        for word in self.wordList:
            xValues = []
            yValues = []
            
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if (words.dataanalyzer.wordNotInChunkException(chunk, word)): # DO EXCEPTION HANDLING
                    xValues.append(k)
                    yValues.append(None)
                    errors.append("at x = " + str(k) + ": chunk did not contain " + word)
                else:
                    xValues.append(k)
                    yValues.append(words.dataanalyzer.averageTfidfOfWord(chunk, word))
                
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
            
        return Result(self.granularity, 'Tfidf Over Time', xValues, yDict, errors) 

class AverageValenceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        docs = words.dataretrieval.getDocumentDataWithWordFilter(self.dateRange[0], self.dateRange[1], self.wordList)
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)            
            yValues.append(words.dataanalyzer.averageValence(v))
        yDict = {}
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Valence"] = yValues
        
        return Result(self.granularity, 'Average Valence of Documents', xValues, yDict)

class AverageArousalOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        docs = words.dataretrieval.getDocumentDataWithWordFilter(self.dateRange[0], self.dateRange[1], self.wordList)
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageArousal(v))
        yDict = {}
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Arousal"] = yValues
        
        return Result(self.granularity, 'Average Arousal of Documents', xValues, yDict)
    
class AverageValenceFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        docs = words.dataretrieval.getDocumentDataWithWordFilter(self.dateRange[0], self.dateRange[1], self.wordList)
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValenceTopFive(v))
        yDict = {}
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Valence Top Five Words"] = yValues
        return Result(self.granularity, 'Average Valence of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
   
class AverageArousalFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        docs = words.dataretrieval.getDocumentDataWithWordFilter(self.dateRange[0], self.dateRange[1], self.wordList)
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageArousalTopFive(v))
        yDict = {}
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Arousal Top Five Words"] = yValues
        return Result(self.granularity, 'Average Arousal of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
  
class CosDistanceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, pairList, cbow, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.pairList = pairList
        self.cbow = cbow
        self.hashStr = hashStr
        
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        errors = []
        for pair in self.pairList:
            xValues = []
            yValues = []
            
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if (words.dataanalyzer.wordNotInChunkException(chunk, pair[0])): # DO EXCEPTION HANDLING
                    xValues.append(k)
                    yValues.append(None)
                    errors.append("at x = " + str(k) + ": chunk did not contain " + pair[0])
                else:
                    if (words.dataanalyzer.wordNotInChunkException(chunk, pair[1])): # DO EXCEPTION HANDLING
                        xValues.append(k)
                        yValues.append(None)
                        errors.append("at x = " + str(k) + ": chunk did not contain " + pair[1])
                    else:               
                        xValues.append(k)
                        yValues.append(words.dataanalyzer.cosDistanceOfPair(chunk, pair[0], pair[1], self.cbow, self.hashStr, k))
                
            xValues, yValues = sortXAndY(xValues, yValues)                
            yDict[pair] = yValues
            
        return Result(self.granularity, 'Cosine Distance', xValues, yDict, errors)  
    
class NClosestNeighboursOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, n, cbow, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.wordList = wordList
        self.n = n
        self.cbow = cbow
        self.hashStr = hashStr
        
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        errors = []
        for word in self.wordList:
            xValues = []
            yValues = []
            
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if (words.dataanalyzer.wordNotInChunkException(chunk, word)): # DO EXCEPTION HANDLING
                    xValues.append(k)
                    yValues.append(None)
                    errors.append("at x = " + str(k) + ": chunk did not contain " + word)
                else:
                    xValues.append(k)
                    yValues.append(words.dataanalyzer.nClosestNeighboursOfWord(chunk, word, self.n, self.cbow, self.hashStr, k))
                
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
            
        return Result(self.granularity, 'N Closest Neighbours', xValues, yDict, errors)   

class PairwiseProbabilitiesOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, pairList, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.pairList = pairList
        self.hashStr = hashStr
        
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        
        yDict = {}
        xValues = []
        errors = []
        for pair in self.pairList:
            xValues = []
            yValsXAndY = []
            yValsXGivenY = []
            yValsYGivenX = []
            yValsXGivenNotY = []
            yValsYGivenNotX = []
            
            for k,v in docHistogram.items():
            # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                    
                xValues.append(k)
                yValsXAndY.append(words.dataanalyzer.probXAndY(chunk, pair[0], pair[1]))
                #yValsXGivenY.append(words.dataanalyzer.probXGivenY(chunk, pair[0], pair[1]))
                
                xErrCode = words.dataanalyzer.probException(chunk, pair[0])
                yErrCode = words.dataanalyzer.probException(chunk, pair[1])
                
                if (xErrCode == 1): # DO EXCEPTION HANDLING
                    errors.append("For " + pair[1] + " given " + pair[0] + ": at x = " + str(k) + ": prob(" + pair[0] + ") = 0")
                    yValsYGivenX.append(None)
                else:
                    yValsYGivenX.append(words.dataanalyzer.probXGivenY(chunk, pair[1], pair[0]))
                    
                if (xErrCode == 2): # DO EXCEPTION HANDLING
                    errors.append("For " + pair[1] + " given not " + pair[0] + ": at x = " + str(k) + ": prob(not " + pair[0] + ") = 0")
                    yValsYGivenNotX.append(None)
                else:
                    yValsYGivenNotX.append(words.dataanalyzer.probXGivenNotY(chunk, pair[1], pair[0]))
                    
                if (yErrCode == 1): # DO EXCEPTION HANDLING
                    errors.append("For " + pair[0] + " given " + pair[1] + ": at x = " + str(k) + ": prob(" + pair[1] + ") = 0")
                    yValsXGivenY.append(None)
                else:
                    yValsXGivenY.append(words.dataanalyzer.probXGivenY(chunk, pair[0], pair[1]))
                    
                if (yErrCode == 2): # DO EXCEPTION HANDLING
                    errors.append("For " + pair[0] + " given not " + pair[1] + ": at x = " + str(k) + ": prob(not " + pair[1] + ") = 0")
                    yValsXGivenNotY.append(None)
                else:
                    yValsXGivenNotY.append(words.dataanalyzer.probXGivenNotY(chunk, pair[0], pair[1]))
                
            xValues1, yValsXAndY = sortXAndY(list(xValues), yValsXAndY)
            xValues2, yValsXGivenY = sortXAndY(list(xValues), yValsXGivenY)
            xValues3, yValsYGivenX = sortXAndY(list(xValues), yValsYGivenX)
            xValues4, yValsXGivenNotY = sortXAndY(list(xValues), yValsXGivenNotY)
            xValues5, yValsYGivenNotX = sortXAndY(list(xValues), yValsYGivenNotX)
            
            yDict[(pair, "XAndY")] = yValsXAndY
            yDict[(pair, "XGivenY")] = yValsXGivenY
            yDict[(pair, "YGivenX")] = yValsYGivenX
            yDict[(pair, "XGivenNotY")] = yValsXGivenNotY
            yDict[(pair, "YGivenNotX")] = yValsYGivenNotX
            
            print("XVALUES1", xValues1)
    
        return Result(self.granularity, 'Pairwise Probabilities', xValues1, yDict, errors)

class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues, errors=None):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues
        self.errors = errors # List of strings in the format: "Error at x = someDate: chunk did not contain someWord". List is empty or None if there are no errors
    def generateCSV(self, hashStr):
        #with open(filePath + hashStr + '.csv', 'w') as csvfile:
        #    resultWriter = csv.writer(csvfile, dialect='excel')
        #    resultWriter.writerow([self.xTitle, self.yTitle])
        #    for i in range(len(self.xValues)):
        #        resultWriter.writerow([self.xValues[i], self.yValues[i]])
        with open(filePath + hashStr + '.csv', 'w') as csvfile:
            resultWriter = csv.writer(csvfile, dialect='excel')
            resultWriter.writerow([self.xTitle, self.yTitle, "keywords"])
            for key in self.yValues:
                print("KEY!!!", key)
                print(len(self.xValues))
                print(self.xValues)
                print(self.yValues)
                for i in range(len(self.xValues)):
                    print("for i in range")
                    resultWriter.writerow([self.xValues[i], self.yValues[key][i], key])
    def saveModel():
        model = ResultModel(params)
        model.save()

# sort parallel lists based on the first list
def sortXAndY(xValues, yValues):
    if (len(xValues) < 1):
        return xValues, yValues
    xValues, yValues = (list(t) for t in zip(*sorted(zip(xValues, yValues))))
    return xValues, yValues

# granularity parameter is for now a string that can be Year or Month
    
# for now, structure every request as a request for some parameter to be evaluated over time
# all requests have a date range (choose a section of the corpus), time granularity (week, year, etc), and parameters (examined over time)
# possible parameters: avg valence, avg arousal, avg valence top 5 words, avg arousal top 5 words, tfidf, cosine distance for a word pair, N closest neighbors for a word
# later: word frequency, rel. word frequency, pairwise conditional probabilities
# a result is therefore a mapping of parameter values to times

# 1 - retrieve documents that fall in the date range
# 2 - split the documents into chunks based on time granularity
# 3 - compute the parameter of interest for each chunk
# 4 - wrap the result

# later the user might also request the raw data. this is a different type of request
