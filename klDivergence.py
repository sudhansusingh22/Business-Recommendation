
import json
import pandas as pd
from glob import glob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
    level=logging.INFO)
from gensim import corpora, models, similarities, matutils
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import json
import re
import pylab

# Creates Corpus for LDA algorithm
class MyCorpus(object):
    def __init__(self, fname, stopf = None, V = None):
        self.fname = fname
        self.file = open(fname, "r")
        stoplist = stopf
        #print "make dictionary started"
        self.dictionary = self.make_dict(stoplist, V)
    def reset(self):
        self.file.seek(0)
    def proc(self, line):
        return filter(lambda x: len(x) > 2, map(lambda x: x.strip(), re.sub(r'[0-9]+|\W',' ',line.strip().lower()).split()))
    def make_dict(self, stoplist = [], V = None):
        self.reset()
        # read all terms
        #print "Corpora.Dictionary"
        dictionary = corpora.Dictionary(self.proc(line) for line in self.read_file())
        # remove stop words
        stop_ids = [dictionary.token2id[sw] for sw in stoplist if sw in dictionary.token2id]
        dictionary.filter_tokens(stop_ids)
        # remove words which occur in less than 5 documents or more than 50% of documents
        dictionary.filter_extremes(keep_n = V)
        #print "Corpora.Dictionary end"
        return dictionary
    def read_file(self):
        #print "read_file"
        for line in self.file:
                txt = json.loads(line)["text"]
                if len(txt) > 5: yield txt
    
    def __iter__(self):
        #print "iter"
        self.reset()
        for line in self.read_file():
            bow = self.dictionary.doc2bow(self.proc(line))
            if len(bow) >= 5: yield bow

# Define KL function
def sym_kl(p,q):
    return np.sum([stats.entropy(p,q),stats.entropy(q,p)])

# Main Function
if __name__ == '__main__':
    stoplist = stopwords.words('english')
    yelp = MyCorpus('review_json_file_pittsburgh_restaurant.json', stoplist, 10000)
    K = 5
    kl = []
    l = np.array([sum(cnt for _, cnt in doc) for doc in yelp])
    # Find the list of KL divergences of different values of K(No. of Topics)
    for i in range(1,2,1):
        lda = models.ldamodel.LdaModel(corpus = yelp, id2word = yelp.dictionary, num_topics = K, update_every = 1)#, chunksize = 100000, passes = 3
        m1 = lda.expElogbeta
        U,cm1,V = np.linalg.svd(m1)
        #Document-topic matrix
        lda_topics = lda[yelp]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2/cm2norm
        kl.append(sym_kl(cm1,cm2))
    print kl
    # Plot the graph for KL convergence
    plt.plot(kl)
    plt.ylabel('Symmetric KL Divergence')
    plt.xlabel('Number of Topics')
    plt.show()
    plt.plot(kl)
    plt.ylabel('Symmetric KL Divergence')
    plt.xlabel('Number of Topics')
    plt.savefig('kldiv.png', bbox_inches='tight')

    
