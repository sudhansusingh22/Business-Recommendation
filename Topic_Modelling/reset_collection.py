from pymongo import MongoClient
from settings import Settings

"""
# Do not run this file 
"""
reviews_collection_bkp = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.REVIEWS_COLLECTION_BKP]
reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.REVIEWS_COLLECTION]
corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]

corpus_collection_bkp = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION_BKP]

# corpus_collection.remove()
# tags_collection.remove()


# c_c = corpus_collection.find()
# c_c_b = corpus_collection_bkp.find()

# corpus_collection_bkp.insert(list(c_c))
# corpus_collection.insert(list(c_c_b))