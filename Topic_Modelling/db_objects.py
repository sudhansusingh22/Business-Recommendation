from pymongo import MongoClient
from settings import Settings
import logging

"""
this is a factory class to return the DBCollections
"""

class Constants(object):
    REVIEW = 'R'
    BUSINESS = 'B'
    CORPUS = 'C'
    TAGS = 'T'
    
class DBCollections(object):
    
    corpus_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.CORPUS_COLLECTION]
    reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.REVIEWS_COLLECTION]
    business_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][Settings.BUSINESS_COLLECTION]
    tags_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE][Settings.REVIEWS_COLLECTION]

    @staticmethod
    def get_collection(collection_name):
        if collection_name == Constants.REVIEW:
            return DBCollections.reviews_collection
        elif collection_name == Constants.BUSINESS:
            return DBCollections.business_collection
        elif collection_name == Constants.CORPUS:
            return DBCollections.corpus_collection
        elif collection_name == Constants.TAGS:
            return DBCollections.tags_collection
        else:
            return None
    
    """
     Get names of all databases present in MongoDB
    """
        
    @staticmethod
    def get_all_db_names():
        return MongoClient(Settings.MONGO_CONNECTION_STRING).database_names()
    
    """
    Call this method to check name of all the collections present in the database
    """
    
    @staticmethod
    def get_all_collections():
        return MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE].collection_names() + MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.TAGS_DATABASE].collection_names()
    
    """
    Start logging information of current task
    """
    @staticmethod
    def start_logging():
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    
    