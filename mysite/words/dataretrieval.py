import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
import django
django.setup()
from models import Document, Word, WordInDocument

# query terms can be id, language, province, city, country, and date
# for now just query by date range
def getDocuments(startDate, endDate):
    docs = Document.objects.filter(publicationDate__lte='').filter(publicationDate__gte='')
    words = []
    for doc in docs:
        words.append(getWordsInDocument(doc))
    return (list(docs), words)

def getWordsInDocument(doc):
    words = WordInDocument.objects.filter(document__article_id=doc.article_id)
    return list(words)