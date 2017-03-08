import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
import django
django.setup()
from words.models import Document, Word, WordInDocument

# query terms can be id, language, province, city, country, and date
# for now just query by date range
def getDocuments(startDate, endDate):
    docs = Document.objects.filter(publicationDate__lte=endDate).filter(publicationDate__gte=startDate)
    words = []
    for doc in docs:
        words.append(getWordsInDocument(doc))
    return (list(docs), words)

def getWordsInDocument(doc):
    words = WordInDocument.objects.filter(document__article_id=doc.article_id)
    result = []
    for w in words:
        result.append(w.word.word)
    return result

# split a list of documents into sublists based on a specified time granularity        
def splitDocuments(documents, granularity):
    result = {} # keys are time bins, values are lists of documents falling into that bin
    if (granularity == 'Year'):
        for doc in documents:
            year = doc.publicationDate.year
            if year not in result:
                result[year] = []
            result[year].append(doc)    
    if (granularity == 'Month'):
        for doc in documents:
            month = (doc.publicationDate.year, doc.publicationDate.month)
            if month not in result:
                result[month] = []
            result[month].append(doc)
    return result