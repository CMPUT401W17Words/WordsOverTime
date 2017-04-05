import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
import django
django.setup()
from words.models import Document_Data, Word_Data, Sentiment_Dict
from datetime import date

"""
Returns arousal of a word
"""
def getArousal(wd):
    return float(Sentiment_Dict.objects.get(word=wd).arousal)

"""
Returns valence of a word
"""    
def getValence(wd):
    return float(Sentiment_Dict.objects.get(word=wd).valence)
    
# query terms can be id, language, province, city, country, and date
# for now just query by date range
"""
Returns documents falling within the date range, inclusive
Returns a nested list of documents where each document is a list of words
"""
def getDocuments(startDate, endDate):
    #docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    docs = Document_Data.objects.filter(publication_Date__range=(startDate, endDate))
    words = []
    for doc in docs:
        words.append(getWordsInDocument(doc))
    return words

"""
Returns a list of Document_Data objects falling within the date range, inclusive
"""
def getDocumentData(startDate, endDate):
    #docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    docs = Document_Data.objects.filter(publication_Date__range=(startDate, endDate))
    return (list(docs))

"""
Variation of getDocumentData that selects only those documents which include all the words in the word list
"""
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
"""
Get all Word_Data objects for a word
"""
def getWordData(wordIn):
    words = Word_Data.objects.filter(word=wordIn)
    return (list(words))

# returns all words in a document
"""
Return the list of all words in a document, including repeats
"""
def getWordsInDocument(doc):
    words = Word_Data.objects.filter(article_id=doc.article_id)
    result = []
    for w in words:
        for i in range(w.word_count):
            result.append(w.word)
    return result

"""
Return word count in a selection of Document_Data objects
"""
def getNumWordsInCorpus(documents):
    total = 0
    for doc in documents:
        words = Word_Data.objects.filter(article_id=doc.article_id)
        for word in words:
            total = total + word.word_count
    return total

"""
Return word count of a specific word in a selection of Document_Data objects
"""            
def getNumWordInCorpus(documents, inputWord):
    total = 0
    for doc in documents:
        words = Word_Data.objects.filter(article_id=doc.article_id, word=inputWord)
        for word in words:
            total = total + word.word_count
    return total

"""
Split a list of documents into sublists based on a specified time granularity
Granularity can be 'Year' or 'Month'
Return object is a dictionary mapping time segments to documents falling into that time segment
"""
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
    return result
