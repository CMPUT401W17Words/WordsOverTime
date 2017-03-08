from datetime import date

from django.test import TestCase

import words.dataretrieval
import words.requesthandler
import words.databaseinput
from words.models import Document, Word, WordInDocument

# Create your tests here.

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.doc1 = Document(article_id=1, publicationDate=date(2010, 6, 7))
        self.doc2 = Document(article_id=2, publicationDate=date(2007, 5, 19))
        self.docs = [self.doc1,
                     Document(article_id=3, publicationDate=date(2008, 10, 11)),
                     Document(article_id=5, publicationDate=date(1990, 12, 17)),
                     Document(article_id=4, publicationDate=date(2000, 5, 19)),
                     self.doc2,
                     Document(article_id=7, publicationDate=date(2010, 1, 17)),
                     Document(article_id=6, publicationDate=date(2008, 11, 1))]
        word1 = Word(word='rabbit')
        word2 = Word(word='bird')
        self.words = [word1, word2]
        for doc in self.docs:
            doc.save()
        for word in self.words:
            word.save()
        self.wordInDocs = [WordInDocument(word=word1, document=self.doc1),
                           WordInDocument(word=word2, document=self.doc1),
                           WordInDocument(word=word2, document=self.doc2)]
        for wid in self.wordInDocs:
            wid.save()
        
    def testGetDocuments(self):
        startDate = date(2000, 5, 19)
        endDate = date(2008, 10, 11)
        docs = words.dataretrieval.getDocuments(startDate, endDate)[0]
        self.assertIs(len(docs)==3, True)
        for doc in docs:
            self.assertGreaterEqual(doc.publicationDate, startDate)
            self.assertLessEqual(doc.publicationDate, endDate)
    
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
        #words.databaseinput.run()
        self.doc1 = Document(article_id=1, publicationDate=date(2010, 6, 7))
        self.doc2 = Document(article_id=2, publicationDate=date(2007, 5, 19))
        self.doc3 = Document(article_id=3, publicationDate=date(2008, 10, 11))
        self.doc4 = Document(article_id=4, publicationDate=date(2000, 5, 19))
        self.docs = [self.doc1,
                     self.doc3,
                     Document(article_id=5, publicationDate=date(1990, 12, 17)),
                     self.doc4,
                     self.doc2,
                     Document(article_id=7, publicationDate=date(2010, 1, 17)),
                     Document(article_id=6, publicationDate=date(2008, 11, 1))]
        word1 = Word(word='rabbit')
        word2 = Word(word='bird')
        self.words = [word1, word2]
        for doc in self.docs:
            doc.save()
        for word in self.words:
            word.save()
        self.wordInDocs = [WordInDocument(word=word1, document=self.doc1),
                           WordInDocument(word=word2, document=self.doc1),
                           WordInDocument(word=word1, document=self.doc2),
                           WordInDocument(word=word1, document=self.doc4),
                           WordInDocument(word=word2, document=self.doc4),
                           WordInDocument(word=word1, document=self.doc3)]
        for wid in self.wordInDocs:
            wid.save()
       
    def testCosDistanceOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word1 = 'rabbit'
        word2 = 'bird'
        doc = (Document.objects.get(article_id=1))
        #print(doc.article_id, doc.publicationDate)
        #print(words.dataretrieval.getWordsInDocument(doc))
        request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word1)
        result = request.execute()
        print(result.xValues)
        print(result.yValues)
        
        