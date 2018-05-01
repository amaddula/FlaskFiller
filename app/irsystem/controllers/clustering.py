#is not useful here, meant to be used in clusterfuck folder to generate some dumps
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
# import clustering2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib

stopwords = nltk.corpus.stopwords.words('english')
print(stopwords[:10])

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

synopses = OrderedDict()
titles = OrderedDict()
#opening synopses
with open('ordered_ingredient_concat.json', 'r') as fr:
    synopses = json.load(fr)
#opening titles
with open('ordered_drinks.json', 'r') as fr:
    titles = json.load(fr)

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed

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


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopses:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)


vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

vocab_frame.to_pickle("vocab_frame.pickle")

# from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(#max_df=0.8,
                                   #max_features=200000,
                                   # min_df=0.1,
                                   stop_words='english',
                                   use_idf=True,
                                   tokenizer=tokenize_and_stem,
                                   ngram_range=(1,3)
                                   )

# %time tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses
tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses

#print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()
print(terms)
# terms_dump = json.dumps(terms, separators=(','))
# with open('terms_dump.json', 'w') as fr:
#     fr.write(terms_dump)
joblib.dump(terms,  'terms_dump.pkl')

# from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)
print
print


#### determine the optimal value of "k" ################ analyze the thing
# elbow.graph_elbow(tfidf_matrix)

#print((tfidf_matrix))
# Xtr = tfidf_matrix
# # vec = tfidf_vectorizer.named_steps['vec']
# features1 = terms
# print(analyzetfidf.top_feats_in_doc(Xtr, features1, 6, 500))


###########################################################################
# from sklearn.cluster import KMeans

num_clusters = 50

km = KMeans(n_clusters=num_clusters)

# %time km.fit(tfidf_matrix)
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

# from sklearn.externals import joblib

#uncomment the below to SAVE your model
#since I've already run my model I am loading from the pickle

joblib.dump(km,  'doc_cluster.pkl')
