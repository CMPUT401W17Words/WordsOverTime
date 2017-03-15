import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
import django
django.setup()
from words.models import Document_Data, Word_Data

# query terms can be id, language, province, city, country, and date
# for now just query by date range
def getDocuments(startDate, endDate):
    docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    words = []
    for doc in docs:
        words.append(getWordsInDocument(doc))
    return  words

def getDocumentData(startDate, endDate):
    docs = Document_Data.objects.filter(publication_Date__lte=endDate).filter(publication_Date__gte=startDate)
    return (list(docs))

# returns all words in a document
def getWordsInDocument(doc):
    words = Word_Data.objects.filter(article_id=doc.article_id)
    result = []
    for w in words:
        for i in range(w.word_count):
            result.append(w.word)
    return result

# split a list of documents into sublists based on a specified time granularity        
def splitDocuments(documents, granularity):
    result = {} # keys are time bins, values are lists of documents falling into that bin
    if (granularity == 'Year'):
        for doc in documents:
            year = doc.publication_Date.year
            if year not in result:
                result[year] = []
            result[year].append(doc)    
    if (granularity == 'Month'):
        for doc in documents:
            month = (doc.publication_Date.year, doc.publication_Date.month)
            if month not in result:
                result[month] = []
            result[month].append(doc)
    return result