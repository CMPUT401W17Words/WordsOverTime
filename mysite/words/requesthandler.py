# This is the "coordinator" module that calls on other modules to process a client request

from words.models import Document
import words.dataretrieval
import words.dataanalyzer

class Request():
    def execute(self):
        return Result(None)
    
class OverTimeRequest(Request):
    def __init__(self, dateRange, granularity):
        super(OverTimeRequest, self).__init__()
        self.dateRange = dateRange
        self.granularity = granularity
    def execute(self):
        return Result(None)
    
class TfidfOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word):
        super(TfidfOverTimeRequest, self).__init__(dateRange, granularity)
        self.word = word
    def execute(self):
        return Result(None)
    
class CosDistanceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word1, word2):
        super(CosDistanceOverTimeRequest, self).__init__(dateRange, granularity)
        self.word1 = word1
        self.word2 = word2
    def execute(self):
        docs = words.dataretrieval.getDocuments(self.dateRange[0], self.dateRange[1])[0]
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
            yValues.append(words.dataanalyzer.cosDistanceOfPair(chunk, self.word1, self.word2))
        return Result(self.granularity, 'Cosine Distance of '+self.word1+' and '+self.word2, xValues, yValues)  
    
class NClosestNeighboursOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word, n):
        super(NClosestNeighboursOverTimeRequest, self).__init__(dateRange, granularity)
        self.word = word
        self.n = n
    def execute(self):
        docs = words.dataretrieval.getDocuments(self.dateRange[0], self.dateRange[1])[0]
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
            yValues.append(words.dataanalyzer.nClosestNeighboursOfWord(chunk, self.word, self.n))
        return Result(self.granularity, 'N closest neighbors of '+self.word, xValues, yValues)   

class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues

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