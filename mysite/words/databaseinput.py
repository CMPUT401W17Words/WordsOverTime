# This module inputs the corpus and sentiment CSV files into Django's built-in SQLite database
# It will not be the final method of database input
# It can be used for quick testing of the data processing modules
# Uses the first 1000 corpus entries and 10000 sentiment entries

import os
import sys

import csv 
import django
import gensim

from words.models import Word, Document, WordInDocument

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append("C:/Users/L/Documents/School/WordsOverTime/mysite")
django.setup()

corpusPath = r'C:\Users\L\Documents\School\CMPUT\401\articles-can\articles-can.csv'
sentimentPath = r'C:\Users\L\Documents\School\CMPUT\401\sentiment_dict_3mil\sentiment_dict_3mil.csv'

# main function that will input corpus and sentiment info into the database
def enterData(corpusCsv, sentimentCsv):
    wordData = {} # represent models as dictionaries of primary key to list of other data
    docData = {}
    wordDocData = {}    
    
    fullCorpus = MainCorpus(corpusCsv)
    tfidf = gensim.models.tfidfmodel.TfidfModel(fullCorpus)
    sentDict = loadSentiment(sentimentCsv)
    
    for word in fullCorpus.dictionary.token2id.keys(): # get each word in the corpus
        wordData[word] = []
        
    with open(corpusCsv, 'r') as csvfile: # iterate over docs in the CSV file
        file = csv.DictReader(csvfile)
        count = 0
        for line in file:
            docData[line['articleID']] = []
            docData[line['articleID']].append(line['publicationDate']) # THIS LINE MAY BE BUGGED. depends on if the string date can be converted to an sql date properly
            words = line['parsedArticle'].split()
            tfidfs = tfidf[fullCorpus.dictionary.doc2bow(words)]
            #print(tfidfs)
            arousal = 0.0
            valence = 0.0
            arousal_five = []
            valence_five = []        
            for item in tfidfs: # get each word in the doc and its tfidf
                word = fullCorpus.dictionary[item[0]]
                value = item[1]
                #print(word,value)
                wordDocData[(word,line['articleID'])] = []
                wordDocData[(word,line['articleID'])].append(value)
            for word in words: # get sentiment info
                if word in sentDict:
                    currentArousal = sentDict[word][0]
                    currentValence = sentDict[word][1]
                    arousal = arousal + currentArousal
                    valence = valence + currentValence
                    if (len(arousal_five)<5):
                        arousal_five.append(currentArousal)
                    else:
                        arousal_five.sort()
                        for i in range(5):
                            if (arousal_five[i]<currentArousal):
                                arousal_five[i] = currentArousal
                                break                    
                    if (len(valence_five)<5):
                        valence_five.append(currentValence)
                    else:
                        valence_five.sort()
                        for i in range(5):
                            if (valence_five[i]<currentValence):
                                valence_five[i] = currentValence
                                break
            arousal_average_five = 0.0
            valence_average_five = 0.0
            for i in range(len(arousal_five)):
                arousal_average_five = arousal_average_five + arousal_five[i]
            for i in range(len(valence_five)):
                valence_average_five = valence_average_five + valence_five[i]     
            docData[line['articleID']].append(arousal/len(words))
            docData[line['articleID']].append(valence/len(words))
            docData[line['articleID']].append(arousal_average_five)
            docData[line['articleID']].append(valence_average_five)
            count = count + 1
            if (count > 1000):
                break
            
    for k,v in wordData.items(): # create Word models and enter into db
        word = Word(word=k)
        word.save()

    for k,v in docData.items(): # Document models
        doc = Document(article_id=k, publicationDate=v[0], average_arousal=v[1], average_valence=v[2],
                       average_arousal_five_highest=v[3], average_valence_five_highest=v[4])
        doc.save()
    
    for k,v in wordDocData.items(): # WordInDocument models
        wordDoc = WordInDocument(word=k[0],document=k[1],tfidf=v[0])
        wordDoc.save()

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
    with open(sentimentCsv, 'r', encoding="utf8") as csvfile:
        file = csv.DictReader(csvfile)
        count = 0
        for line in file:
            try:
                sentDict[line['Word']] = (float(line['Valence']), float(line['Arousal']))
            except ValueError:
                pass
                #print(line)
            count = count + 1
            if (count %100==0): 
                #print(count)
                sys.stdout.flush()
            if (count > 10000):
                break        
    return sentDict

def run():
    enterData(corpusPath,sentimentPath)