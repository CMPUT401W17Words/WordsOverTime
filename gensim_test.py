# http://radimrehurek.com/gensim/index.html

# import modules & set up logging
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
 # word2vec: skipgram and CBOW
sentences = [['first', 'sentence'], ['second', 'sentence']] # corpus chunk selected by user
model = gensim.models.Word2Vec(sentences, min_count=1) # generate matrix on corpus. other parameters control the training, and you can choose cbow or skipgram
model.similarity('first', 'sentence') # cosine distance for word pairs... i think
most_similar(positive=['first', 'word'], negative=['now', 'stop'], topn=10) # N closest/farthest neighbours in the matrix for a list of words

# tfidf
#idf = gensim.models.tfidfmodel.TfidfModel(corpus) # calculate idf of each word in the whole corpus... i think
#tfidf = tfidf[some_doc] # calculate tfidf of each word in a given document... i think

