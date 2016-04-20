import multiprocessing
import time
import sys
from nltk import WordNetLemmatizer

import nltk
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from settings import Settings
tokenizer = RegexpTokenizer(r'\w{3,}')
from stop_words import get_stop_words
corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]


def load_stopwords():
    stopwords = []
    with open('stopwords.txt', 'rU') as f:
        for line in f:
            stopwords.append(line.strip())

    return stopwords
print load_stopwords()
# create English stop words list
en_stop = get_stop_words('en')
lem = WordNetLemmatizer()

def worker(identifier, skip, count):
    done = 0
    start = time.time()

    stopwords = load_stopwords()
    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
        Settings.REVIEWS_COLLECTION]
    tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][
        Settings.REVIEWS_COLLECTION]
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


def main():
    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
        Settings.REVIEWS_COLLECTION]
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
    
# number of workers should be equal to the number of cores available in the system
# http://xmodulo.com/how-to-find-number-of-cpu-cores-on.html
# http://stackoverflow.com/questions/20886565/python-using-multiprocessing-process-with-a-maximum-number-of-simultaneous-pro
    
