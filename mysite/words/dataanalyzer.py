import gensim, logging
import decimal
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# possible parameters: avg valence, avg arousal, avg valence top 5 words, avg arousal top 5 words, average tfidf of a word in the chunk, cosine distance for a word pair, N closest neighbors for a word
# chunk has the format [['word', 'word],['word','word']]
# docs is a list of Document_Data objects

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
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_valence_words
    return result/len(docs)
    
def averageArousalTopFive(docs):
    result = decimal.Decimal(0.0)
    for doc in docs:
        result = result + doc.average_arousal_words
    return result/len(docs)

# each corpus is a list of documents
# each document is a list of tuples
# each tuple is an id,count pair, where id maps to a word and count is the number of times the word appears in the document
# pass in a chunk as a list of documents, where each document is a list of words, something like [['word', 'word],['word','word']]
# dictionary = corpora.Dictionary(texts): map each word appearing in the corpus "texts" to an id
# dictionary.doc2bow(text): using the mapping of the dictionary, convert text to gensim's corpus format where each text is a list of words
# corpus = [dictionary.doc2bow(text) for text in texts]: pass in texts as a list of lists of words
def averageTfidfOfWord(chunk, word):
    dictionary = gensim.corpora.Dictionary(chunk)
    corpus = [dictionary.doc2bow(text) for text in chunk]
    tfidf = gensim.models.TfidfModel(corpus)
    corpusTfidf = tfidf[corpus]
    totalTfidf = 0.0
    docCount = 0.0
    wordId = dictionary.token2id[word]
    for doc in corpusTfidf:
        for word in doc:
            if (word[0] == wordId):
                totalTfidf = totalTfidf + word[1]
                break
        docCount = docCount + 1
    return totalTfidf/docCount
    
def cosDistanceOfPair(chunk, word1, word2, cbow=True):
    #print(chunk)
    model = gensim.models.Word2Vec(chunk, min_count=1)
    return model.similarity(word1, word2)
    
def nClosestNeighboursOfWord(chunk, word, N, cbow=True):
    model = gensim.models.Word2Vec(chunk, min_count=1)
    return model.most_similar(positive=[word], topn=N)

def wordFrequencyInChunk(chunk, word):
    pass

def probXAndY(chunk, x, y):
    # probability that an article in the chunk has both x and y?
    # all articles with x and y / total articles
    pass

def probXGivenY(doc, x, y):
    # probability that an article has x given that it has y?
    # probXAndY / probY
    pass