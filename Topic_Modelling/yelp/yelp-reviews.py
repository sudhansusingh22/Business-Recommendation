import os
import time
import json
from pymongo import MongoClient
import csv
import sys
import __init__
from settings import Settings
from collections import Counter


dataset_file = Settings.DATASET_FILE
reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.REVIEWS_COLLECTION]
reviews_collection.remove()
business_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.BUSINESS_COLLECTION]

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
""""o = open(dataset_file,'rU')
reader = csv.reader(o)
row_count = sum(1 for row in reader)
all_reviews = []
with open(dataset_file, 'rb') as f:
#     for i in range(len(bids)):
        reader = csv.DictReader(f)
#         id = bids[i]
#         print id
        rows = [row for row in reader if row['business_id'] == [id in bids]]
        print len(rows)
# all_reviews = []
# with open(dataset_file, 'rb') as f:
#     for bid in bids:
#         reader = csv.DictReader(f)
#         rows = [row for row in reader if row['business_id'] == str(bid)]
#         print len(rows)
#         all_reviews.extend(rows)
    # row_count1 = sum(1 for row in filtered)
print len(all_reviews)
"""
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
