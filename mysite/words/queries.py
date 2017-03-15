from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.db import models
from .models import SentimentDictionary, ArticlesCan, DocumentData, WordData, CorpusData

def splitByLocationNoWord(givenProv = None, givenCity = None, givenCountry = None):
    #results = DocumentData.objects
    # I think it needs to be the articles we search due to DocumentData not having all the word data, so
    results = ArticlesCan.objects
    if(givenProv is not None):
        results.filter(province=givenProv)
    if(givenCity is not None):
        results.filter(city=givenCity)
    if(givenCountry is not None):
        results.filter(country=givenCountry)
    return results

def splitByLocationOneWord(word, givenProv = None, givenCity = None, givenCountry = None):
    results = ArticlesCan.objects
    if(givenProv is not None):
        results.filter(province=givenProv)
    if(givenCity is not None):
        results.filter(city=givenCity)
    if(givenCountry is not None):
        results.filter(country=givenCountry)
    results.filter(parsed_article__contains=word)
    return results

def splitByLocationMultipleWords(words, givenProv = None, givenCity = None, givenCountry = None):
    results = ArticlesCan.objects
    if(givenProv is not None):
        results.filter(province=givenProv)
    if(givenCity is not None):
        results.filter(city=givenCity)
    if(givenCountry is not None):
        results.filter(country=givenCountry)
    for word in words:
        results.filter(parsed_article__contains=word)
    return results

def splitByTimeNoWord(time1, time2):
    return ArticlesCan.objects.filter(publication_date__range=[time1, time2])

def splitByTimeNoWordTextOnly(time1, time2):
    result = ArticlesCan.objects.filter(publication_date__range=[time1, time2]).values("parsed_article")
    return result.split()

def splitByTimeOneWord(word, time1, time2):
    return ArticlesCan.objects.filter(publication_date__range=[time1, time2]).filter(parsed_article__contains=word)

def splitByTimeOneWordTextOnly(word, time1, time2):
    result = ArticlesCan.objects.filter(publication_date__range=[time1, time2]).filter(parsed_article__contains=word).values("parsed_article")
    return result.split()

def splitByTimeMultipleWords(words, time1, time2):
    selection = ArticlesCan.objects.filter(publication_date__range=[time1, time2])
    for word in words:
        selection.filter(parsed_article__contains=word)
    return selection

def splitByTimeMultipleWordsTextOnly(words, time1, time2):
    selection = ArticlesCan.objects.filter(publication_date__range=[time1, time2])
    for word in words:
        selection.filter(parsed_article__contains=word)
    text = selection.values("parsed_article")
    return text.split()

# Easier just to get article IDs then get valence/arousal from that
def getArticleIDsForGivenWord(word):
    return ArticlesCan.objects.filter(parsed_article__contains=word).values("articleID")

def getValence(docId):
    return DocumentData.objects.get(articleID=docId).values("average_valence_doc")

def getArousal(docId):
    return DocumentData.objects.get(articleID=docId).values("average_arousal_doc")

def getTop5Valence(docId):
    return DocumentData.objects.get(articleID=docId).values("average_valence_words")

def getTop5Arousal(docId):
    return DocumentData.objects.get(articleID=docId).values("average_arousal_words")

# Note that there can be multiple instances of the word in wordData
def getWordData(givenWord):
    return WordData.objects.filter(word = givenWord)

# Still unsure of how this works.
def getSimilarWords(word):
    return None

def getWordFrequency(word, time1=None, time2=None, givenProv = None, givenCity = None, givenCountry = None):
    if(time1 is not None or time2 is not None):
        result1 = self.splitByTimeOneWord(word, time1, time2)
        result2 = self.splitByTimeNoWord(time1, time2)
        return result1/result2
    elif(givenProv is not None or givenCity is not None or givenCountry is not None):
        result1 = self.splitByLocationOneWord(word, givenProv, givenCity, givenCountry)
        result2 = self.splitByLocationNoWord(givenProv, givenCity, givenCountry)
        return result1/result2
    else:
        return None

# These 3 below should be implemented eventually.
def getTFIDF(word):
    return None

def getRelativeWordFrequency(word):
    return None

def getPairwiseWords(word):
    return None