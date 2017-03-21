# This module inputs the corpus and sentiment CSV files into Django's built-in SQLite database
# It will not be the final method of database input
# It can be used for quick testing of the data processing modules
# Uses the first 1000 corpus entries and 10000 sentiment entries

# 

import io

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import math

import csv 
import django
import gensim


from words.models import Sentiment_Dict, Document_Data, Word_Data
from django.db.models import F

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append(r"C:\Users\L\Documents\School\WordsOverTime\mysite")
django.setup()

corpusPath = r'C:\Users\L\Documents\School\CMPUT\401\articles-can\articles-can.csv'
sentimentPath = r'C:\Users\L\Documents\School\CMPUT\401\sentiment_dict_3mil\sentiment_dict_3mil.csv'

corpusPath3 = r'C:\Users\L\Documents\School\CMPUT\401\mock_corpus.csv'
sentimentPath3 = r'C:\Users\L\Documents\School\CMPUT\401\mock_sentiment.csv'

corpusPath2 = r'C:\Users\Master Chief\Documents\School\articles-can\articles-can.csv'
sentimentPath2 = r'C:\Users\Master Chief\Documents\School\sentiment_dict_3mil\sentiment_dict_3mil.csv'

corpusPath4 = r'/mnt/vol/articles-can.csv'
sentimentPath4 = r'/mnt/vol/sentiment_dict_3mil.csv'

def enterSentiment():
    pass

def enterArticles():
    pass

# main function that will input corpus and sentiment info into the database
def enterData(corpusCsv, sentimentCsv):
    #wordData = {} # represent models as dictionaries of primary key to list of other data
    #docData = {}
    #wordDocData = {}    
    
    fullCorpus = MainCorpus(corpusCsv)
    #for text in fullCorpus:
    #    print(text)
    #corpus = [gensim.corpora.Dictionary.doc2bow(text) for text in fullCorpus]
    #tfidf = gensim.models.tfidfmodel.TfidfModel(corpus)
    #sentDict = loadSentiment(sentimentCsv)
    print("Beginning document input")
    #print(len(fullCorpus.dictionary.token2id.keys()), 'unique word count')
    #for word in fullCorpus.dictionary.token2id.keys(): # get each word in the corpus
        #wordData[word] = []
        
    with open(corpusCsv, 'r') as csvfile: # iterate over docs in the CSV file
        file = csv.DictReader(csvfile)
        count = 0
        for line in file:
            #docData[line['articleID']] = []
            #docData[line['articleID']].append(line['language'])
            #docData[line['articleID']].append(line['province'])
            #docData[line['articleID']].append(line['city'])
            #docData[line['articleID']].append(line['country'])
            #docData[line['articleID']].append(line['publicationDate'])
            #docData[line['articleID']].append(line['wordCount'])
            words = line['parsedArticle'].split()
            #tfidfs = tfidf[fullCorpus.dictionary.doc2bow(words)]
            #print(tfidfs, 'TFIDFS')
            #print(len(tfidfs), 'TFIDFS')
            arousal = 0.0
            valence = 0.0
            arousal_five = []
            valence_five = []
            tfidf_five =[]
            #for item in tfidfs: # get each word in the doc and its tfidf
                #word = fullCorpus.dictionary[item[0]]
                #value = item[1]
                #print(word,value)
                #wordDocData[(word,line['articleID'])] = []
                #wordDocData[(word,line['articleID'])].append(value)
            value = 0
            doc_word_count = len(words)
            #print(doc_word_count)
            for word in words: # get sentiment info
                # TODO: log10 term frequency
                word, created = Word_Data.objects.get_or_create(word=word, article_id = line['articleID'], word_count = 1, term_frequency = (1/doc_word_count), tfidf = value)#, inverse_term_frequency = 0)
                if not created:
                    #wrd = Word_Data(word=word, article_id = line['articleID'], word_count = word.word_count + 1, term_frequency = ((word.word_count + 1)/doc_word_count), tfidf = value)#, inverse_term_frequency = 0)
                    #wrd.save()
                    Word_Data.objects.filter(word=word, article_id = line['articleID']).update(word_count = F('word_count')+1, term_frequency = (F('word_count')+1/doc_word_count))
                #if word in sentDict:
                    #currenttfidf = tfidfs [word][0]
                    #currentValence = sentDict[word][0]
                    #currentArousal = sentDict[word][1]
                wordvalues = Sentiment_Dict.objects.filter(word = word)
                if wordvalues:
                    currentArousal = wordvalues.values_list("arousal", flat=True)
                    currentValence = wordvalues.values_list("valence", flat=True)
                    arousal = arousal + currentArousal[0]
                    valence = valence + currentValence[0]
                    if (len(tfidf_five)<5):
                        tfidf_five.append([word,value,currentValence[0],currentArousal[0]])
                    else:
                        tfidf_five = sorted(tfidf_five, key=lambda entry: entry[1])
                        for i in range(5):
                            if (tfidf_five[i][1]<value):
                                tfidf_five[i] = [word, value]
                                break  
                            
                            
                    #if (len(arousal_five)<5):
                        #arousal_five.append(currentArousal)
                    #else:
                        ##arousal_five.sort()
                        #for i in range(5):
                            #if (arousal_five[i]<currentArousal):
                                #arousal_five[i] = currentArousal
                                #break                    
                    #if (len(valence_five)<5):
                        #valence_five.append(currentValence)
                    #else:
                        #valence_five.sort()
                        #for i in range(5):
                            #if (valence_five[i]<currentValence):
                                #valence_five[i] = currentValence
                                #break
            arousal_average_five = 0.0
            valence_average_five = 0.0
            #for i in range(len(tfidf_five)):
                #valence_average_five = valence_average_five + tfidf_five[i][2]
                #arousal_average_five = arousal_average_five + tfidf_five[i][3]
            #valence_average_five = valence_average_five/len(tfidf)
            #arousal_average_five = arousal_average_five/len(tfidf)
            while (len(tfidf_five)<5):
                tfidf_five.append(["",0,0,0])            
            #docData[line['articleID']].append(len(words))
            #docData[line['articleID']].append("")
            #docData[line['articleID']].append("")
            #docData[line['articleID']].append("")
            #docData[line['articleID']].append("")
            #docData[line['articleID']].append("")
            #docData[line['articleID']].append(arousal/len(words))
            #docData[line['articleID']].append(valence/len(words))
            #docData[line['articleID']].append(arousal_average_five)
            #docData[line['articleID']].append(valence_average_five)
            doc = Document_Data(article_id = line['articleID'], language = line['language'], province = line['province'], 
                          city = line['city'], country = line['country'], publication_Date = line['publicationDate'], 
                          word_count = doc_word_count, word_one = tfidf_five[0][0], word_two = tfidf_five[1][0], word_three = tfidf_five[2][0], word_four = tfidf_five[3][0], 
                          word_five = tfidf_five[4][0], average_arousal_doc = arousal/doc_word_count, average_valence_doc = valence/doc_word_count,
                          average_arousal_words = arousal_average_five, average_valence_words = valence_average_five)  
            doc.save()

            count = count + 1
            if (count %1000==0): 
                print(count, " documents computed")
                sys.stdout.flush()            
           # if (count > 1000):
               # break
            
    #for k,v in wordData.items(): # create Word models and enter into db
        #word = Word_data(word=k, articleID = line['articleID'], word_count = 1, term_frequency = 0, inverse_term_frequency = 0)
        #word.save()

    #for k,v in docData.items(): # Document models
        #doc = Document_Data(article_id=k, language = v[0], province = v[1], city = v[2], country = v[4], 
                        #publication_Date = v[5], count = v[6], word_one = v[7], word_two = v[8], word_three = v[9],
                        #word_four = v[10], word_five = v[11], average_arousal_doc = v[12], average_valence_doc = v[13],
                        #average_arousal_words=v[14], average_valence_words=v[15])
        #doc.save()
    
    #print(len(wordDocData), 'LOL')
    #for k,v in wordDocData.items(): # WordInDocument models
        ##print(Word.objects.get(word=k[0]).word, Document.objects.get(article_id=k[1]).article_id)
        #wordDoc = Word_Data(word=Word_Data.objects.get(word=k[0]),document=Document_Data.objects.get(article_id=k[1]))
        #wordDoc.save()

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

def run():
    enterData(corpusPath4,sentimentPath4)


if __name__ == "__main__":
    run()

