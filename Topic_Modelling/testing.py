from pymongo import MongoClient
from settings import Settings
import json
from bson.json_util import dumps
import make_json_serializable  # apply monkey-patch
import simplejson as sjson
from bson import json_util
# class Foo(object):
#     def __init__(self, name):
#         self.name = name
#     def to_json(self):  # New special method.
#         return "{u'name': %r}" % self.name.decode('utf-8')

reviews_collection_bkp = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION_BKP]
reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]
corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]
corpus_collection_bkp = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION_BKP]

corpus_collection_pits = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION_PITTSBURG]

# print tags_cursor.count()


print corpus_collection.find().count()



r_c = reviews_collection.find()
# reviews_collection_bkp.insert(list(r_c))

# c_c = corpus_collection.find()
# corpus_collection_bkp.insert(list(c_c))

# create a back up for pittsburg data

corpus_collection_pits.insert(list(r_c)) 
print corpus_collection_pits.find().count()
# print corpus_collection_bkp.find().count()

# with open("collections/review.json", "w") as f:
#     l = [] 
#     for doc in reviews_collection.find():
#         l.append(doc)
#     json.dump(l,f)

# with open("collections/review.json") as dataset:
#  
#     next(dataset)
#     for line in dataset:
#         data = json.loads(line)
#         reviews_collection_bkp.insert({
#                 "reviewId": data["reviewId"],
#                 "business": data["business"],
#                 "text": data["text"],
#                 "stars": data['stars'],
#                 "votes":data["votes"]
#             })    
# print reviews_collection_bkp.find().count()  
         
# reviews_collection_bkp.remove()
# reviews_collection_bkp.remove()
# with open("collections/review.json") as dataset:
#     for line in dataset:
# #             print line
#             data = json.loads(line)
#             print data
#             break
#             reviews_collection_bkp.insert({
#                  "reviewId": data["reviewId"],
#                  "business": data["business"],
#                  "text": data["text"],
#                  "stars": data['stars'],
#                  "votes":data["votes"]
#              })
# print reviews_collection_bkp.find().count()  
# with open("collections/review.json") as dataset:
#     for line in dataset:
#         data = json.loads(line)
# #         print(data)
#         for doc in dict(data):
# #             print type(doc)
#             reviews_collection_bkp.insert({
#                 "reviewId": doc["reviewId"],
#                 "business": data["business"],
#                 "text": data["text"],
#                 "stars": data['stars'],
#                 "votes":data["votes"]
#             })     
# print reviews_collection_bkp.find().count()  
    