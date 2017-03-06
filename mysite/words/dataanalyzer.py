import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# possible parameters: avg valence, avg arousal, avg valence top 5 words, avg arousal top 5 words, average tfidf of a word in the chunk, cosine distance for a word pair, N closest neighbors for a word

#def averageValence(chunk): # average valence of a list of documents
    
#def averageArousal(chunk): # average arousal of a list of documents
    
#def averageValenceTopFive(chunk):
    
#def averageArousalTopFive(chunk):
    
def averageTfidfOfWord(chunk, word):
    return
    
def cosDistanceOfPair(chunk, word1, word2, cbow=True):
    model = gensim.models.Word2Vec(chunk, min_count=1)
    return model.similarity(word1, word2)
    
def nClosestNeighborsOfWord(chunk, word, N, cbow=True):
    model = gensim.models.Word2Vec(chunk, min_count=1)
    return model.most_similar(positive=[word], topn=N)