import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
import django
django.setup()
from models import Document

# return a list of documents matching the query
# query terms can be id, language, province, city, country, and date
# for now just query by date range
def getDocuments(startDate, endDate):
    querySet = Document.objects.filter(publicationDate__lte='').filter(publicationDate__gte='')
    return list(querySet)