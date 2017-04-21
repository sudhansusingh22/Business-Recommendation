# Business Recommendation using Topic-Modelling on Yelp Data Set

## Objective : 
* Based on Yelp Data Set of User Reviews for Restaurants. Business value for this project are:
   * To provide recommendation on topics a Business Owner can improve in their restaurant.
   * To provide recommendation on topics for a new Restaurant.
* This project involved parsing raw customer reviews data with python's NLTK tokenizing words, POS tagging, filtering out only NN, NNS (noun singular/plurals) and removing stop words .
* Created Corpus documents with tokenized words 
* Apply LDA algorithm on the documents and create a set of topics and the distribution of words in them. 
* Predict new topics based on trained model.

#### Dataset

1.	Please download and extract Yelp Dataset Challenge data, yelp_dataset_challenge_academic_dataset from the following link: [Yelp Data Set](https://www.yelp.com/dataset_challenge)
2.	Put this data dolder in the dataset folder in the same directory as Topic_Modelling.
![alt text](https://github.com/sudhansusingh22/Business-Recommendation/blob/master/folder.png)
3.	Install MongoDB in your system from the following link : Install MongoDB
4.	Download the MongoDB data files from the following google drive link: MongoDB
5.	Put this folder in `/var/lib`
![alt text](https://github.com/sudhansusingh22/Business-Recommendation/blob/master/unix.png) 	

#### Python Packages:
Python packages to be installed for running the program:

1.	Gensim
2.	Nltk
3.	Pandas
4.	Numpy
5.	Matplotlib
6.	Scipy
7.	pymongo

#### File Information:

Relevant File Informations:

1.	`__init__.py`   - To treat the current directory as package.
2.	`db_objects.py` - Factory class to return database collections.
3.	`filter_review.py` - Filters the reviews from JSON file and stores into MongoDB REVIEW collections.
4.	`make_json_serializable.py` - Creates serializable JSON objects from the MongoDB collection to write JSON data to JSON file.
5.	`processing.py` - Processes the reviews by tokenizing, removing stop words, lemmatizing and POS tagging and stores it into MongoDB CORPUS collection.
6.	`settings.py` - Contains database constants, connection strings, collection names, CORPUS disctionary object names.
7.	 `show_db_information.py` - Displays the database names currently present in the MongoDB database, collections present and collection objects informations.
8.	`training.py` - Creates CORPUS documents and train the LDA Model with documents as input.
9.	`klDivergence.py` - Creates KL Divergence graph to find out optimal number of topics for LDA.


#### Project Setup:

1.	We have filtered out review data based on  “Pittsburgh” city (total 61849 reviews after filtering) and trained our LDA model on this data. It took a total of 7.91 Hrs to preprocess (tokenization, removing stop words, lemmatizing,POS tagging) the reviews on running 4 processes on 4 different cores on Dell, Intel i5 processor.
2.	The review data are present in the REVIEWS_COLLECTION, while the corpus document data are present in the CORPUS_COLLECTION.


#### Steps To Run:

1.	Run `transform.py` file to extract the reviews data for pittsburgh area into a new json file(`review_json_file_pittsburgh_restaurant.json`).
2.	Run `kldivergence.py` to plot the symmetric KL divergence vs number of topic to find the optimal number of topics for LDA.
3.	Run `training.py` to train the LDA model and populate the optimal number of topics found by KL Divergence method in the previous step.
4.	 Run `display.py` to check the results based on business ID provided.


#### Project WorkFlow:
![alt text](https://github.com/sudhansusingh22/Business-Recommendation/blob/master/flow.jpg) 
 

#### Results:

The topics that would be output from the program
```json
(0, u'0.093*pizza + 0.023*sauce + 0.015*slice + 0.015*place + 0.014*salad + 0.014*tomato + 0.013*cheese + 0.012*crust + 0.012*delivery + 0.012*bread')
(1, u'0.017*meal + 0.016*restaurant + 0.015*dinner + 0.014*flavor + 0.014*dessert + 0.013*menu + 0.011*plate + 0.011*pork + 0.011*meat + 0.010*potato')
(2, u'0.031*taco + 0.023*place + 0.021*breakfast + 0.020*coffee + 0.019*egg + 0.019*chip + 0.018*brunch + 0.010*time + 0.009*potato + 0.009*day')
(3, u'0.037*place + 0.026*time + 0.022*order + 0.021*burger + 0.012*sandwich + 0.012*don + 0.012*lunch + 0.011*fry + 0.011*service + 0.010*people')
(4, u'0.029*place + 0.026*chicken + 0.021*restaurant + 0.019*soup + 0.018*spicy + 0.016*rice + 0.016*roll + 0.013*sushi + 0.013*sauce + 0.013*service')
(5, u'0.036*place + 0.030*bar + 0.024*beer + 0.022*service + 0.021*time + 0.018*night + 0.013*drink + 0.013*restaurant + 0.012*selection + 0.012*menu')
```

This can be summarised as the following chart:
![alt text](https://github.com/sudhansusingh22/Business-Recommendation/blob/master/chart.png) 

The following  table shows  the average rating for the topics of business id -  
```
SsGNAc9U-aKPZccnaDtFkA
```
![alt text](https://github.com/sudhansusingh22/Business-Recommendation/blob/master/table.PNG) 

The above results infer that the restaurant needs to improve on `Breakfast`.

#### References:

1.	http://mlwave.com/tutorial-online-lda-with-vowpal-wabbit/
2.	http://xmodulo.com/how-to-find-number-of-cpu-cores-on.html
3.	http://stackoverflow.com/questions/20886565/python-using-multiprocessing-process-with-a-maximum-number-of-simultaneous-pro
    
* LDA Algorithm Explanation:
1.	http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
2.	https://wellecks.wordpress.com/2014/09/03/these-are-your-tweets-on-lda-part-i/
3.	http://stackoverflow.com/questions/10624760/latent-dirichlet-allocation-solution-example
4.	http://obphio.us/pdfs/lda_tutorial.pdf
5.	http://www.vladsandulescu.com/topic-prediction-lda-user-reviews/
6.	https://www.quora.com/What-is-a-good-explanation-of-Latent-Dirichlet-Allocation


