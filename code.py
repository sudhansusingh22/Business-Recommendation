from gensim import corpora, models
from nltk.corpus import stopwords
import json
import re
import pandas as pd
import ijson
from pandas import *

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
    df1 = df[["business_id","name","city"]]
    df2 = df1[df1.city == "Las Vegas"]
    #print df2
    #print df1[df1.business_id == 'Ts4xsKPU7FNPPZRj-nRjIg']
    business_id = df2['business_id'].tolist()
    #print df2[df2.business_id == 'Ts4xsKPU7FNPPZRj-nRjIg']
    # print business_id

    # reviewJsonFileName = "newfile.json"
    reviewJsonFileName = "yelp_academic_dataset_review.json"
    
    finalReviewJsonFile = "review_json_file.json"
    outfile = open (finalReviewJsonFile,"w")
    #data = []
    with open(reviewJsonFileName, 'r') as f:
        for row in f:
            if any(bus in row for bus in business_id):      
                    json.dump(row,outfile)
                    outfile.write('\n')
    good_columns = ['business_id', 'text','stars']
    # df = pd.DataFrame([convert(line) for line in file(reviewJsonFileName)])
    # print df
 #    stoplist = stopwords.words('english')
 #    originalFile = open('yelp_academic_dataset_review.json',"rw+")
 #    newFile = open("newfile.json","rw+")
 #    for line in originalFile:
 #        if '"business_id": "Ts4xsKPU7FNPPZRj-nRjIg"' in line:
 #            newFile.write(line)
 #    originalFile.close()
 #    newFile.close()
 #    yelp = MyCorpus('newfile.json', stoplist, 10000)
 #    K = 5
 #    for i in  yelp.dictionary:
	# print yelp.dictionary[i]
 #    #lda = models.ldamodel.LdaModel(corpus = yelp, id2word = yelp.dictionary, num_topics = K, update_every = 1, chunksize = 100000, passes = 3)
 #    print 'done'
 #    print lda.show_topics(K, formatted=True)
    
 #    lda.save("ldapy")