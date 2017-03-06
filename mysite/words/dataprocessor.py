import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import csv
import sys

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
def loadSentiment():
    sentDict = {}
    with open(sent_path, 'r', encoding="utf8") as csvfile:
        file = csv.DictReader(csvfile)
        count = 0
        for line in file:
            try:
                sentDict[line['Word']] = (float(line['Valence']), float(line['Arousal']))
            except ValueError:
                print("error on line")
                #print(line)
            count = count + 1
            if (count %100==0): 
                #print(count)
                sys.stdout.flush()
            if (count > 10000):
                break        
    return sentDict

# ACTUAL CODE STARTS HERE

#wordData = {} # represent models as dictionaries of primary key to list of other data
#docData = {}
#wordDocData = {}

#fullCorpus = MainCorpus(nothing)
#tfidf = gensim.models.tfidfmodel.TfidfModel(fullCorpus)
#sentDict = loadSentiment()
##print(fullCorpus.dictionary.token2id)
##print(sentDict)

#for word in fullCorpus.dictionary.token2id.keys(): # get each word in the corpus
    ##print(word)
    #wordData[word] = []
    
#with open(file_path, 'r') as csvfile: # iterate over docs in the CSV file
    #file = csv.DictReader(csvfile)
    #count = 0
    #for line in file:
        #docData[line['articleID']] = []
        #docData[line['articleID']].append(line['publicationDate'])
        #words = line['parsedArticle'].split()
        #tfidfs = tfidf[fullCorpus.dictionary.doc2bow(words)]
        ##print(tfidfs)
        #arousal = 0.0
        #valence = 0.0
        #arousal_five = []
        #valence_five = []        
        #for item in tfidfs: # get each word in the doc and its tfidf
            #word = fullCorpus.dictionary[item[0]]
            #value = item[1]
            ##print(word,value)
            #wordDocData[(word,line['articleID'])] = []
            #wordDocData[(word,line['articleID'])].append(value)
        #for word in words: # get sentiment info
            #if word in sentDict:
                #currentArousal = sentDict[word][0]
                #currentValence = sentDict[word][1]
                #arousal = arousal + currentArousal
                #valence = valence + currentValence
                #if (len(arousal_five)<5):
                    #arousal_five.append(currentArousal)
                #else:
                    #arousal_five.sort()
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
        #arousal_average_five = 0.0
        #valence_average_five = 0.0
        #for i in range(len(arousal_five)):
            #arousal_average_five = arousal_average_five + arousal_five[i]
        #for i in range(len(valence_five)):
            #valence_average_five = valence_average_five + valence_five[i]     
        #docData[line['articleID']].append(arousal/len(words))
        #docData[line['articleID']].append(valence/len(words))
        #docData[line['articleID']].append(arousal_average_five)
        #docData[line['articleID']].append(valence_average_five)
        #count = count + 1
        #if (count > 1000):
            #break
##print(wordData)
##print(docData)
##print(wordDocData)

#for k,v in wordData.items(): # create Word models and enter into db
    #word = Word(word=k)
    #word.save()

#for k,v in docData.items(): # Document models
    #doc = Document(article_id=k, publicationDate=v[0], average_arousal=v[1], average_valence=v[2],
                   #average_arousal_five_highest=v[3], average_valence_five_highest=v[4])
    #doc.save()
    
#for k,v in wordDocData.items(): # WordInDocument models
    #wordDoc = WordInDocument(word=k[0],document=k[1],tfidf=v[0])
    #wordDoc.save()        