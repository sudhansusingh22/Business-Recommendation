"""
This class shows information about databases and the collections 
"""

from Topic_Modelling.db_objects import Constants,DBCollections

print "All Database present in MongoDB"
print DBCollections.get_all_db_names()
print
print "All collections present in the database"
print DBCollections.get_all_collections()
print
print "Review count"
print DBCollections.get_collection(Constants.REVIEW).find().count()
print
print "Business Id Count"
print DBCollections.get_collection(Constants.BUSINESS).find().count()
print
print "Corpus Collection Count"
print DBCollections.get_collection(Constants.CORPUS).find().count()
print
print "Tags Collection Count"
print DBCollections.get_collection(Constants.TAGS).find().count()


# r_c = reviews_collection.find()
# reviews_collection_bkp.insert(list(r_c))

# c_c = corpus_collection.find()
# corpus_collection_bkp.insert(list(c_c))

# create a back up for pittsburg data

# corpus_collection_pits.insert(list(r_c)) 
# print corpus_collection_pits.find().count()
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
    