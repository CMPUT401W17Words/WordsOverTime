from datetime import date

from django.test import TestCase

import words.dataretrieval
import words.requesthandler
import words.databaseinput
from words.models import Document_Data, Word_Data

# Create your tests here.

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.doc1 = Document_Data(article_id=1, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 6, 7), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc2 = Document_Data(article_id=2, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.docs = [self.doc1,
                     Document_Data(article_id=3, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 10, 11), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     Document_Data(article_id=5, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(1990, 12, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     Document_Data(article_id=4, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     self.doc2,
                     Document_Data(article_id=7, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 1, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     Document_Data(article_id=6, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 11, 1), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)]
        word1 ='rabbit'
        word2 ='bird'
        self.words = [word1, word2]
        for doc in self.docs:
            doc.save()
        #for word in self.words:
            #word.save()
        self.wordInDocs = [Word_Data(word=word1, article_id=self.doc1.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc1.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc2.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0)]
        for wid in self.wordInDocs:
            wid.save()
        
    def testGetDocuments(self):
        startDate = date(2000, 5, 19)
        endDate = date(2008, 10, 11) 
        docs = words.dataretrieval.getDocuments(startDate, endDate)
        self.assertIs(len(docs)==3, True)
        #for doc in docs:
            #print(doc)
        
    def testGetDocumentData(self):
        startDate = date(2000, 5, 19)
        endDate = date(2008, 10, 11)
        docs = words.dataretrieval.getDocumentData(startDate, endDate)
        self.assertIs(len(docs)==3, True)
        for doc in docs:
            self.assertGreaterEqual(doc.publication_Date, startDate)
            self.assertLessEqual(doc.publication_Date, endDate)
    
    def testGetWordsInDocument(self):
        wds = words.dataretrieval.getWordsInDocument(self.doc2)
        self.assertTrue('bird' in wds)
        self.assertFalse('rabbit' in wds)
    
    def testSplitDocuments(self):
        docs = words.dataretrieval.splitDocuments(self.docs, 'Year')
        for k,v in docs.items():
            if (k==2010 or k==2008):
                self.assertTrue(len(v)==2)
            else:
                self.assertTrue(len(v)==1)
    
class RequestHandlerTests(TestCase):
    
    def setUp(self):
        self.csvFilePath = 'outputDump.csv'
        self.doc1 = Document_Data(article_id=1, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 6, 7), word_count = 4, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc2 = Document_Data(article_id=2, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 5, 19), word_count = 10, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc3 = Document_Data(article_id=3, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 10, 11), word_count = 8, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc4 = Document_Data(article_id=4, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 19), word_count = 2, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc8 = Document_Data(article_id=8, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 21), word_count = 13, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.doc9 = Document_Data(article_id=9, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 7, 11), word_count = 8, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0)
        self.docs = [self.doc1,
                     self.doc3,
                     Document_Data(article_id=5, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(1990, 12, 17), word_count = 0, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     self.doc4,
                     self.doc2,
                     Document_Data(article_id=7, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 1, 17), word_count = 0, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     Document_Data(article_id=6, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 11, 1), word_count = 0, average_arousal_doc = 1.0, average_valence_doc = 1.0, average_arousal_words = 1.0, average_valence_words = 1.0),
                     self.doc8,
                     self.doc9]
        word1 = 'rabbit'
        word2 = 'bird'
        word3 = 'water'
        for doc in self.docs:
            doc.save()
        self.wordInDocs = [Word_Data(word=word1, article_id=self.doc1.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word3, article_id=self.doc2.article_id, word_count = 2, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc1.article_id, word_count = 3, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word1, article_id=self.doc2.article_id, word_count = 7, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc2.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word1, article_id=self.doc4.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc4.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word1, article_id=self.doc3.article_id, word_count = 2, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc3.article_id, word_count = 4, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word3, article_id=self.doc3.article_id, word_count = 2, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word1, article_id=self.doc8.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc8.article_id, word_count = 1, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word3, article_id=self.doc8.article_id, word_count = 11, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word1, article_id=self.doc9.article_id, word_count = 4, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word3, article_id=self.doc9.article_id, word_count = 2, term_frequency =1.0, tfidf = 1.0),
                           Word_Data(word=word2, article_id=self.doc9.article_id, word_count = 2, term_frequency =1.0, tfidf = 1.0)]
        for wid in self.wordInDocs:
            wid.save()
            
    #def testDatabaseEntry(self):
        #print(len(Document_Data.objects.all()))
        #print(len(Word_Data.objects.all()))
       
    def testCosDistanceOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word1 = 'rabbit'
        word2 = 'bird'
        doc = (Document_Data.objects.get(article_id=1))
        #print(doc.article_id, doc.publicationDate)
        #print(words.dataretrieval.getWordsInDocument(doc))
        request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2)
        result = request.execute()
        print('cos distance over time')
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)
        
    def testNClosestNeighboursOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word = 'rabbit'
        N = 2
        request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, word, N)
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
        
# will be implemented once there is a clearer way to test the analysis process. probably with help from client
class DataAnalyzerTests(TestCase):
    
    def setUp(self):
        pass