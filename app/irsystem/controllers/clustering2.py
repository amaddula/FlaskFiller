from __future__ import print_function

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
# import mpld3
import json
# import analyzetfidf
import numpy as np
from collections import OrderedDict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib

num_clusters = 50
######################################################################################################
synopses = OrderedDict()
#opening synopses
with open('ordered_ingredient_concat.json', 'r') as fr:
    synopses = json.load(fr)

titles = OrderedDict()
with open('ordered_drinks.json', 'r') as fr:
    titles = json.load(fr)

# with open('terms_dump.json', 'r') as fr:
#     terms = json.load(fr)

terms = joblib.load('terms_dump.pkl')
#######################################################################################################
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

# films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters, 'genre': genres }
films = { 'title': titles, 'cluster': clusters}

vocab_frame = pd.read_pickle('vocab_frame.pickle')
frame = pd.DataFrame(films, index = [clusters] , columns = ['title', 'cluster'])

frame['cluster'].value_counts() #number of films per cluster (clusters from 0 to 4)
print(frame['cluster'].value_counts())
#grouped = frame['title'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

#grouped.mean() #average rank (1 to 100) per cluster

# from __future__ import print_function

###############################################################################
stopwords = nltk.corpus.stopwords.words('english')
print(stopwords[:10])

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


tfidf_vectorizer = TfidfVectorizer(#max_df=0.8,
                                   #max_features=200000,
                                   # min_df=0.1,
                                   stop_words='english',
                                   use_idf=True,
                                   tokenizer=tokenize_and_stem,
                                   ngram_range=(1,3)
                                   )
tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses

##############################################################################


print("Top terms per cluster:")
print()
# SORT cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

# for i in range(num_clusters):
#     print("Cluster %d words:" % i, end='')
#
#     for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
#         print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
#     print() #add whitespace
#     print() #add whitespace
#
#     print("Cluster %d titles:" % i, end='')
#     for title in frame.ix[i]['title'].values.tolist():
#         print(' %s,' % title, end='')
#     print() #add whitespace
#     print() #add whitespace

print("ending terms per cluster ##############################################")
print()

print("#######################################################################")
#print(frame.ix)
# print(frame.ix[0])
# print(frame.ix[0]['title'].values)
# print(frame.ix[0]['title'].values.tolist())

def ingr_to_string(drink_name):
    data_dict = OrderedDict()
    #opening drink dictionary
    with open('drinks_data_no_weird_amts.json', 'r') as fr:
        data_dict = json.load(fr)
    this_drink = data_dict[drink_name]
    print(this_drink)
    doc_words = ""
    for pair in this_drink:
        doc_words = doc_words + " " + (pair[0]).lower().encode('ascii', 'ignore')
    doc_words = doc_words.strip()
    print(doc_words)
    return [doc_words]

# def ingr_to_string(ingr_list):
#     doc_words = ""
#     for word in ingr_list:
#         doc_words = doc_words + " " + str(word).lower()
#     doc_words = doc_words.strip()
#     print(doc_words)
#     return [doc_words]

# def get_top_k_similar(ingr_list):
#     Y = vectorizer.transform(["chrome browser to open."])
#     prediction = model.predict(Y)
#     print(prediction)
def get_top_k_similar(drink_name, k):
    # Y = tfidf_vectorizer.transform(["apple", "cider", "apple", "juice"])
    ings_as_string = ingr_to_string(drink_name)
    print(ings_as_string)
    Y = tfidf_vectorizer.transform(ings_as_string)
    prediction = km.predict(Y)
    prediction = prediction[0]
    print("predicted cluster: " + str(prediction))
    top_k = frame.ix[prediction]['title'].values.tolist()[0:k]
    #print(top_k)
    top_k_utf = [item.encode('utf-8') for item in top_k]
    print(top_k_utf)
    return(top_k_utf)
