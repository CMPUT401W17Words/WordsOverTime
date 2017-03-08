from datetime import date

from django.test import TestCase

import words.dataretrieval
import words.requesthandler
import words.databaseinput
from words.models import Document

# Create your tests here.

class DataRetrievalTests(TestCase):
    
    def setUp(self):
        self.docs = [Document(article_id=1, publicationDate=date(2010, 6, 7)),
                     Document(article_id=3, publicationDate=date(2008, 10, 11)),
                     Document(article_id=5, publicationDate=date(1990, 12, 17)),
                     Document(article_id=4, publicationDate=date(2000, 5, 19)),
                     Document(article_id=2, publicationDate=date(2007, 5, 19)),
                     Document(article_id=7, publicationDate=date(2010, 1, 17)),
                     Document(article_id=6, publicationDate=date(2008, 11, 1))]
        for doc in self.docs:
            doc.save()
        
    def testGetDocuments(self):
        startDate = date(2000, 5, 19)
        endDate = date(2008, 10, 11)
        docs = words.dataretrieval.getDocuments(startDate, endDate)[0]
        self.assertIs(len(docs)==3, True)
        for doc in docs:
            self.assertGreaterEqual(doc.publicationDate, startDate)
            self.assertLessEqual(doc.publicationDate, endDate)
    
    def testGetWordsInDocument(self):
        pass
    
    def testSplitDocuments(self):
        docs = words.dataretrieval.splitDocuments(self.docs, 'Year')
        for k,v in docs.items():
            if (k==2010 or k==2008):
                self.assertTrue(len(v)==2)
            else:
                self.assertTrue(len(v)==1)
    
class RequestHandlerTests(TestCase):
    
    def testCosDistanceOverTime(self):
        dateRange = (date(2000, 5, 19), date(2008, 10, 11))
        granularity = 'Year'
        word1 = 'pumpkin'
        word2 = 'bird'
        request = words.requesthandler.CosDistanceOverTimeRequest(dateRange, granularity, word1, word2)
        result = request.execute()
        
        