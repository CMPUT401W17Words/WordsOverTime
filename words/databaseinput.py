# This module inputs the corpus and sentiment CSV files into Django's built-in SQLite database
# It will not be the final method of database input
# It can be used for quick testing of the data processing modules
# Uses the first 1000 corpus entries and 10000 sentiment entries

# 
from __future__ import division
import io

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import math
import datetime
import csv 
import django
import gensim
import time
import dataretrieval

from collections import Counter
from decimal import *
from words.models import Sentiment_Dict, Document_Data, Word_Data
from django.db.models import F
from django.db import transaction
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append(r"C:\Users\L\Documents\School\WordsOverTime\mysite")
django.setup()

#load data local infile '/mnt/vol/sentiment_dict_3mil.csv' into table Generated_Data.words_sentiment_dict FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);
def enterSentiment(dictpath):
    
    cursor = django.db.connection.cursor()
    nr_records_inserted = cursor.execute("load data local infile '%s' into table Generated_Data.words_sentiment_dict FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES (Word, Valence, Arousal, Dominance, Concreteness, AoA);" % dictpath)

#load data local infile "/mnt/vol/articles-can.csv" into table Client_Generated_Data.articles_can FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES (articleID, language, province, city, country, publication_date, wordcount, parsed_article);

def enterArticles(corpuspath):
    cursor = django.db.connection.cursor()
    nr_records_inserted = cursor.execute("load data local infile '%s' into table Generated_Data.words_sentiment_dict FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 1 LINES (articleID, language, province, city, country, publication_date, wordcount, parsed_article);" % corpuspath)
    Articles_Can.objects.filter(publicationdate = None).delete()

# main function that will input corpus info into the database
def enterData(corpusCsv):
    transaction.set_autocommit(False)
    fullCorpus = MainCorpus(corpusCsv)
    maxInt = sys.maxsize
    decrement = True

    # We're sometimes dealing with very large inputs, so raise the max size allowed.
    while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
    print("Beginning document input")
    with open(corpusCsv, 'r') as csvfile: # iterate over docs in the CSV file
        file = csv.DictReader(csvfile)
        count = 0
        for line in file: # make sure the article is not already entered
            if Document_Data.objects.filter(article_id = line['articleID']).exists():
                continue
	    try:
                words = line['parsedArticle'].split()
                datte = line['publicationDate']
                datesplit = datte.split("-")
                dattte = datetime.datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]))
                arousal = Decimal('0.0')
                valence = Decimal('0.0')
                arousal_five = []
                valence_five = []
                tfidf_five =[]
                value = Decimal(0.0)
                doc_word_count = len(words)
                wordsindictcount = 0
                wordscounted = Counter(words)

                for eachword in wordscounted: # get sentiment info
                    wrdcnt = wordscounted[eachword]
                    termfreq = Decimal(math/log(wrdcnt/doc_word_count)).quantize(Decimal('0.000000000001'), rounding = ROUND_DOWN)
                    word = Word_Data(word=eachword, article_id=line['articleID'], word_count=wrdcnt, term_frequency=termfreq, tfidf=value)
                    word.save()
                    wordvalues = Sentiment_Dict.objects.filter(word=eachword)
                    if wordvalues:
                        wordsindictcount = wordsindictcount + 1
                        currentArousal = wordvalues.values_list("arousal", flat=True)
                        currentValence = wordvalues.values_list("valence", flat=True)
                        arousal = arousal + currentArousal[0]
                        valence = valence + currentValence[0]
                            
                arousal_average_five = 0.0
                valence_average_five = 0.0          

                doc = Document_Data(article_id = line['articleID'], language = line['language'], province = line['province'], 
                          city = line['city'], country = line['country'], publication_Date = dattte, 
                          word_count = doc_word_count, word_one = "", word_two = "", word_three = "", word_four = "", 
                          word_five = "", average_arousal_doc = arousal/wordsindictcount, average_valence_doc = valence/wordsindictcount,
                          average_arousal_words = arousal_average_five, average_valence_words = valence_average_five)  
                doc.save()

                count = count + 1
                if (count %20000==0): 
                    #print(count, " documents computed")
                    sys.stdout.flush()            
                    transaction.commit()
                    completedtime = time.asctime(time.localtime(time.time()))
                    print(count, " documents computed", completedtime)
                    sys.stdout.flush()

            except Exception as e:    
                print str(e)
        transaction.commit()
        print(count, "all documents computed")
        sys.stdout.flush()


def tfidfForFullCorpus():
    completedtime = time.asctime(time.localtime(time.time()))
    print "Starting tfidf calculations", completedtime
    chunk = Document_Data.objects.all()
    words = []
    completedtime = time.asctime(time.localtime(time.time()))
    print "Loading Chunk", completedtime
    count = 0
    for doc in chunk:
        try:
            words.append(dataretrieval.getWordsInDocument(doc))
        except (django.db.utils.OperationalError, django.db.utils.InterfaceError) as e:
            django.db.connection.close()
            words.append(dataretrieval.getWordsInDocument(doc))
        count = count + 1
        if (count%10000==0):
	    completedtime = time.asctime(time.localtime(time.time()))
            print count, " docs loaded into chunk", completedtime
    completedtime = time.asctime(time.localtime(time.time()))
    print "Built list of words", completedtime
    #wordData = Word_Data.objects.all()
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidffull = gensim.models.TfidfModel(corpus)
    completedtime = time.asctime(time.localtime(time.time()))
    print "Calculated TFIDF", completedtime
    #for word in wordData:
        #wordId = dictionary.token2id[word.word]
    count = 0
    transaction.set_autocommit(False)
    for doc,datadoc in zip(corpus, chunk):
        print "doc ", doc
        print "tfidf doc ", tfidf[doc]
        try:
            wordData = Word_Data.objects.filter(article_id = datadoc.article_id)
        except (django.db.utils.OperationalError, django.db.utils.InterfaceError) as e:
            django.db.connection.close()
            wordData = Word_Data.objects.filter(article_id = datadoc.article_id)
        print "wordd", wordData
        #articleId = datadoc.article_id

        for wordd in wordData:
            wordId = dictionary.token2id[wordd.word]
            #print "wordd", wordd    
            for item in tfidffull[doc]:
                if (item[0] == wordId):
                    tfidfvalue = item[1]
                    count = count + 1
                    break
            wordd.tfidf = tfidfvalue
            prelogtf = wordd.term_frequency
            prelogtf = log(prelogtf)
            wordd.term_frequency = Decimal(prelogtf).quantize(Decimal('0.000000000001'), rounding = ROUND_DOWN)
            wordd.save(['tfidf','term_frequency'])
            if (count %10000==0):
                completedtime = time.asctime(time.localtime(time.time()))
                print count, " words updated ", completedtime
                try:
                    transaction.commit()
                except (django.db.utils.OperationalError, django.db.utils.InterfaceError) as e:
                    django.db.connection.close()
                    transaction.commit()
            if (count > 0):
                break
    try:
        transaction.commit()
    except (django.db.utils.OperationalError, django.db.utils.InterfaceError) as e:
        django.db.connection.close()
        transaction.commit()

    completedtime = time.asctime(time.localtime(time.time()))
    print "all words updated ", completedtime

# generate corpus from file path   
class MainCorpus(gensim.corpora.textcorpus.TextCorpus):
    def __init__(self, path):
        gensim.corpora.textcorpus.TextCorpus.__init__(self)
        self.file_path = path
    def get_texts(self):
        with open(self.file_path, 'r') as csvfile:
            file = csv.DictReader(csvfile)
            count = 0
            for line in file:
                words = []
                #print(line["parsedArticle"])
                for word in line["parsedArticle"].split():
                    words.append(word)
                yield words
                count = count + 1
                if (count > 1000):
                    break
    
# load sentiment dictionary from file path                
def loadSentiment(sentimentCsv):
    sentDict = {}
    csv.field_size_limit(sys.maxsize)
    with io.open(sentimentCsv, 'r', encoding="utf8") as csvfile:
        file = csv.DictReader(csvfile)
        count = 0
        for line in file:
            try:
                sentDict[line['Word']] = (float(line['Valence']), float(line['Arousal']))
            except ValueError:
                pass
                #print(line)
            count = count + 1
            #if (count %100==0): 
                #print(count)
                #sys.stdout.flush()
            #if (count > 1000):
                #break 
        print(count, " word dictionary loaded")
        sys.stdout.flush()                
    return sentDict

def run(sentPath, corpusPath):
    print("Creating database from ", sentPath, " and ", corpusPath)
    enterSentiment(sentPath)
    enterArticles(corpusPath)
    enterData(corpusPath)
    tfidfForFullCorpus()
    
if __name__ == "__main__":
    run()
