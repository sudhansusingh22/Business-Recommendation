from gensim import corpora, models
from nltk.corpus import stopwords
import json
import re
import pandas as pd
import ijson
from pandas import *
import ast

def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob   


if __name__ == '__main__':
    # 
    
    #Load Bussiness Data from File to Pandas Dataframe
    businessJsonFileName = "./dataset/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
    df = pd.DataFrame([convert(line) for line in file(businessJsonFileName)])
    #Filter out the required columns from dataframe
    df1 = df[["business_id","name","city",'categories']]
    #Filter out Business data for restaurants at Pittsburgh location
    df2 = df1[df1.city == "Pittsburgh"]
    business_id = df2['business_id'].tolist()
    #Save Business id into sets for review data filtering
    business_id = set(business_id)

    reviewJsonFileName = "./dataset/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"
    finalReviewJsonFile = "review_json_file_pittsburgh_restaurant.json"
    outfile = open (finalReviewJsonFile,"w")
    data = []
    rowcnt = 0
    #Filter out review data for business ids in pittsburgh
    with open(reviewJsonFileName, 'r') as f:
        for row in f:
            rowcnt = rowcnt + 1           
            if ast.literal_eval(row)["business_id"] in business_id:                
                data.append(row)
    
    #Write data to the file  
    for item in data:
        outfile.write(item)
    
    

