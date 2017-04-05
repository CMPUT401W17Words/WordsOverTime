"""
Gensim wrapper that analyzes chunks of data
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import sys
sys.path.append("C:/Users/L/Documents/School/WordsOverTime")

import gensim, logging
import decimal
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import words.dataretrieval
import os
# possible parameters: avg valence, avg arousal, avg valence top 5 words, avg arousal top 5 words, average tfidf of a word in the chunk, cosine distance for a word pair, N closest neighbors for a word
# chunk has the format [['word', 'word],['word','word']]
# docs is a list of Document_Data objects

NNsize = 300
minWords = 5
#filePath = '/mnt/vol/matrices/'
filePath = 'C:/Users/L/Documents/School/'

"""
Returns the average valence of a list of Document_Data objects
"""
def averageValence(docs): # average valence of a list of documents
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_valence_doc
    return result/len(docs)

"""
Returns the average arousal of a list of Document_Data objects
"""
def averageArousal(docs): # average arousal of a list of documents
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_arousal_doc
    return result/len(docs)
    
"""
Returns the average valence of the five words with the highest tfidfs in a list of Document_Data objects
"""
def averageValenceTopFive(docs):
    chunk = []
    for document in docs:
        chunk.append(words.dataretrieval.getWordsInDocument(document))
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    totalChunk = 0.0
    for doc in chunk:
        tfidfs = getTopFiveWords(tfidf[doc])
        totalDoc = 0.0
        for item in tfidfs:
            for wd,num in dictionary.token2id:
                if (num == item[0]):
                    word = wd
                    break
            totalDoc = totalDoc + words.dataretrieval.getValence(word)
        totalChunk = totalChunk + totalDoc/len(tfidfs)
    return totalChunk/len(chunk)

"""
Returns the average arousal of the five words with the highest tfidfs in a list of Document_Data objects
"""
def averageArousalTopFive(docs):
    chunk = []
    for document in docs:
        chunk.append(words.dataretrieval.getWordsInDocument(document))
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    totalChunk = 0.0
    for doc in chunk:
        tfidfs = getTopFiveWords(tfidf[doc])
        totalDoc = 0.0
        for item in tfidfs:
            for wd,num in dictionary.token2id:
                if (num == item[0]):
                    word = wd
                    break
            totalDoc = totalDoc + words.dataretrieval.getArousal(word)
        totalChunk = totalChunk + totalDoc/len(tfidfs)
    return totalChunk/len(chunk)

# helper
def getTopFiveWords(tfidfsDoc):
    result = []
    tfidfs = tfidfsDoc.copy().items()
    topWord = getTopWord(tfidfs)
    while (topWord != None):
        result.append(topWord)
        tfidfs.pop(topWord[0])
    return result

# helper  
def getTopWord(tfidfs):
    current = None
    for item in tfidfs:
        if (current == None):
            current = item
        else:
            if (item[1]>current[1]):
                current = item
    return current

# each corpus is a list of documents
# each document is a list of tuples
# each tuple is an id,count pair, where id maps to a word and count is the number of times the word appears in the document
# pass in a chunk as a list of documents, where each document is a list of words, something like [['word', 'word],['word','word']]
# dictionary = corpora.Dictionary(texts): map each word appearing in the corpus "texts" to an id
# dictionary.doc2bow(text): using the mapping of the dictionary, convert text to gensim's corpus format where each text is a list of words
# corpus = [dictionary.doc2bow(text) for text in texts]: pass in texts as a list of lists of words
# not sure if bugged... seems to be sort of working
"""
Return the average tfidf of a word in a chunk of documents
Chunk is a nested list of documents where each document is a list of words
"""
def averageTfidfOfWord(chunk, word):
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    #print(tfidf)
    #print(corpus)
    totalTfidf = 0.0
    docCount = 0.0
    wordId = dictionary.token2id[word] # THIS CAUSES ERROR IF WORD NOT IN CHUNK
    for doc in corpus:
        #print(doc)
        #print(tfidf[doc])
        for item in tfidf[doc]:
            if (item[0] == wordId):
                totalTfidf = totalTfidf + item[1]
                break
        docCount = docCount + 1
    return totalTfidf/docCount
    #corpusTfidf = tfidf[corpus]
    #for doc in corpusTfidf:
        #for wordd in doc:
            #if (wordd[0] == wordId):
                #totalTfidf = totalTfidf + wordd[1]
                #break

"""
Return the cosine distance between two words in a chunk of documents
Chunk is a nested list of documents where each document is a list of words
If cbow is True, use cbow, else skipgram
The training matrix is saved to disk based on the hash and date
"""    
def cosDistanceOfPair(chunk, word1, word2, cbow, hashStr, chunkDate):
    if (cbow==True):
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=0)
    else:
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=1)
    #model.save(filePath+hashStr+'/'+word1+word2+'/'+str(chunkDate)) # save models to /mnt/vol/matrices/somehash/word1word2/somedate. email the user by zipping the somehash folder
    saveMatrix(model, word1+word2, hashStr, chunkDate)
    return model.similarity(word1, word2)

"""
Return the N closest neighbours of a word in a chunk of documents
Chunk is a nested list of documents where each document is a list of words
If cbow is True, use cbow, else skipgram
The training matrix is saved to disk based on the hash and date
"""     
def nClosestNeighboursOfWord(chunk, word, N, cbow, hashStr, chunkDate):
    if (cbow==True):
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=0)
    else:
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=1)
    #model.save(filePath+hashStr+'/'+word+'/'+str(chunkDate)) # save models to /mnt/vol/matrices/somehash/someword/somedate. email the user by zipping the somehash folder
    saveMatrix(model, word, hashStr, chunkDate)
    return model.most_similar(positive=[word], topn=N)

"""
Return the frequency of a word in a chunk
Chunk is a nested list of documents where each document is a list of words
"""
def wordFrequency(chunk, word):
    result = 0.0
    for doc in chunk:
        result = result + doc.count(word)
    return result

# fullFreq is frequency in full corpus
#def relativeWordFrequency(chunk, word, fullFreq):
    #return wordFrequency(chunk,word)/fullFreq # MUST CHECK IF fullFreq = 0

"""
Return the relative frequency of a word in a chunk
Chunk is a nested list of documents where each document is a list of words
"""
def relativeWordFrequency(chunk, word):
    wordCount = 0.0
    totalWordCount = 0.0
    for doc in chunk:
        wordCount = wordCount + doc.count(word)
        totalWordCount = totalWordCount + len(doc)
    return wordCount/totalWordCount # multiply by 1000000 to get occurences per million

def probX(chunk, x):
    count = 0.0
    for doc in chunk:
        if x in doc:
            count = count + 1.0
    return count/len(chunk)

"""
Return the probability of word x and y appearing together in a chunk
Chunk is a nested list of documents where each document is a list of words
"""
def probXAndY(chunk, x, y):
    # probability that an article in the chunk has both x and y?
    # all articles with x and y / total articles
    count = 0.0
    for doc in chunk:
        if ((x in doc) and (y in doc)):
            count = count + 1.0
    return count/len(chunk)

def probXAndNotY(chunk, x, y):
    count = 0.0
    for doc in chunk:
        if ((x in doc) and (y not in doc)):
            count = count + 1.0
    return count/len(chunk)

"""
Return the probability of word x appearing in a chunk given y has appeared
Chunk is a nested list of documents where each document is a list of words
"""
def probXGivenY(chunk, x, y):
    # probability that an article has x given that it has y?
    # probXAndY / probY
    return probXAndY(chunk,x,y)/probX(chunk,y)

"""
Return the probability of word x appearing in a chunk given y has not appeared
Chunk is a nested list of documents where each document is a list of words
"""
def probXGivenNotY(chunk, x, y):
    return probXAndNotY(chunk, x, y)/(1.0 - probX(chunk, y))
    
    #notY = 1.0 - probX(chunk, y)
    #if (notY == 0):
        #return 0.0
    #xAndNotY = probX(chunk, x)*notY
    #return xAndNotY/notY

# return 1 if probX = 0, 2 if probX = 1, and 0 if no error
def probException(chunk, x):
    pX = probX(chunk, x)
    if (pX.is_integer()):
        if (pX == 0.0):
            return 1
        if (pX == 1.0):
            return 2
        return 0
    else:
        return 0

def wordNotInChunkException(chunk, word):
    for doc in chunk:
        if word in doc:
            return False
    return True

"""
Saves a learned matrix to disk based on a hash
"""
def saveMatrix(model, word, hashStr, chunkDate):
    path = filePath+hashStr+'/'+word+'/'+str(chunkDate)
    try: 
        os.makedirs(path, 0o777)
    except OSError:
        if not os.path.isdir(path):
            raise
    os.chmod(path, 0o777)
    #os.chmod(path, 0777)
    with open(path+'ff.txt', 'a+b'):
        os.chmod(path+'ff.txt', 0o777)
        try:
            model.save(path)
        except:
            print('model save failed')
            #raise