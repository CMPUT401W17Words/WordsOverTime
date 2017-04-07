import gensim, logging
import decimal
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import words.dataretrieval
import os
import copy

NNsize = 300
minWords = 1#5
filePath = '/mnt/vol/matrices/'

def averageValence(docs): # average valence of a list of documents
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_valence_doc
    return result/len(docs)

def averageArousal(docs): # average arousal of a list of documents
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_arousal_doc
    return result/len(docs)
    
def averageValenceTopFive(docs):
    chunk = []
    for document in docs:
        chunk.append(words.dataretrieval.getWordsInDocument(document))
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    totalChunk = 0.0
    for doc in corpus:
        tfidfs = getTopFiveWords(tfidf[doc])
        totalDoc = 0.0
        for item in tfidfs:
            for wd,num in dictionary.token2id.items():
                if (num == item[0]):
                    word = wd
                    break
            if (words.dataretrieval.getValence(word) != None):
                totalDoc = totalDoc + words.dataretrieval.getValence(word)
        totalChunk = totalChunk + totalDoc/len(tfidfs)
    return totalChunk/len(chunk)

def averageArousalTopFive(docs):
    chunk = []
    for document in docs:
        chunk.append(words.dataretrieval.getWordsInDocument(document))
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    totalChunk = 0.0
    for doc in corpus:
        tfidfs = getTopFiveWords(tfidf[doc])
        if (len(tfidfs)<1):
            continue
        totalDoc = 0.0
        for item in tfidfs:
            for wd,num in dictionary.token2id.items():
                if (num == item[0]):
                    word = wd
                    break
            if (words.dataretrieval.getArousal(word) != None):
                totalDoc = totalDoc + words.dataretrieval.getArousal(word)
        totalChunk = totalChunk + totalDoc/len(tfidfs)
    return totalChunk/len(chunk)

# helper
def getTopFiveWords(tfidfsDoc):
    result = []
    tfidfs = copy.deepcopy(tfidfsDoc)
    topWord = getTopWord(tfidfs)
    while ((topWord != None) and (len(result)<5)):
        result.append(topWord)
        tfidfs.remove(topWord)
        topWord = getTopWord(tfidfs)
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

def averageTfidfOfWord(chunk, word):
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    totalTfidf = 0.0
    docCount = 0.0
    wordId = dictionary.token2id[word]
    for doc in corpus:
        for item in tfidf[doc]:
            if (item[0] == wordId):
                totalTfidf = totalTfidf + item[1]
                break
        docCount = docCount + 1
    return totalTfidf/docCount
    
def cosDistanceOfPair(chunk, word1, word2, cbow, hashStr, chunkDate):
    if (cbow==True):
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=0)
    else:
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=1)
    saveMatrix(model, word1+word2, hashStr, chunkDate)
    return model.similarity(word1, word2)
   
def nClosestNeighboursOfWord(chunk, word, N, cbow, hashStr, chunkDate):
    if (cbow==True):
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=0)
    else:
        model = gensim.models.Word2Vec(chunk, size=NNsize, min_count=minWords, sg=1)
    saveMatrix(model, word, hashStr, chunkDate)
    return model.most_similar(positive=[word], topn=N)

def wordFrequency(chunk, word):
    result = 0.0
    for doc in chunk:
        result = result + doc.count(word)
    return result

def relativeWordFrequency(chunk, word):
    wordCount = 0.0
    totalWordCount = 0.0
    for doc in chunk:
        wordCount = wordCount + doc.count(word)
        totalWordCount = totalWordCount + len(doc)
    return wordCount/totalWordCount

def probX(chunk, x):
    count = 0.0
    for doc in chunk:
        if x in doc:
            count = count + 1.0
    return count/len(chunk)

def probXAndY(chunk, x, y):
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

def probXGivenY(chunk, x, y):
    return probXAndY(chunk,x,y)/probX(chunk,y)

def probXGivenNotY(chunk, x, y):
    return probXAndNotY(chunk, x, y)/(1.0 - probX(chunk, y))

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
    wordCount = 0
    for doc in chunk:
        if word in doc:
            wordCount = wordCount + doc.count(word)
            if (wordCount >= minWords):
                return False
    return True

def saveMatrix(model, word, hashStr, chunkDate):
    path = filePath+hashStr+'/'+word+'/'+str(chunkDate)
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    try:
        model.wv.save_word2vec_format(path+'/model', fvocab=path+'/vocab')
    except:
        pass
