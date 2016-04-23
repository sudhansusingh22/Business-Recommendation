import logging

from gensim.models import LdaModel
from gensim import corpora
from settings import Settings
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w{3,}')

reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary_path = "models/dictionary.dict"
corpus_path = "models/corpus.lda-c"
lda_num_topics = 6
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
     
# for dataPoint in reviews_cursor:
#     #temp = unicodedata.normalize('NFKD', dataPoint['text']).encode('ascii','ignore')
#     raw = dataPoint['text'].lower()
#     tokens = tokenizer.tokenize(raw)
#     for word in tokens:
#         #print type(dataPoint['text'])
#         for key in topics:
#             if word in keyWord[key]:
#                 topicSum[key] = topicSum[key] + float(dataPoint['stars'])
#                 totalWordCount[key] = totalWordCount[key] + 1
#             if totalWordCount[key] > 0:
#                 topicAverageRating[key] = topicSum[key]/totalWordCount[key]
# 
# print "Feedback to open new business in particular area"
# print 'Topic Number with max rating', ' ',topicAverageRating.index(max(topicAverageRating))
# print 'Max rating ', ' - ', max(topicAverageRating)
# 
# print 'Topic Number with min rating', ' ',topicAverageRating.index(min(topicAverageRating))
# print 'Min rating ', ' - ', min(topicAverageRating)


topicAverageRating = [float(0) for elem in topics]
totalWordCount = [float(0) for elem in topics]
topicSum = [float(0) for elem in topics]

reviews_cursor = reviews_collection.find()


count = 0

reviews_cursor = reviews_collection.find()

# busineesReviewCount = {}
# 
# for elem in reviews_cursor:
#     busineesReviewCount[elem['business']] = 0
# reviews_cursor = reviews_collection.find()
# 
# for elem in reviews_cursor:
#     busineesReviewCount[elem['business']] = busineesReviewCount[elem['business']] + 1
#     
# sortedbusinessReviewCount = sorted(busineesReviewCount.items(), key=operator.itemgetter(1))
# for element in sortedbusinessReviewCount:
#     print "review count ", element[0], element[1]

for dataPoint in reviews_cursor:
    raw = dataPoint['text'].lower()
    tokens = tokenizer.tokenize(raw)
    for word in tokens:
        #print type(dataPoint['text'])
        for key in topics:
            #print dataPoint['business']
            if dataPoint['business'] == 'SsGNAc9U-aKPZccnaDtFkA':
                if word in keyWord[key]:
                    topicSum[key] = topicSum[key] + float(dataPoint['stars'])
                    totalWordCount[key] = totalWordCount[key] + 1
                if totalWordCount[key] > 0:
                    topicAverageRating[key] = topicSum[key]/totalWordCount[key]


businessRating = {}

class businessRatingClass:
    averageRating = 0
    ratingCount = 0
    
    def __init__(self, rating, count):
        self.averageRating = rating
        self.ratingCount = count
    
    def getAverageRating(self):
        return self.averageRating
# for index in range(0,len(topicAverageRating)):
#     if topicAverageRating[index]>0:
#         businessRating[index] = topicAverageRating[index]
#         businessRatingCount[index] = totalWordCount[index]

for index in range(0,len(topics)):
    newBusinessObject = businessRatingClass(topicAverageRating[index], totalWordCount[index])
    businessRating[index] = newBusinessObject
    #businessRating.append(newBusinessObject)
        
sortedbusinessRating = sorted(businessRating.items(), key=lambda value : value[1].averageRating)

minRating = 5
minIndex = 0
minRatingCount = 0

for element in sortedbusinessRating:
    #print element[0], element[1].averageRating, element[1].ratingCount
    if element[1].averageRating < minRating and element[1].ratingCount > 0:
        minRating = element[1].averageRating
        minIndex = element[0]
        minRatingCount = element[1].ratingCount


print '\n'
print "Feedback to business with ID - SsGNAc9U-aKPZccnaDtFkA"
print 'Topic Number with min rating', ' ',minIndex
print 'Min rating ', ' - ', minRating, 'with count ', minRatingCount

print 'Topic Number with max rating', ' ',sortedbusinessRating[-1][0]
print 'Max rating ', ' - ', sortedbusinessRating[-1][1].averageRating, 'with count ', sortedbusinessRating[-1][1].ratingCount