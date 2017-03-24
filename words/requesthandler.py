# This is the "coordinator" module that calls on other modules to process a client request

import csv
from words.models import Document_Data
import words.dataretrieval
import words.dataanalyzer

filePath = '/mnt/vol/csvs/'

from threading import Thread

class RequestsExecuteThread(Thread):
    def __init__(self, requests):
        Thread.__init__(self)
        self.requests = requests

    def run(self):
        for req in self.requests:
            print('thread start')
            res = req.execute()
            res.generateCSV(req.hashStr)
            #emailUser(req.hashStr)
            print('thread done')

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
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yDict = {}
        for word in self.wordList:
            yValues = []
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if(k not in xValues):
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
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yDict = {}
        for word in self.wordList:
            yValues = []
            wordData = words.dataretrieval.getWordData(word)
            fullFreq = 0.0
            for thing in wordData:
                fullFreq = fullFreq + thing.word_count  
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if(k not in xValues):
                    xValues.append(k)
                yValues.append(words.dataanalyzer.relativeWordFrequency(chunk, word, fullFreq))
                xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
        return Result(self.granularity, 'Relative Word Frequency Over Time', xValues, yDict)
    
class TfidfOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yDict = {}
        for word in self.wordList:
            yValues = []
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if(k not in xValues):
                    xValues.append(k)
                yValues.append(words.dataanalyzer.averageTfidfOfWord(chunk, word))
                xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
        return Result(self.granularity, 'Tfidf Over Time', xValues, yDict) 

class AverageValenceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)            
            yValues.append(words.dataanalyzer.averageValence(v))
        yDict = {}
        yDict["Average Valence"] = yValues
        return Result(self.granularity, 'Average Valence of Documents', xValues, yDict)

class AverageArousalOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        yDict = {}
        yDict["Average Arousal"] = yValues
        return Result(self.granularity, 'Average Arousal of Documents', xValues, yDict)
    
class AverageValenceFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        yDict = {}
        yDict["test"] = yValues
        return Result(self.granularity, 'Average Valence of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
    
class AverageArousalFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        yDict = {}
        yDict["test"] = yValues
        return Result(self.granularity, 'Average Arousal of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
    
class CosDistanceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, pairList, cbow, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.pairList = pairList
        self.cbow = cbow
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yDict = {}
        for pair in self.pairList:
            yValues = []
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if(k not in xValues):
                    xValues.append(k)
                yValues.append(words.dataanalyzer.cosDistanceOfPair(chunk, pair[0], pair[1], self.cbow))
                xValues, yValues = sortXAndY(xValues, yValues)
            yDict[pair] = yValues
        return Result(self.granularity, 'Cosine Distance', xValues, yDict)  
    
class NClosestNeighboursOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, n, cbow, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.wordList = wordList
        self.n = n
        self.cbow = cbow
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yDict = {}
        for word in self.wordList:
            yValues = []
            for k,v in docHistogram.items():
                # v is a list of Documents
                chunk = []
                for doc in v:
                    wordss = words.dataretrieval.getWordsInDocument(doc)
                    chunk.append(wordss)
                if(k not in xValues):
                    xValues.append(k)
                yValues.append(words.dataanalyzer.nClosestNeighboursOfWord(chunk, word, self.n, self.cbow))
                xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues
        return Result(self.granularity, 'N closest neighbors', xValues, yDict)   

class PairwiseProbabilitiesOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word1, word2, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.word1 = word1
        self.word2 = word2
        self.hashStr = hashStr
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValsXAndY = []
        yValsXGivenY = []
        yValsYGivenX = []
        yValsXGivenNotY = []
        yValsYGivenNotX = []
        yDictXAndY = {}
        yDictXGivenY = {}
        yDictYGivenX = {}
        yDictXGivenNotY = {}
        yDictYGivenNotX = {}
        for k,v in docHistogram.items():
            # v is a list of Documents
            chunk = []
            for doc in v:
                wordss = words.dataretrieval.getWordsInDocument(doc)
                chunk.append(wordss)
            xValues.append(k)
            yValsXAndY.append(words.dataanalyzer.probXAndY(chunk, self.word1, self.word2))
            yValsXGivenY.append(words.dataanalyzer.probXGivenY(chunk, self.word1, self.word2))
            yValsYGivenX.append(words.dataanalyzer.probXGivenY(chunk, self.word2, self.word1))
            yValsXGivenNotY.append(words.dataanalyzer.probXGivenNotY(chunk, self.word1, self.word2))
            yValsYGivenNotX.append(words.dataanalyzer.probXGivenNotY(chunk, self.word2, self.word1))
        xValues1, yValsXAndY = sortXAndY(list(xValues), yValsXAndY)
        xValues2, yValsXGivenY = sortXAndY(list(xValues), yValsXGivenY)
        xValues3, yValsYGivenX = sortXAndY(list(xValues), yValsYGivenX)
        xValues4, yValsXGivenNotY = sortXAndY(list(xValues), yValsXGivenNotY)
        xValues5, yValsYGivenNotX = sortXAndY(list(xValues), yValsYGivenNotX)
        yDictXAndY["XAndY"] = yValsXAndY
        yDictXGivenY["XGivenY"] = yValsXGivenY
        yDictYGivenX["YGivenX"] = yValsYGivenX
        yDictXGivenNotY["XGivenNotY"] = yValsXGivenNotY
        yDictYGivenNotX["YGivenNotX"] = yValsYGivenNotX
        return{'XAndY':Result(self.granularity, 'p(' + self.word1 +',' + self.word2+')', xValues1, yDictXAndY),
               'XGivenY':Result(self.granularity, 'p(' + self.word1 +'|' + self.word2+')', xValues2, yDictXGivenY),
               'YGivenX':Result(self.granularity, 'p(' + self.word2 +'|' + self.word1+')', xValues3, yDictYGivenX),
               'XGivenNotY':Result(self.granularity, 'p(' + self.word1 +'|~' + self.word2+')', xValues4, yDictXGivenNotY),
               'YGivenNotX':Result(self.granularity, 'p(' + self.word2 +'|~' + self.word1+')', xValues5, yDictYGivenNotX)}
    
class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues
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
                for i in range(len(self.xValues)):
                    resultWriter.writerow([self.xValues[i], self.yValues[key][i], key])
    def saveModel():
        model = ResultModel(params)
        model.save()
                
def sortXAndY(xValues, yValues):
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
