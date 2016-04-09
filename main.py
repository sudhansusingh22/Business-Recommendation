'''
Created on Apr 8, 2016

@author: BI Team 23 NCSU
'''
'''
# -*- coding: utf-8 -*-
"""Convert the Yelp Dataset Challenge dataset from json format to csv.
For more information on the Yelp Dataset Challenge please visit http://yelp.com/dataset_challenge
"""
import argparse
import collections
import csv
import simplejson as json


def read_and_write_file(json_file_path, csv_file_path, column_names):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    with open(csv_file_path, 'wb+') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(column_names))
        with open(json_file_path) as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow(get_row(line_contents, column_names))

def get_superset_of_column_names_from_file(json_file_path):
    """Read in the json dataset file and return the superset of column names."""
    column_names = set()
    with open(json_file_path) as fin:
        for line in fin:
            line_contents = json.loads(line)
            column_names.update(
                    set(get_column_names(line_contents).keys())
                    )
    return column_names

def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names given a dict.
    Example:
        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        
        
        will return: ['a.b', 'a.c']
    These will be the column names for the eventual csv file.
    """
    column_names = []
    for k, v in line_contents.iteritems():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            column_names.extend(
                    get_column_names(v, column_name).items()
                    )
        else:
            column_names.append((column_name, v))
    return dict(column_names)

def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.
    
    Example:
        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'
        will return: 2
    
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )
        if isinstance(line_value, unicode):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    parser = argparse.ArgumentParser(
            description='Convert Yelp Dataset Challenge data from JSON format to CSV.',
            )

    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert.',
            )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = '{0}.csv'.format(json_file.split('.json')[0])

    column_names = get_superset_of_column_names_from_file(json_file)
    read_and_write_file(json_file, csv_file, column_names)
'''  

import json
import pandas as pd
from glob import glob

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

    
from gensim import corpora, models
from nltk.corpus import stopwords
import json
import re
class MyCorpus(object):
    def __init__(self, fname, stopf = None, V = None):
        self.fname = fname
        self.file = open(fname, "r")
        stoplist = stopf
        #print "make dictionary started"
        self.dictionary = self.make_dict(stoplist, V)
    def reset(self):
        self.file.seek(0)
    def proc(self, line):
        return filter(lambda x: len(x) > 2, map(lambda x: x.strip(), re.sub(r'[0-9]+|\W',' ',line.strip().lower()).split()))
    def make_dict(self, stoplist = [], V = None):
        self.reset()
        # read all terms
        #print "Corpora.Dictionary"
        dictionary = corpora.Dictionary(self.proc(line) for line in self.read_file())
        # remove stop words
        stop_ids = [dictionary.token2id[sw] for sw in stoplist if sw in dictionary.token2id]
        dictionary.filter_tokens(stop_ids)
        # remove words which occur in less than 5 documents or more than 50% of documents
        dictionary.filter_extremes(keep_n = V)
        #print "Corpora.Dictionary end"
        return dictionary
    def read_file(self):
        #print "read_file"
        for line in self.file:
                txt = json.loads(line)["text"]
                if len(txt) > 5: yield txt
    
    def __iter__(self):
        #print "iter"
        self.reset()
        for line in self.read_file():
            bow = self.dictionary.doc2bow(self.proc(line))
            if len(bow) >= 5: yield bow

if __name__ == '__main__':
    stoplist = stopwords.words('english')
    originalFile = open('yelp_academic_dataset_review.json',"rw+")
    json_new_filename = "newfile.json"
    newFile = open(json_new_filename,"rw+")
    for line in originalFile:
        if '"business_id": "Ts4xsKPU7FNPPZRj-nRjIg"' in line:
            newFile.write(line)
    originalFile.close()
    newFile.close()
    df = pd.DataFrame([convert(line) for line in file(json_new_filename)])
    yelp = MyCorpus('newfile.json', stoplist, 10000)
    K = 5
    lda = models.ldamodel.LdaModel(corpus = yelp, id2word = yelp.dictionary, num_topics = K, update_every = 1, chunksize = 100000, passes = 3)
    #print 'done'
    print lda.show_topics(K, formatted=True)
    
    lda.save("ldapy")