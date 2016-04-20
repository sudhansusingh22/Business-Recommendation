class Settings:
    def __init__(self):
        pass

    DATASET_FILE = '../dataset/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
    MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
    REVIEWS_DATABASE = "Dataset_Challenge_Reviews"
    TAGS_DATABASE = "Tags"
    REVIEWS_COLLECTION = "Reviews"
    CORPUS_COLLECTION = "Corpus"
    BUSINESS_COLLECTION = 'Business'
    BUSINESS_DATA_FILE = '../dataset/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
    Dictionary_path = "models/dictionary.dict"
    Corpus_path = "models/corpus.lda-c"
    Lda_num_topics = 60
    Lda_model_path = "models/lda_model_50_topics.lda"
    REVIEWS_COLLECTION_BKP = "Reviews_Bkp"
    CORPUS_COLLECTION_BKP = "Corpus_Bkp"
    CORPUS_COLLECTION_PITTSBURG = "Corpus_Pits"

