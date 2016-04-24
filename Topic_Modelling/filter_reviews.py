import json
import time
from collections import Counter
from Topic_Modelling.settings import *
from db_objects import *

"""
This file is used filter review and business ids based on certain location
"""


# define the data_file name to read the review data from the json file

dataset_file = Settings.DATASET_FILE

# get the review collection and the business collection
 
reviews_collection = DBCollections.get_collection(Constants.REVIEW)
business_collection = DBCollections.get_collection(Constants.BUSINESS)

print reviews_collection
print business_collection


# delete existing review and business collections so that for a new city new collections should be created.

reviews_collection.remove()
business_collection.remove()

"""
Populate business collection based on the city
To populate with a new city, change the city name
"""

c = Counter()
with open(Settings.BUSINESS_DATA_FILE) as dataset:
    for line in dataset:
            data = json.loads(line)
            c[data["city"]]+= 1
            if 'Restaurants' in data["categories"] and data['city'] == 'Pittsburgh':
                business_collection.insert({
                                           "_id": data["business_id"]
               })

# print most common city 

print c.most_common(10)
count = 0
done = 02
start = time.time()

"""
Populate review collection based on the business IDs corresponding to the city selected in the previous step city
"""

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
