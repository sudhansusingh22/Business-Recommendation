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
    