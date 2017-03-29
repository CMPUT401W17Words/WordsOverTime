from datetime import date

from django.test import TestCase

import words.dataretrieval
import words.requesthandler
#import words.databaseinput
from words.models import Document_Data, Word_Data, Sentiment_Dict, Articles_Can
import csv
import decimal
from datetime import date
# Create your tests here.

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.sentDict = []
        self.artCan = []
        self.docData = []
        self.wordData = []
        
        with open(r'words\sentiment_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
            file = csv.DictReader(csvfile)
            for line in file:
                self.sentDict.append(Sentiment_Dict(word=line['Word'], valence=line['Valence'],arousal=line['Arousal'],dominance=0.0,concreteness=0.0,aoa=0.0))
        
        for item in self.sentDict:
            item.save()        
                
        with open(r'words\corpus_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
            file = csv.DictReader(csvfile)
            for line in file:
                self.artCan.append(Articles_Can(article_id=line['articleID'], language=line['language'],province=line['province'],city=line['city'],country=line['country'],publicationDate=line['publicationDate'],wordCount=line['wordCount'],parsed_article=line['parsedArticle']))
                
                words = line['parsedArticle'].split()
                avgArousal = decimal.Decimal(0.0)
                avgValence = decimal.Decimal(0.0)
                wordCounts = {}
                for wd in words:
                    sent = Sentiment_Dict.objects.get(word=wd)
                    avgArousal = avgArousal + sent.arousal
                    avgValence = avgValence + sent.valence
                    if wd not in wordCounts:
                        wordCounts[wd] = 0
                    wordCounts[wd] = wordCounts[wd] + 1
                    
                for k,v in wordCounts.items():
                    self.wordData.append(Word_Data(word=k,article_id=line['articleID'],word_count=v,term_frequency=0,tfidf=0))
                    
                avgArousal = avgArousal/len(words)
                avgValence = avgValence/len(words)
                
                self.docData.append(Document_Data(article_id=line['articleID'], language=line['language'],province=line['province'],city=line['city'],country=line['country'],publication_Date=line['publicationDate'],word_count=len(words),average_arousal_doc=avgArousal,average_valence_doc=avgValence,average_arousal_words=0,average_valence_words=0))
                
        for item in self.artCan:
            item.save()
        for item in self.docData:
            item.save()
        for item in self.wordData:
            item.save()    
        
    def testGetArousal(self):
        self.assertEqual(words.dataretrieval.getArousal('minors'), 0.57294869)
        self.assertEqual(words.dataretrieval.getArousal('computer'), 0.37374821)
        self.assertEqual(words.dataretrieval.getArousal('response'), 0.36475822)
    
    def testGetValence(self):
        self.assertEqual(words.dataretrieval.getValence('minors'), 0.42352934)
        self.assertEqual(words.dataretrieval.getValence('computer'), 0.76485739)
        self.assertEqual(words.dataretrieval.getValence('response'), 0.77583958)    

    def testGetDocuments(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        #print(words.dataretrieval.getDocuments(startDate, endDate))
        startDate = date(2010, 11, 7)
        endDate = date(2015, 1, 31)
        #print(words.dataretrieval.getDocuments(startDate, endDate))
        
    def testGetDocumentData(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        for doc in words.dataretrieval.getDocumentData(startDate, endDate):
            #print(doc.article_id)
            pass
        #print()
        startDate = date(2010, 11, 7)
        endDate = date(2015, 1, 31)
        for doc in words.dataretrieval.getDocumentData(startDate, endDate):
            #print(doc.article_id)
            pass
        
    def testGetWordData(self):
        systemData = words.dataretrieval.getWordData('system')
        for wd in systemData:
            #print(wd.article_id, wd.word_count)
            pass
        
    def testGetWordsInDocument(self):
        wordsIn1 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=1))
        wordsIn4 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=4))
        wordsIn18 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=18))
        self.assertTrue('system' in wordsIn4)
        self.assertTrue('human' in wordsIn4)
        self.assertTrue('eps' in wordsIn4)
        self.assertTrue('human' in wordsIn1)
        self.assertTrue(wordsIn4.count('system') == 2)
        self.assertTrue(wordsIn4.count('human') == 1)
        self.assertTrue(wordsIn4.count('eps') == 1)
        self.assertTrue(wordsIn4.count('survey') == 0)
        self.assertTrue(wordsIn18.count('survey') == 1)
    
    def testGetNumWordsInCorpus(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        self.assertTrue(words.dataretrieval.getNumWordsInCorpus(docs) == 26)

    def testGetNumWordInCorpus(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        self.assertTrue(words.dataretrieval.getNumWordInCorpus(docs, 'system') == 4)       

    def testSplitDocuments(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        splitYear = words.dataretrieval.splitDocuments(docs, 'Year')
        for k,v in splitYear.items():
            #print('Year: ', k)
            for doc in v:
                #print(doc.article_id)
                pass
            #print()
            pass
        splitMonth = words.dataretrieval.splitDocuments(docs, 'Month')
        for k,v in splitMonth.items():
            #print('Y/M: ', k)
            for doc in v:
                #print(doc.article_id)
                pass
            #print()
            pass
        
class RequestHandlerTests(TestCase):
    
    def setUp(self):
        pass
       
    def testCosDistanceOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word1 = 'rabbit'
        word2 = 'bird'
        #doc = (Document_Data.objects.get(article_id=1))
        #print(doc.article_id, doc.publicationDate)
        #print(words.dataretrieval.getWordsInDocument(doc))
        request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2, False)
        result = request.execute()
        print('cos distance over time')
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)
        
    def testTfidfOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word = 'water'
        #doc = (Document_Data.objects.get(article_id=1))
        #print(doc.article_id, doc.publicationDate)
        #print(words.dataretrieval.getWordsInDocument(doc))
        request = words.requesthandler.TfidfOverTimeRequest(dateRange, granularity, word)
        result = request.execute()
        print('average tfidf over time')
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)        
        
    def testNClosestNeighboursOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word = 'rabbit'
        N = 2
        request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, word, N, True)
        result = request.execute()
        print('n closest neighbours over time')
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)
        
    def testAverageArousalOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        request = words.requesthandler.AverageArousalOverTimeRequest(dateRange, granularity)
        result = request.execute()
        print('average arousal over time')
        print(result.xValues)
        print(result.yValues)
        
    def testAverageValenceOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        request = words.requesthandler.AverageValenceOverTimeRequest(dateRange, granularity)
        result = request.execute()
        print('average valence over time')
        print(result.xValues)
        print(result.yValues)       

    def testAverageArousalTopFiveOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        request = words.requesthandler.AverageArousalFiveWordsOverTimeRequest(dateRange, granularity)
        result = request.execute()
        print('average arousal top five words over time')
        print(result.xValues)
        print(result.yValues) 

    def testAverageValenceTopFiveOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        request = words.requesthandler.AverageValenceFiveWordsOverTimeRequest(dateRange, granularity)
        result = request.execute()
        print('average valence top five words over time')
        print(result.xValues)
        print(result.yValues)
    
    def testPairwiseProbabilities(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        request = words.requesthandler.PairwiseProbabilitiesOverTimeRequest(dateRange, granularity, 'water', 'rabbit')
        result = request.execute()
        print('pairwise probabilities over time')
        for k,v in result.items():
            print(v.yTitle)
            print(v.xValues)
            print(v.yValues)
        
# will be implemented once there is a clearer way to test the analysis process. probably with help from client
class DataAnalyzerTests(TestCase):
    
    def setUp(self):
        pass
    
#class DataInputTests(TestCase):
    
    #def testDataInput(self):
        #words.databaseinput.run()
        