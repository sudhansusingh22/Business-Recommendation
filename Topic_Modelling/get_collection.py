from pymongo import MongoClient
from settings import Settings


"""
this is a factory class to return the DBCollections
"""

class Constants(object):
    REVIEW = 'R'
    BUSINESS = 'B'
    CORPUS = 'C'
    
class DBCollections(object):
    
    corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]
    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.REVIEWS_COLLECTION]
    business_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.BUSINESS_COLLECTION]

    @staticmethod
    def get_collection(collection_name):
        if collection_name == Constants.REVIEW:
            return DBCollections.reviews_collection
        elif collection_name == Constants.BUSINESS:
            return DBCollections.business_collection
        elif collection_name == DBCollections.corpus_collection:
            return DBCollections.corpus_collection
        else:
            return None
