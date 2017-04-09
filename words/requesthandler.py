# This is the "coordinator" module that calls on other modules to process a client request

import csv
from words.models import Document_Data, Articles_Can, Sentiment_Dict, Word_Data
import words.dataretrieval
import words.dataanalyzer
from words.emailsending import *
filePath = '/mnt/vol/csvs/'
from django.db.models import Sum, When, IntegerField, Case, Count, Avg, Q
from django.db.models.functions import Trunc
from datetime import date
from threading import Thread

import os
import zipfile
import sys
import shutil 
        
# http://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory/
def zipMatrices(matricesPath, hashStr):
    shutil.make_archive(matricesPath, 'zip', matricesPath, hashStr)

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
                if (req.__class__.__name__ != "NClosestNeighboursOverTimeRequest"):
                    urlList.append(url)
                # if the request involved word2vec, email the user a zip file containing matrices for the analysis
                matrixPath = '/mnt/vol/matrices/' + req.hashStr
                print(matrixPath)
                print(os.path.isdir(matrixPath))
                if (os.path.isdir(matrixPath)):
                    matrices = matrixPath+'.zip'
                    print(matrices)                    
                    matrixList.append(matrices)
                    zipMatrices(matrixPath, req.hashStr)
            except Exception as e:
                errorDict[''] = [str(e)]
            print('thread done')
        send_mail(self.email, urlList, csvList, errorDict, matrixList)

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
     
        wordData = words.dataretrieval.getChunks('Word_Data', self.dateRange, self.granularity) 
        yDict = {}
        xValues = []
        for wordd in self.wordList:
            xValues = []
            yValues = []            
            currentWordData = wordData.annotate(wcount=Sum(Case(When(word=wordd, then='word_count'))))
            #print('QUERY for word frequency: ', currentWordData.query)
            for item in currentWordData:
                print(item)
                xValues.append(item[0])
                wordCount = item[1]
                if (wordCount is None):
                    wordCount = 0
                yValues.append(wordCount)
                    
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[wordd] = yValues                
            
        return Result(self.granularity, 'Word Frequency Over Time', xValues, yDict)

class RelativeWordFrequencyOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
        
    def execute(self):
        
        wordData = words.dataretrieval.getChunks('Word_Data', self.dateRange, self.granularity)
        totalWordData = wordData.annotate(wcount=Sum('word_count'))
        yDict = {}
        xValues = []
        errors = []
        for wordd in self.wordList:
            xValues = []
            yValues = []
            currentWordData = totalWordData.annotate(wdcount=Sum(Case(When(word=wordd, then='word_count'))))
            #print('QUERY for relative word frequency: ', currentWordData.query)
            for item in currentWordData:
                chunkDate = item[0]
                wordCount = item[2]
                totalWordCount = item[1]
                xValues.append(chunkDate)
                if (totalWordCount == None):
                    yValues.append(None)
                    errors.append("at x = " + str(chunkDate) + ": chunk did not contain any words")
                else:
                    if (wordCount == None):
                        wordCount = 0
                    yValues.append(float(wordCount)/totalWordCount)
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[wordd] = yValues      
            
        return Result(self.granularity, 'Relative Word Frequency Over Time', xValues, yDict, errors)
  
class TfidfOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.wordList = wordList
        self.hashStr = hashStr
        
    def execute(self):
        
        docs = words.dataretrieval.getChunks('Articles_Can', self.dateRange, self.granularity)
        #print('QUERY for tfidf: ', docs.query)
        dateToChunk = initDict(self.dateRange, self.granularity)
        for doc in docs:
            dateToChunk[doc[0]].append(doc[1].split())
        yDict = {}
        xValues = []
        errors = []
        for word in self.wordList:
            xValues = []
            yValues = []         
            for k,v in dateToChunk.items():
                xValues.append(k)
                try:
                    avgTfidf = words.dataanalyzer.averageTfidfOfWord(v, word)
                except:
                    avgTfidf = None
                    errors.append("at x = " + str(k) + ": chunk did not contain " + word)
                yValues.append(avgTfidf)
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues            
            
        return Result(self.granularity, 'Tfidf Over Time', xValues, yDict, errors) 

class AverageValenceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        
        if (self.wordList == [] or self.wordList == None):
            filteredArticles = Document_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1])).annotate(chunk=Trunc('publication_Date', self.granularity.lower())).values_list('chunk').annotate(avg_val=Avg('average_valence_doc'))
        else:
            preQuery = Word_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1]))      
            filters = []
            for wordd in self.wordList:
                filters.append(preQuery.filter(word=wordd).values_list('article_id'))
            filteredArticles = Document_Data.objects.all()
            for fil in filters:
                filteredArticles = filteredArticles.filter(article_id__in=fil)
            filteredArticles = filteredArticles.annotate(chunk=Trunc('publication_Date', self.granularity.lower())).values_list('chunk').annotate(avg_val=Avg('average_valence_doc'))
        
        #print('QUERY for valence: ', filteredArticles.query)
        
        xValues = []
        yValues = []        
        for item in filteredArticles:
            xValues.append(item[0])
            yValues.append(item[1])    
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
        
        if (self.wordList == [] or self.wordList == None):
            filteredArticles = Document_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1])).annotate(chunk=Trunc('publication_Date', self.granularity.lower())).values_list('chunk').annotate(avg_val=Avg('average_arousal_doc'))
        else:
            preQuery = Word_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1]))      
            filters = []
            for wordd in self.wordList:
                filters.append(preQuery.filter(word=wordd).values_list('article_id'))
            filteredArticles = Document_Data.objects.all()
            for fil in filters:
                filteredArticles = filteredArticles.filter(article_id__in=fil)
            filteredArticles = filteredArticles.annotate(chunk=Trunc('publication_Date', self.granularity.lower())).values_list('chunk').annotate(avg_val=Avg('average_arousal_doc'))
        
        #print('QUERY for arousal: ', filteredArticles.query)
        
        xValues = []
        yValues = []        
        for item in filteredArticles:
            xValues.append(item[0])
            yValues.append(item[1])
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
        
        if (self.wordList == [] or self.wordList == None):
            filteredArticles = Articles_Can.objects.filter(publicationDate__range=(self.dateRange[0], self.dateRange[1])).annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk', 'parsed_article')
        else:
            preQuery = Word_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1]))      
            filters = []
            for wordd in self.wordList:
                filters.append(preQuery.filter(word=wordd).values_list('article_id'))
            filteredArticles = Articles_Can.objects.all()
            for fil in filters:
                filteredArticles = filteredArticles.filter(article_id__in=fil)
            filteredArticles = filteredArticles.annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk', 'parsed_article')
        
        #print('QUERY for valence 5: ', filteredArticles.query)
        
        dateToChunk = initDict(self.dateRange, self.granularity)
        for doc in filteredArticles:
            dateToChunk[doc[0]].append(doc[1].split())
        yDict = {}
        xValues = []
        errors = []
        yValues = []         
        for k,v in dateToChunk.items():
            xValues.append(k)
            try:
                avgVal = words.dataanalyzer.averageValenceTopFive(v)
            except:
                avgVal = None
                errors.append("at x = " + str(k) + ": there was an error")
            yValues.append(avgVal)
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Valence Top Five Words"] = yValues
            
        return Result(self.granularity, 'Average Valence of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
   
class AverageArousalFiveWordsOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, wordList, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.hashStr = hashStr
        self.wordList = wordList
        
    def execute(self):
        if (self.wordList == [] or self.wordList == None):
            filteredArticles = Articles_Can.objects.filter(publicationDate__range=(self.dateRange[0], self.dateRange[1])).annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk', 'parsed_article')
        else:
            preQuery = Word_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1]))      
            filters = []
            for wordd in self.wordList:
                filters.append(preQuery.filter(word=wordd).values_list('article_id'))
            filteredArticles = Articles_Can.objects.all()
            for fil in filters:
                filteredArticles = filteredArticles.filter(article_id__in=fil)
            filteredArticles = filteredArticles.annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk', 'parsed_article')
        
        #print('QUERY for arousal 5: ', filteredArticles.query)
        
        dateToChunk = initDict(self.dateRange, self.granularity)
        for doc in filteredArticles:
            dateToChunk[doc[0]].append(doc[1].split())
        yDict = {}
        xValues = []
        errors = []
        yValues = []         
        for k,v in dateToChunk.items():
            xValues.append(k)
            try:
                avgAro = words.dataanalyzer.averageArousalTopFive(v)
            except:
                avgAro = None
                errors.append("at x = " + str(k) + ": there was an error")
            yValues.append(avgAro)
        xValues, yValues = sortXAndY(xValues, yValues)
        yDict["Average Valence Top Five Words"] = yValues
        
        return Result(self.granularity, 'Average Arousal of Documents Using Top Five Tfidfs In Each Document', xValues, yDict)
  
class CosDistanceOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, pairList, cbow, hashStr):
        OverTimeRequest.__init__(self,dateRange, granularity)
        self.pairList = pairList
        self.cbow = cbow
        self.hashStr = hashStr
        
    def execute(self):
        
        docs = words.dataretrieval.getChunks('Articles_Can', self.dateRange, self.granularity)
        #print('QUERY for cos distance: ', docs.query)
        dateToChunk = initDict(self.dateRange, self.granularity)
        for doc in docs:
            dateToChunk[doc[0]].append(doc[1].split())
        yDict = {}
        xValues = []
        errors = []
        for pair in self.pairList:
            xValues = []
            yValues = []         
            for k,v in dateToChunk.items():
                xValues.append(k)
                try:
                    cosDist = words.dataanalyzer.cosDistanceOfPair(v, pair[0], pair[1], self.cbow, self.hashStr, k)
                except:
                    cosDist = None
                    errors.append("at x = " + str(k) + ": chunk did not contain " + pair[0] + " or " + pair[1])
                yValues.append(cosDist)
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

        docs = words.dataretrieval.getChunks('Articles_Can', self.dateRange, self.granularity)
        #print('QUERY for n closest: ', docs.query)
        dateToChunk = initDict(self.dateRange, self.granularity)
        for doc in docs:
            dateToChunk[doc[0]].append(doc[1].split())
        yDict = {}
        xValues = []
        errors = []
        for word in self.wordList:
            xValues = []
            yValues = []         
            for k,v in dateToChunk.items():
                xValues.append(k)
                try:
                    nNeighbours = words.dataanalyzer.nClosestNeighboursOfWord(v, word, self.n, self.cbow, self.hashStr, k)
                except:
                    nNeighbours = None
                    errors.append("at x = " + str(k) + ": chunk did not contain " + word)
                yValues.append(nNeighbours)
            xValues, yValues = sortXAndY(xValues, yValues)
            yDict[word] = yValues         
            
        return Result(self.granularity, 'N Closest Neighbours', xValues, yDict, errors)   

class PairwiseProbabilitiesOverTimeRequest(OverTimeRequest):
    def __init__(self, dateRange, granularity, pairList, hashStr):
        OverTimeRequest.__init__(self, dateRange, granularity)
        self.pairList = pairList
        self.hashStr = hashStr
        
    def execute(self):
        yDict = {}
        xValsXAndY = []
        xValsXGivenY = []
        xValsYGivenX = []
        xValsXGivenNotY = []
        xValsYGivenNotX = []              
        yValsXAndY = []
        yValsXGivenY = []
        yValsYGivenX = []
        yValsXGivenNotY = []
        yValsYGivenNotX = []      
        errors = []
        
        preQuery = Word_Data.objects.filter(publication_Date__range=(self.dateRange[0], self.dateRange[1]))
        baseQuery = preQuery.annotate(chunk=Trunc('publication_Date', self.granularity.lower())).values_list('chunk')
        
        totalArticles = baseQuery.annotate(art_count=Count('article_id', distinct=True))
        #print('QUERY for total articles: ', totalArticles.query)
            
        for pair in self.pairList:
            xValsXAndY = []
            xValsXGivenY = []
            xValsYGivenX = []
            xValsXGivenNotY = []
            xValsYGivenNotX = []              
            yValsXAndY = []
            yValsXGivenY = []
            yValsYGivenX = []
            yValsXGivenNotY = []
            yValsYGivenNotX = []
            
            w1Count = baseQuery.filter(word=pair[0]).annotate(w1_count=Count('article_id'))
            #print('QUERY for w1: ', w1Count.query)
                
            w2Count = baseQuery.filter(word=pair[1]).annotate(w2_count=Count('article_id'))
            #print('QUERY for w2: ', w2Count.query)
            
            w1Articles = preQuery.filter(word=pair[0]).values_list('article_id')
            w2Articles = preQuery.filter(word=pair[1]).values_list('article_id')
            
            w1Andw2Count = Articles_Can.objects.filter(Q(article_id__in=w1Articles)).filter(Q(article_id__in=w2Articles)).annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk').annotate(w1w2_count=Count('article_id'))
            #print('QUERY for w1w2: ', w1Andw2Count.query)
            
            w1Notw2Count = Articles_Can.objects.filter(Q(article_id__in=w1Articles)).exclude(Q(article_id__in=w2Articles)).annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk').annotate(w1notw2_count=Count('article_id'))
            #print('QUERY for w1notw2: ', w1Notw2Count.query)
                
            w2Notw1Count = Articles_Can.objects.filter(Q(article_id__in=w2Articles)).exclude(Q(article_id__in=w1Articles)).annotate(chunk=Trunc('publicationDate', self.granularity.lower())).values_list('chunk').annotate(w2notw1_count=Count('article_id'))
            #print('QUERY for w2notw1: ', w2Notw1Count.query)
                         
            for itemA in totalArticles:
                xValsXAndY.append(itemA[0])
                itemFound = False
                for itemB in w1Andw2Count:
                    if (itemB[0] == itemA[0]):
                        try:
                            prob = itemB[1]/itemA[1]
                        except:
                            prob = None
                            errors.append("at x = " + str(itemA[0]) + "no words found")
                        yValsXAndY.append(prob)
                        itemFound = True
                        break
                if (not itemFound):
                    yValsXAndY.append(0)
            xValsXAndY, yValsXAndY = sortXAndY(xValsXAndY, yValsXAndY)
            yDict[(pair, "XAndY")] = yValsXAndY      
            
            totalArticles = orderTuples(xValsXAndY,totalArticles)
            w1Count = orderTuples(xValsXAndY,w1Count)
            w2Count = orderTuples(xValsXAndY,w2Count)
            w1Andw2Count = orderTuples(xValsXAndY,w1Andw2Count)
            w1Notw2Count = orderTuples(xValsXAndY,w1Notw2Count)
            w2Notw1Count = orderTuples(xValsXAndY,w2Notw1Count)
            
            for itemA,itemB in zip(w1Andw2Count, w2Count):
                try:
                    prob = itemA[1]/itemB[1]
                except:
                    if (itemB[1] == None or itemB[1] == 0):
                        prob = None
                        errors.append("For " + pair[0] + " given " + pair[1] + ": at x = " + str(itemA[0]) + ": prob(" + pair[1] + ") = 0")
                    else:
                        prob = 0
                xValsXGivenY.append(itemA[0])    
                yValsXGivenY.append(prob)
            yDict[(pair, "XGivenY")] = yValsXGivenY
            
            for itemA,itemB in zip(w1Andw2Count, w1Count):
                try:
                    prob = itemA[1]/itemB[1]
                except:
                    if (itemB[1] == None or itemB[1] == 0):
                        prob = None
                        errors.append("For " + pair[1] + " given " + pair[0] + ": at x = " + str(itemA[0]) + ": prob(" + pair[0] + ") = 0")
                    else:
                        prob = 0
                xValsYGivenX.append(itemA[0])    
                yValsYGivenX.append(prob)
            yDict[(pair, "YGivenX")] = yValsYGivenX
            
            for itemA,itemB,itemC in zip(w1Notw2Count, w2Count, totalArticles):
                try:
                    diff = itemC[1]-itemB[1]
                    prob = itemA[1]/diff
                except:
                    if (diff == 0 or itemB[1] == None or itemC[1] == None):
                        prob = None
                        errors.append("For " + pair[0] + " given not " + pair[1] + ": at x = " + str(itemA[0]) + ": prob(not " + pair[1] + ") = 0")
                    else:
                        prob = 0
                xValsXGivenNotY.append(itemA[0])    
                yValsXGivenNotY.append(prob)
            yDict[(pair, "XGivenNotY")] = yValsXGivenNotY
            
            for itemA,itemB,itemC in zip(w2Notw1Count, w1Count, totalArticles):
                try:
                    diff = itemC[1]-itemB[1]
                    prob = itemA[1]/diff
                except:
                    if (diff == 0 or itemB[1] == None or itemC[1] == None):
                        prob = None
                        errors.append("For " + pair[1] + " given not " + pair[0] + ": at x = " + str(itemA[0]) + ": prob(not " + pair[0] + ") = 0")
                    else:
                        prob = 0
                xValsYGivenNotX.append(itemA[0])    
                yValsYGivenNotX.append(prob)
            yDict[(pair, "YGivenNotX")] = yValsYGivenNotX            
    
        return Result(self.granularity, 'Pairwise Probabilities', xValsYGivenNotX, yDict, errors)

class Result():
    def __init__(self, xTitle, yTitle, xValues, yValues, errors=None):
        self.xTitle = xTitle # string describing the x-axis. basically time frame and granularity
        self.yTitle = yTitle # string describing the y-axis. basically the parameter that was being calculated
        self.xValues = xValues # xValues and yValues are parallel lists that together construct a scatterplot
        self.yValues = yValues
        self.errors = errors # List of strings in the format: "Error at x = someDate: chunk did not contain someWord". List is empty or None if there are no errors
    def generateCSV(self, hashStr):
        with open(filePath + hashStr + '.csv', 'w') as csvfile:
            resultWriter = csv.writer(csvfile, dialect='excel')
            resultWriter.writerow([self.xTitle, self.yTitle, "keywords"])
            for key in self.yValues:
                for i in range(len(self.xValues)):
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

def initDict(dateRange, granularity):
    result = {}
    if (granularity == 'Year'):
        for yr in range(dateRange[0].year, dateRange[1].year+1):
            result[date(yr,1,1)] = []
    if (granularity == 'Month'):
        for yr in range(dateRange[0].year, dateRange[1].year+1):
            for mn in range(1,13):
                result[date(yr,mn,1)] = []
    if (granularity == 'Week'):
        pass
    return result

# take a list of ordered dates (like a sorted xValues) and a list of tuples containing unordered dates, and return the tuple list with dates in correct order and missing dates filled in
def orderTuples(dateList, tupleList):
    result = []
    for d in dateList:
        itemFound = False
        for item in tupleList:
            if (d == item[0]):
                result.append(item)
                itemFound = True
                break
        if (not itemFound):
            result.append((d, 0))
    return result