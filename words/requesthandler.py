# This is the "coordinator" module that calls on other modules to process a client request

import csv
from words.models import Document_Data
import words.dataretrieval
import words.dataanalyzer

filePath = '/mnt/vol/csvs/'

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
    
class TfidfOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.word = word
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            # v is a list of Documents
            chunk = []
            for doc in v:
                wordss = words.dataretrieval.getWordsInDocument(doc)
                chunk.append(wordss)
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageTfidfOfWord(chunk, self.word))
        xValues, yValues = sortXAndY(xValues, yValues)
        return Result(self.granularity, 'Tfidf Over Time of '+self.word, xValues, yValues) 

class AverageValenceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity):
        OverTimeRequest.__init__(self,dateRange, granularity)
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        return Result(self.granularity, 'Average Valence of Documents', xValues, yValues)

class AverageArousalOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity):
        OverTimeRequest.__init__(self,dateRange, granularity)
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        return Result(self.granularity, 'Average Arousal of Documents', xValues, yValues)
    
class AverageValenceFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity):
        OverTimeRequest.__init__(self,dateRange, granularity)
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        return Result(self.granularity, 'Average Valence of Documents Using Top Five Tfidfs In Each Document', xValues, yValues)
    
class AverageArousalFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity):
        OverTimeRequest.__init__(self,dateRange, granularity)
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            xValues.append(k)
            yValues.append(words.dataanalyzer.averageValence(v))
        return Result(self.granularity, 'Average Arousal of Documents Using Top Five Tfidfs In Each Document', xValues, yValues)
    
class CosDistanceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word1, word2, cbow):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.word1 = word1
        self.word2 = word2
        self.cbow = cbow
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            # v is a list of Documents
            chunk = []
            for doc in v:
                wordss = words.dataretrieval.getWordsInDocument(doc)
                chunk.append(wordss)
            xValues.append(k)
            yValues.append(words.dataanalyzer.cosDistanceOfPair(chunk, self.word1, self.word2, self.cbow))
        xValues, yValues = sortXAndY(xValues, yValues)
        return Result(self.granularity, 'Cosine Distance of '+self.word1+' and '+self.word2, xValues, yValues)  
    
class NClosestNeighboursOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word, n, cbow):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.word = word
        self.n = n
        self.cbow = cbow
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram.items():
            # v is a list of Documents
            chunk = []
            for doc in v:
                wordss = words.dataretrieval.getWordsInDocument(doc)
                chunk.append(wordss)
            xValues.append(k)
            yValues.append(words.dataanalyzer.nClosestNeighboursOfWord(chunk, self.word, self.n, self.cbow))
        xValues, yValues = sortXAndY(xValues, yValues)
        return Result(self.granularity, 'N closest neighbors of '+self.word, xValues, yValues)   

class PairwiseProbabilitiesOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word1, word2):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.word1 = word1
        self.word2 = word2
    def execute(self):
        docs = words.dataretrieval.getDocumentData(self.dateRange[0], self.dateRange[1])#[0]
        docHistogram = words.dataretrieval.splitDocuments(docs, self.granularity)
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
        return{'XAndY':Result(self.granularity, 'p(' + self.word1 +',' + self.word2+')', xValues1, yValsXAndY),
               'XGivenY':Result(self.granularity, 'p(' + self.word1 +'|' + self.word2+')', xValues2, yValsXGivenY),
               'YGivenX':Result(self.granularity, 'p(' + self.word2 +'|' + self.word1+')', xValues3, yValsYGivenX),
               'XGivenNotY':Result(self.granularity, 'p(' + self.word1 +'|~' + self.word2+')', xValues4, yValsXGivenNotY),
               'YGivenNotX':Result(self.granularity, 'p(' + self.word2 +'|~' + self.word1+')', xValues5, yValsYGivenNotX)}
    
class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues
    def generateCSV(self, hashStr):
        with open(filePath + hashStr + '.csv', 'w') as csvfile:
            resultWriter = csv.writer(csvfile, dialect='excel')
            resultWriter.writerow([self.xTitle, self.yTitle])
            for i in range(len(self.xValues)):
                resultWriter.writerow([self.xValues[i], self.yValues[i]])
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
