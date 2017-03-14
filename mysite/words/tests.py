from datetime import date

from django.test import TestCase

import words.dataretrieval
import words.requesthandler
import words.databaseinput
from words.models import Document_Data, Word_Data

# Create your tests here.

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.doc1 = Document_Data(article_id=1, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 6, 7), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc2 = Document_Data(article_id=2, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.docs = [self.doc1,
                     Document_Data(article_id=3, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 10, 11), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     Document_Data(article_id=5, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(1990, 12, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     Document_Data(article_id=4, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     self.doc2,
                     Document_Data(article_id=7, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 1, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     Document_Data(article_id=6, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 11, 1), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)]
        word1 = Word_Data(word='rabbit')
        word2 = Word_Data(word='bird')
        self.words = [word1, word2]
        for doc in self.docs:
            doc.save()
        for word in self.words:
            word.save()
        self.wordInDocs = [Word_Data(word=word1, document=self.doc1, word_count = 1),
                           Word_Data(word=word2, document=self.doc1, word_count = 1),
                           Word_Data(word=word2, document=self.doc2, word_count = 1)]
        for wid in self.wordInDocs:
            wid.save()
        
    def testGetDocuments(self):
        startDate = date(2000, 5, 19)
        endDate = date(2008, 10, 11)
        docs = words.dataretrieval.getDocuments(startDate, endDate)[0]
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
        #words.databaseinput.run()
        self.doc1 = Document_Data(article_id=1, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 6, 7), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc2 = Document_Data(article_id=2, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc3 = Document_Data(article_id=3, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 10, 11), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc4 = Document_Data(article_id=4, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 19), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc8 = Document_Data(article_id=8, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2000, 5, 21), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.doc9 = Document_Data(article_id=9, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2007, 7, 11), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0)
        self.docs = [self.doc1,
                     self.doc3,
                     Document_Data(article_id=5, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(1990, 12, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     self.doc4,
                     self.doc2,
                     Document_Data(article_id=7, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2010, 1, 17), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     Document_Data(article_id=6, language = "english", province = "AB", city = "Edmonton", country = "CAN", publication_Date=date(2008, 11, 1), word_count = 1, average_arousal_doc = 1.0, average_valence_doc = 1.0),
                     self.doc8,
                     self.doc9]
        word1 = Word(word='rabbit')
        word2 = Word(word='bird')
        self.words = [word1, word2]
        for doc in self.docs:
            doc.save()
        #for word in self.words:
            #word.save()
        self.wordInDocs = [Word_Data(word=word1, document=self.doc1, word_count = 1,),
                           Word_Data(word=word2, document=self.doc1, word_count = 1,),
                           Word_Data(word=word1, document=self.doc2, word_count = 1,),
                           Word_Data(word=word1, document=self.doc4, word_count = 1,),
                           Word_Data(word=word2, document=self.doc4, word_count = 1,),
                           Word_Data(word=word1, document=self.doc3, word_count = 1,),
                           Word_Data(word=word2, document=self.doc3, word_count = 1,),                           
                           Word_Data(word=word2, document=self.doc8, word_count = 1,),
                           Word_Data(word=word2, document=self.doc9, word_count = 1,)]
        for wid in self.wordInDocs:
            wid.save()
            
    def testDatabaseEntry(self):
        print(len(Document_Data.objects.all()))
        #print(len(WordInDocument.objects.all()))
        print(len(Word_Data.objects.all()))
       
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
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)
        
    def testNClosestNeighboursOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word = 'rabbit'
        N = 1
        request = words.requesthandler.NClosestNeighboursOverTimeRequest(dateRange, granularity, word, N)
        result = request.execute()
        print(result.xValues)
        print(result.yValues)
        result.generateCSV(self.csvFilePath)
        
        