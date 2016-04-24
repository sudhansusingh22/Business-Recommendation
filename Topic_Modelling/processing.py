import multiprocessing
import time
import sys
from nltk import WordNetLemmatizer

import nltk
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from settings import Settings
from stop_words import get_stop_words
from Topic_Modelling.db_objects import *

# loading corpus collections

corpus_collection = DBCollections.db_objects(Constants.CORPUS)

"""
create Tokenizer
Based on this tokenizer we are filtering out the words which have length grater than 3 and train our model on this data,
So that there would be less noise words in the document.
But restricting the word size count to 3 will cause any performance issue in the LDA Model is an open question to us:
Link to stackoverflow post:
http://stackoverflow.com/questions/36673316/latent-dirichlet-allocationlda-performance-by-limiting-word-size-for-corpus-do
"""

tokenizer = RegexpTokenizer(r'\w{3,}')


def load_stopwords():
    stopwords = []
    with open('files/stopwords.txt', 'rU') as f:
        for line in f:
            stopwords.append(line.strip())
    return stopwords


print load_stopwords()

# create English stop words list

en_stop = get_stop_words('en')

# create lemmatizer object

lem = WordNetLemmatizer()


"""
This method runs on different cores of the system. While multiprocessing we have create 4 workers and tested our code to 
run of 4 different cores of the system
"""

def worker(identifier, skip, count):
    done = 0
    start = time.time()

    reviews_collection = DBCollections.db_objects(Constants.REVIEW)
    batch_size = 50
    for batch in range(0, count, batch_size):
        reviews_cursor = reviews_collection.find().skip(skip + batch).limit(batch_size)
        for review in reviews_cursor:
            raw = review['text'].lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [i for i in tokens if not i in en_stop]
            texts = [lem.lemmatize(i) for i in stopped_tokens]
            tagged_text = nltk.pos_tag(texts)
            words = []
            words = [b[0]  for b in tagged_text if b[-1] in ['NN','NNS']]
            corpus_collection.insert({
                              "reviewId": review["reviewId"],
                              "business": review["business"],
                              "text": review["text"],
                              "words": words
                              })
            done += 1
            if done % 100 == 0:
                end = time.time()
                print 'Worker' + str(identifier) + ': Done ' + str(done) + ' out of ' + str(count) + ' in ' + (
                    "%.2f" % (end - start)) + ' sec ~ ' + ("%.2f" % (done / (end - start))) + '/sec'
                sys.stdout.flush()


"""
main method: calls the worker method on different cores of the system
   
number of workers should be equal to the number of cores available in the system
http://xmodulo.com/how-to-find-number-of-cpu-cores-on.html
http://stackoverflow.com/questions/20886565/python-using-multiprocessing-process-with-a-maximum-number-of-simultaneous-pro
"""   

def main():
    reviews_collection = DBCollections.db_objects(Constants.REVIEW)
    reviews_cursor = reviews_collection.find()
    count = reviews_cursor.count()
    print count
    workers = 4
    batch = count / workers
    left = count % workers
    jobs = []
    for i in range(workers):
        size = count / workers
        if i == (workers - 1):
            size += left
        p = multiprocessing.Process(target=worker, args=((i + 1), i * batch, size))
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()
        print '%s.exitcode = %s' % (j.name, j.exitcode)

if __name__ == '__main__':
    main()

 
