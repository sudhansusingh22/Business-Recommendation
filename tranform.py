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
    
    # dfFiltered = df.ix[:,['business_id','text','stars']]
    # print dfFiltered
    businessJsonFileName = "yelp_academic_dataset_business.json"
    df = pd.DataFrame([convert(line) for line in file(businessJsonFileName)])
    df1 = df[["business_id","name","city",'categories']]
    df2 = df1[df1.city == "Phoenix"]
    df2 = df2[df2['categories'].str.contains("Restaurant")]
    print df2[:10]
    #print df1[df1.business_id == 'Ts4xsKPU7FNPPZRj-nRjIg']
    business_id = df2['business_id'].tolist()
    #print df2[df2.business_id == 'Ts4xsKPU7FNPPZRj-nRjIg']
    # print business_id
    # reviewJsonFileName = "newfile.json"
    business_id = set(business_id)
    reviewJsonFileName = "yelp_academic_dataset_review.json"
    
    finalReviewJsonFile = "review_json_file_phoenix_restaurant.json"
    outfile = open (finalReviewJsonFile,"w")
    data = []
    rowcnt = 0
    with open(reviewJsonFileName, 'r') as f:
        for row in f:
            rowcnt = rowcnt + 1
            # print rowcnt
            #print row["business_id"]
            #print bus
            if ast.literal_eval(row)["business_id"] in business_id:
                # print row
                data.append(row)
        # print data

    for item in data:
        outfile.write(item)
    
    

