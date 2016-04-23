"""
This file is used to train the LDA model with corpus documents
"""

import gensim
from gensim.corpora import BleiCorpus
from gensim import corpora

from settings import Settings
from Topic_Modelling.db_objects import DBCollections, Constants


class Corpus(object):
    def __init__(self, cursor, reviews_dictionary, corpus_path):
        self.cursor = cursor
        self.reviews_dictionary = reviews_dictionary
        self.corpus_path = corpus_path

    def __iter__(self):
        self.cursor.rewind()
        for review in self.cursor:
            yield self.reviews_dictionary.doc2bow(review["words"])

    def serialize(self):
        BleiCorpus.serialize(self.corpus_path, self, id2word=self.reviews_dictionary)

        return self


class Dictionary(object):
    def __init__(self, cursor, dictionary_path):
        self.cursor = cursor
        self.dictionary_path = dictionary_path

    def build(self):
        self.cursor.rewind()
        dictionary = corpora.Dictionary(review["words"] for review in self.cursor)
        dictionary.filter_extremes(keep_n=10000)
        dictionary.compactify()
        corpora.Dictionary.save(dictionary, self.dictionary_path)

        return dictionary


class Train:
    def __init__(self):
        pass

    @staticmethod
    def run(lda_model_path, corpus_path, num_topics, id2word):
        corpus = corpora.BleiCorpus(corpus_path)
        lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=id2word, passes=10)
        lda.save(lda_model_path)

        return lda


def main():
    DBCollections.start_logging()
    dictionary_path = Settings.Dictionary_path
    corpus_path = Settings.Corpus_path
    lda_num_topics = Settings.Lda_num_topics
    lda_model_path = Settings.Lda_model_path

    corpus_collection = DBCollections.get_collection(Constants.CORPUS)
    reviews_cursor = corpus_collection.find()

    dictionary = Dictionary(reviews_cursor, dictionary_path).build()
    Corpus(reviews_cursor, dictionary, corpus_path).serialize()
    Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)


if __name__ == '__main__':
    main()
