import logging

from gensim.models import LdaModel
from gensim import corpora
from settings import Settings
from pymongo import MongoClient
import unicodedata
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w{3,}')

reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "models/dictionary.dict"
corpus_path = "models/corpus.lda-c"
lda_num_topics = 50
lda_model_path = "models/lda_model_50_topics.lda"

dictionary = corpora.Dictionary.load(dictionary_path)
corpus = corpora.BleiCorpus(corpus_path)
lda = LdaModel.load(lda_model_path)

i = 0
topics = {}
for topic in lda.show_topics(lda_num_topics):
    topicAndWordList = list(topic)
    topics[topicAndWordList[0]]=topicAndWordList[1]
    #print topics[topicAndWordList[0]]
    i += 1
    keyWord = {}
    for key in topics:
        temp = []
        temp = topics[key].split('+')
        keyWord[key] = []
        for elem in temp:
            keyWord[key].append(elem.split("*")[1])
        #print keyWord[key]
        
topicAverageRating = [0 for elem in topics]
totalWordCount = [0 for elem in topics]
topicSum = [0 for elem in topics]

reviews_cursor = reviews_collection.find()
    
for dataPoint in reviews_cursor:
    #temp = unicodedata.normalize('NFKD', dataPoint['text']).encode('ascii','ignore')
    raw = dataPoint['text'].lower()
    tokens = tokenizer.tokenize(raw)
    for word in tokens:
        #print type(dataPoint['text'])
        for key in topics:
            if word in keyWord[key]:
                topicSum[key] = topicSum[key] + float(dataPoint['stars'])
                totalWordCount[key] = totalWordCount[key] + 1
            if totalWordCount[key] > 0:
                topicAverageRating[key] = topicSum[key]/totalWordCount[key]

#print topicAverageRating
print 'Topic Number with max rating', ' ',topicAverageRating.index(max(topicAverageRating))
print 'Max rating ', ' - ', max(topicAverageRating)

print 'Topic Number with min rating', ' ',topicAverageRating.index(min(topicAverageRating))
print 'Min rating ', ' - ', min(topicAverageRating)
