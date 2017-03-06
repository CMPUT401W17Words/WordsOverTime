from models import Document
import dataretrieval
import dataanalyzer

def __init__(self):
    self.requests = []
    def addRequest(request):
        self.requests.append(request)

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
        super(TfidfOverTimeRequest, self).__init__(dateRange, granularity)
        self.word1 = word1
        self.word2 = word2
    def execute(self):
        docs = dataretrieval.getDocuments(self.dateRange[0], self.dateRange[1])
        docHistogram = splitDocuments(docs, self.granularity)
        xValues = []
        yValues = []
        for k,v in docHistogram:
            xValues.append(k)
            yValues.append(dataanalyzer.cosDistanceOfPair(v, self.word1, self.word2))
        return Result(granularity, 'Cosine Distance of '+self.Word1+' and '+self.Word2, xValues, yValues)  
    
class NClosestNeighboursOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, word, n):
        super(TfidfOverTimeRequest, self).__init__(dateRange, granularity)
        self.word = word
        self.n = n
    def execute(self):
        return Result(None)  

class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues

# granularity parameter is for now a string that can be Year or Month

# split a list of documents into sublists based on a specified time granularity        
def splitDocuments(documents, granularity):
    result = {} # keys are time bins, values are lists of documents falling into that bin
    if (granularity == 'Year'):
        for doc in documents:
            year = doc.publicationDate
            if year not in result:
                result[year] = []
            result[year].append(doc)    
    if (granularity == 'Month'):
        for doc in documents:
            month = doc.publicationDate
            if month not in result:
                result[month] = []
            result[month].append(doc)
    return result
    
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