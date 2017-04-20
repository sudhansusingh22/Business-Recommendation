# Business Recommendation using Topic-Modelling on Yelp Data Set

## Objective : 
* Based on Yelp Data Set of User Reviews for Restaurants. Business value for this project are:
   * To provide recommendation on topics a Business Owner can improve in their restaurant.
   * To provide recommendation on topics for a new Restaurant.
* This project involved parsing raw customer reviews data with python's NLTK tokenizing words, POS tagging, filtering out only NN, NNS (noun singular/plurals) and removing stop words .
* Created Corpus documents with tokenized words 
* Apply LDA algorithm on the documents and create a set of topics and the distribution of words in them. 
* Predict new topics based on trained model.

## Requirements:
* MongoDB
* nltk
* gensim
* Yelp Data Set
* Python

## Steps to Run:
* Data Transformation : Load Bussiness Data from File to Pandas Dataframe
```python
python transform.py
```
* Filter Data: filter review and business ids based on certain location
```python
python filter_reviews.py
```
* Data Processing : Tokenize and lemmatize
```python
python processing.py
```
* Train Model :Train LDA model with corpus documents
```python
python training.py
```
## Results:
* Topics predcited for "Pittsburg" as location:
```json
(0, u'0.150*sandwich + 0.053*bread + 0.034*meat + 0.030*place + 0.019*eat + 0.015*flavor + 0.014*try + 0.014*paper + 0.013*steak + 0.012*day')
(1, u'0.083*time + 0.082*place + 0.031*fish + 0.028*pittsburgh + 0.027*service + 0.026*friend + 0.024*area + 0.020*gem + 0.019*year + 0.017*mozzarella')
(2, u'0.053*music + 0.037*night + 0.032*place + 0.029*floor + 0.023*saturday + 0.020*crowd + 0.019*people + 0.018*conversation + 0.016*cafe + 0.013*hip')
(3, u'0.189*pork + 0.025*tequila + 0.021*medium + 0.021*warm + 0.015*meat + 0.014*church + 0.014*difference + 0.011*thing + 0.011*entrance + 0.011*chef')
(4, u'0.081*strip + 0.055*steak + 0.049*seafood + 0.028*value + 0.028*joint + 0.019*pre + 0.019*disappoint + 0.019*desert + 0.018*point + 0.018*recommendation')
(5, u'0.204*burger + 0.027*bun + 0.022*place + 0.022*onion + 0.021*mussel + 0.017*product + 0.014*menu + 0.012*medium + 0.012*burgatory + 0.011*time')
```
