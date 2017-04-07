from datetime import date

from django.test import TestCase
#from unittest import TestCase

import words.dataretrieval
import words.requesthandler
import words.databaseinput
from words.emailsending import *
from words.models import Document_Data, Word_Data, Sentiment_Dict, Articles_Can
import csv
import decimal
from datetime import date
# Create your tests here.
import gensim

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.sentDict = []
        self.artCan = []
        self.docData = []
        self.wordData = []

        with open(r'words/sentiment_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
            file = csv.DictReader(csvfile)
            for line in file:
                self.sentDict.append(Sentiment_Dict(word=line['Word'], valence=line['Valence'],arousal=line['Arousal'],dominance=0.0,concreteness=0.0,aoa=0.0))
        
        for item in self.sentDict:
            item.save()        
                
        with open(r'words/corpus_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
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
        self.assertEqual(words.dataretrieval.getArousal('kitten'), None)
    
    def testGetValence(self):
        self.assertEqual(words.dataretrieval.getValence('minors'), 0.42352934)
        self.assertEqual(words.dataretrieval.getValence('computer'), 0.76485739)
        self.assertEqual(words.dataretrieval.getValence('response'), 0.77583958)
        self.assertEqual(words.dataretrieval.getArousal('kitten'), None)

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
        
    def testGetDocumentDataWithWordFilter(self):
        startDate = date(2008,2,17)
        endDate = date(2011,11,7)
        docs = words.dataretrieval.getDocumentDataWithWordFilter(startDate, endDate, ['interface'])
        ids = []
        for item in docs:
            ids.append(item.article_id)
        self.assertTrue(10 in ids and 4 not in ids)
        self.assertTrue(9 not in ids and 31 in ids)
        
    def testGetWordData(self):
        systemData = words.dataretrieval.getWordData('system')
        for wd in systemData:
            #print(wd.article_id, wd.word_count)
            pass
        
    def testGetWordsInDocument(self):
        wordsIn1 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=1))
        wordsIn4 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=4))
        wordsIn145 = words.dataretrieval.getWordsInDocument(Document_Data.objects.get(article_id=145))
        self.assertTrue('system' in wordsIn4)
        self.assertTrue('human' in wordsIn4)
        self.assertTrue('eps' in wordsIn4)
        self.assertTrue('human' in wordsIn1)
        self.assertTrue(wordsIn4.count('system') == 5)
        self.assertTrue(wordsIn4.count('human') == 1)
        self.assertTrue(wordsIn4.count('eps') == 1)
        self.assertTrue(wordsIn4.count('survey') == 0)
        self.assertTrue(wordsIn145.count('computer') == 1)
    
    def testGetNumWordsInCorpus(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        self.assertTrue(words.dataretrieval.getNumWordsInCorpus(docs) == 67)

    def testGetNumWordInCorpus(self):
        startDate = date(2008, 2, 17)
        endDate = date(2011, 11, 7)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        self.assertTrue(words.dataretrieval.getNumWordInCorpus(docs, 'system') == 26)       

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
        self.sentDict = []
        self.artCan = []
        self.docData = []
        self.wordData = []
        
        with open(r'words/sentiment_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
            file = csv.DictReader(csvfile)
            for line in file:
                self.sentDict.append(Sentiment_Dict(word=line['Word'], valence=line['Valence'],arousal=line['Arousal'],dominance=0.0,concreteness=0.0,aoa=0.0))
        
        for item in self.sentDict:
            item.save()        
                
        with open(r'words/corpus_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
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
    
    # working
    def testCosDistanceOverTime(self):
        dateRange = (date(2008, 2, 17), date(2010, 11, 11))
        granularity = 'Year'
        request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, [('human', 'system')], False, 'test1')
        result = request.execute()
        print('Cos Distance over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v)
        print("Errors: " + str(result.errors))
        print()
    
    # working
    def testTfidfOverTime(self):
        dateRange = (date(2008, 2, 17), date(2011, 11, 11))
        granularity = 'Year'
        request = words.requesthandler.TfidfOverTimeRequest(dateRange, granularity, ['human'], 'test2')
        result = request.execute()
        print('Average Tfidf over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v)
        print("Errors: " + str(result.errors))
        print()
        
    # working
    def testNClosestNeighboursOverTime(self):
        dateRange = (date(2008, 2, 17), date(2010, 11, 11))
        granularity = 'Year'
        request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, ['human', 'system', 'interface'], 2, True, 'test3')
        result = request.execute()
        print('N Closest Neighbours over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v)
        print("Errors: " + str(result.errors))
        print()
        
    # working   
    def testAverageArousalOverTime(self):
        dateRange = (date(2008, 1, 1), date(2012, 12, 31))
        granularity = 'Year'
        request = words.requesthandler.AverageArousalOverTimeRequest(dateRange, granularity, ['human', 'system'], 'test4')
        result = request.execute()
        print('Average Arousal over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(v)
        print("Errors: " + str(result.errors))
        print()            
        
    # working    
    def testAverageValenceOverTime(self):
        dateRange = (date(2008, 1, 1), date(2011, 12, 31))
        granularity = 'Year'
        request = words.requesthandler.AverageValenceOverTimeRequest(dateRange, granularity, ['user'], 'test5')
        result = request.execute()
        print('Average Valence over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(v)       
        print("Errors: " + str(result.errors))
        print()
                
    # working
    def testAverageArousalTopFiveOverTime(self):
        dateRange = (date(2013, 1, 1), date(2013, 12, 31))
        granularity = 'Month'
        request = words.requesthandler.AverageArousalFiveWordsOverTimeRequest(dateRange, granularity, ['trees'], 'test6')
        result = request.execute()
        print('Average Arousal Top Five Words over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(v)  
        print("Errors: " + str(result.errors))
        print()
        
    # working
    def testAverageValenceTopFiveOverTime(self):
        dateRange = (date(2008, 2, 17), date(2011, 11, 11))
        granularity = 'Year'
        request = words.requesthandler.AverageValenceFiveWordsOverTimeRequest(dateRange, granularity, [], 'test7')
        result = request.execute()
        print('Average Valence Top Five Words over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(v)
        print("Errors: " + str(result.errors))
        print()            
    
    # working    
    def testPairwiseProbabilities(self):
        dateRange = (date(2008, 2, 17), date(2010, 12, 31))
        granularity = 'Year'
        request = words.requesthandler.PairwiseProbabilitiesOverTimeRequest(dateRange, granularity, [('human', 'user')] , 'test8')
        result = request.execute()
        print('Pairwise Probabilities over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v) 
        print("Errors: " + str(result.errors))
        print()
    
    # working
    def testWordFrequency(self):
        dateRange = (date(2008, 1, 1), date(2010, 12, 31))
        granularity = 'Year'
        request = words.requesthandler.WordFrequencyOverTimeRequest(dateRange, granularity, ['human'], 'test9')
        result = request.execute()
        #result.generateCSV('test9')
        print('Word Frequency over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v)
        print("Errors: " + str(result.errors))
        print()
    
    # working
    def testRelativeWordFrequency(self):
        dateRange = (date(2013, 1, 1), date(2013, 12, 31))
        granularity = 'Month'
        request = words.requesthandler.RelativeWordFrequencyOverTimeRequest(dateRange, granularity, ['human', 'tomato'], 'test10')
        result = request.execute()
        print('Relative Word Frequency over time')
        print(result.xTitle, result.xValues)
        for k,v in result.yValues.items():
            print(k, v)        
        print("Errors: " + str(result.errors))
        print()
    
    # django does not support testing this concurrently, but it does seem to work    
    def testRequestsExecuteThread(self):
        reqs = []
        dateRange = (date(2008, 2, 17), date(2010, 12, 31))
        granularity = 'Year'
        request = words.requesthandler.PairwiseProbabilitiesOverTimeRequest(dateRange, granularity, [('human', 'user')] , 'test11')
        reqs.append(request)
        dateRange = (date(2008, 2, 17), date(2010, 11, 11))
        request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, ['human', 'system', 'interface'], 2, True, 'test12')
        reqs.append(request)       
        ret = words.requesthandler.RequestsExecuteThread(reqs, r'tommy3@ualberta.ca')
        ret.run()
    
# will be implemented once there is a clearer way to test the analysis process. probably with help from client
class DataAnalyzerTests(TestCase):
    
    def setUp(self):
        self.sentDict = []
        self.artCan = []
        self.docData = []
        self.wordData = []
        
        with open(r'words/sentiment_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
            file = csv.DictReader(csvfile)
            for line in file:
                self.sentDict.append(Sentiment_Dict(word=line['Word'], valence=line['Valence'],arousal=line['Arousal'],dominance=0.0,concreteness=0.0,aoa=0.0))
        
        for item in self.sentDict:
            item.save()        
                
        with open(r'words/corpus_mock.csv', 'r') as csvfile: # iterate over docs in the CSV file
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
                
    def testSaveMatrix(self):
        pass
    
#class DataInputTests(TestCase):
 
    #def testenterSentiment(self):
        #words.databaseinput.enterSentiment('words/sentiment_mock.csv')
        #result = sentiment_dict.objects.all()
        #print('Sentiment_Mock in database:')
        #for v in result:
            #print(v)
            
    #def testCorpusInput(self):
        #words.databaseinput.enterArticles('words/corpus_mock.csv')
        #result = articles_can.objects.all()
        #print('corpus_Mock in database:')
        #for v in result:
            #print(v)  
            
    #def testDataInput(self):
        #words.databaseinput.run('words/sentiment_mock.csv', 'words/corpus_mock.csv')
        #pass
        
