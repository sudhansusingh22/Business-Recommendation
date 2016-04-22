import os
import time
import json
from pymongo import MongoClient
import csv
import sys
import __init__
from settings import Settings
from collections import Counter
from get_collection import *
from Topic_Modelling.get_collection import DBCollections, Constants

dataset_file = Settings.DATASET_FILE

reviews_collection = DBCollections.get_collection(Constants.REVIEW)
business_collection = DBCollections.get_collection(Constants.BUSINESS)
reviews_collection.remove()
business_collection.remove()
c = Counter()
with open(Settings.BUSINESS_DATA_FILE) as dataset:
    for line in dataset:
            data = json.loads(line)
            c[data["city"]]+= 1
            if 'Restaurants' in data["categories"] and data['city'] == 'Pittsburgh':
               business_collection.insert({
                 "_id": data["business_id"]
               })

print c.most_common(10)
count = 0
done = 02
start = time.time()

with open(dataset_file) as dataset:
    count = sum(1 for line in dataset)
i = 0
with open(dataset_file) as dataset:
    next(dataset)
    for line in dataset:
        try:
            data = json.loads(line)
        except ValueError:
            print 'Oops!'
        isRestaurant = business_collection.find({"_id": data["business_id"]}).count();  
        if data["type"] == "review" and isRestaurant !=0:
            reviews_collection.insert({
                "reviewId": data["review_id"],
                "business": data["business_id"],
                "text": data["text"],
                "stars": data['stars'],
                "votes":data["votes"]
            })      
