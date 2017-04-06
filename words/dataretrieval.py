#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#import sys
#sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
#import django
#django.setup()
from words.models import Document_Data, Word_Data, Sentiment_Dict
from datetime import date
from django.core.exceptions import ObjectDoesNotExist

def getArousal(wd):
    try:
        return float(Sentiment_Dict.objects.get(word=wd).arousal)
    except ObjectDoesNotExist:
        return None
   
def getValence(wd):
    try:
        return float(Sentiment_Dict.objects.get(word=wd).valence)
    except ObjectDoesNotExist:
        return None
    
# query terms can be id, language, province, city, country, and date
# for now just query by date range
def getDocuments(startDate, endDate):
    #docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    docs = Document_Data.objects.filter(publication_Date__range=(startDate, endDate))
    words = []
    for doc in docs:
        words.append(getWordsInDocument(doc))
    return words

def getDocumentData(startDate, endDate):
    #docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    docs = Document_Data.objects.filter(publication_Date__range=(startDate, endDate))
    return (list(docs))

def getDocumentDataWithWordFilter(startDate, endDate, wordList):
    if (len(wordList)<1):
        return getDocumentData(startDate, endDate)
    else:
        docs = Document_Data.objects.filter(publication_Date__range=(startDate, endDate)) # all documents in date range
        articleIds = docs.values_list('article_id', flat=True) # list of article ids for all documents
        for wd in wordList:
            filteredArticleIds = []
            idFilter = Word_Data.objects.filter(word=wd).values_list('article_id', flat=True)
            for x in articleIds:
                if x in idFilter:
                    filteredArticleIds.append(x)
            articleIds = filteredArticleIds
        docs = docs.filter(article_id__in=articleIds) # filter docs by articles that contain the words
        return (list(docs))

# return all word data objects for a word (each word data will be a different doc with the same word)
def getWordData(wordIn):
    words = Word_Data.objects.filter(word=wordIn)
    return (list(words))

# returns all words in a document
def getWordsInDocument(doc):
    words = Word_Data.objects.filter(article_id=doc.article_id)
    result = []
    for w in words:
        for i in range(w.word_count):
            result.append(w.word)
    return result

def getNumWordsInCorpus(documents):
    total = 0
    for doc in documents:
        words = Word_Data.objects.filter(article_id=doc.article_id)
        for word in words:
            total = total + word.word_count
    return total
           
def getNumWordInCorpus(documents, inputWord):
    total = 0
    for doc in documents:
        words = Word_Data.objects.filter(article_id=doc.article_id, word=inputWord)
        for word in words:
            total = total + word.word_count
    return total

def splitDocuments(documents, granularity):
    result = {} # keys are time bins, values are lists of documents falling into that bin
    if (granularity == 'Year'):
        for doc in documents:
            #year = doc.publication_Date.year
            year = date(doc.publication_Date.year,1,1)
            if year not in result:
                result[year] = []
            result[year].append(doc)    
    if (granularity == 'Month'):
        for doc in documents:
            #month = (doc.publication_Date.year, doc.publication_Date.month)
            month = date(doc.publication_Date.year, doc.publication_Date.month, 1)
            if month not in result:
                result[month] = []
            result[month].append(doc)
    if (granularity == 'Week'):
        for doc in documents:
            if (doc.publication_Date.day / 7 <= 1):
                day = 1
            elif (doc.publication_Date.day / 7 <= 2):
                day = 8
            elif (doc.publication_Date.day / 7 <= 2):
                day = 15
            else:
                day = 22
            week = date(doc.publication_Date.year, doc.publication_Date.month, day)
            if week not in result:
                result[week] = []
            result[week].append(doc)
    return result
