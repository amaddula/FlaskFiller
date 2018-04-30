from __future__ import print_function

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import json
import elbow
import analyzetfidf
import numpy as np
from collections import OrderedDict

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

num_clusters = 15

km = KMeans(n_clusters=num_clusters)

# %time km.fit(tfidf_matrix)
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

# from sklearn.externals import joblib

#uncomment the below to SAVE your model
#since I've already run my model I am loading from the pickle

joblib.dump(km,  'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

# films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters, 'genre': genres }
films = { 'title': titles, 'cluster': clusters}


frame = pd.DataFrame(films, index = [clusters] , columns = ['title', 'cluster'])

frame['cluster'].value_counts() #number of films per cluster (clusters from 0 to 4)

#grouped = frame['title'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

#grouped.mean() #average rank (1 to 100) per cluster

# from __future__ import print_function

print("Top terms per cluster:")
print()
# SORT cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')

    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() #add whitespace
    print() #add whitespace

    print("Cluster %d titles:" % i, end='')
    for title in frame.ix[i]['title'].values.tolist():
        print(' %s,' % title, end='')
    print() #add whitespace
    print() #add whitespace

print()
print()


# def ingr_to_string(drink_name):
#     data_dict = OrderedDict()
#     #opening drink dictionary
#     with open('drinks_data_no_weird_amts.json', 'r') as fr:
#         data_dict = json.load(fr)
#     this_drink = data_dict[drink_name]
#     doc_words = ""
#     for pair in this_drink:
#         doc_words = doc_words + " " + str(pair[0])
#     doc_words = doc_words.strip()
#     print(doc_words)
#     print(tokenize_only(doc_words))
#     return tokenize_only(doc_words)

def ingr_to_lst(ingr_list):
    doc_words = ""
    for word in ingr_list:
        doc_words = doc_words + " " + str(word)
    doc_words = doc_words.strip()
    print(doc_words)
    print(tokenize_only(doc_words))
    return tokenize_only(doc_words)

# def get_top_k_similar(ingr_list):
#     Y = vectorizer.transform(["chrome browser to open."])
#     prediction = model.predict(Y)
#     print(prediction)
def get_top_k_similar(ingr_lst, k):
    # Y = tfidf_vectorizer.transform(["apple cider apple juice"])
    tokens = ingr_to_lst(ingr_lst)
    Y = tfidf_vectorizer.transform(tokens)
    prediction = km.predict(Y)
    prediction = prediction[0]
    print(prediction)
    print(type(prediction))
    top_k = frame.ix[prediction]['title'].values.tolist()[0:k]
    print(top_k)
    top_k_utf = [item.lower().encode('utf-8') for item in top_k]
    print(top_k)
    return(top_k_utf)


# import os  # for os.path.basename
#
# import matplotlib.pyplot as plt
# import matplotlib as mpl
#
# from sklearn.manifold import MDS
#
# MDS()
#
# # convert two components as we're plotting points in a two-dimensional plane
# # "precomputed" because we provide a distance matrix
# # we will also specify `random_state` so the plot is reproducible.
# mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
#
# pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
#
# xs, ys = pos[:, 0], pos[:, 1]
# print()
# print()
#set up colors per clusters using a dict
# cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
#
# #set up cluster names using a dict
# cluster_names = {0: 'Family, HOME, war',
#                  1: 'Police, killed, murders',
#                  2: 'Father, New York, brothers',
#                  3: 'Dance, singing, love',
#                  4: 'Killed, soldiers, captain'}
#
# #some ipython magic to show the matplotlib plots inline
# #%matplotlib inline
# print("made it here?")
# #create data frame that has the result of the MDS plus the cluster numbers and titles
# df = pd.DataFrame(dict(x=[0,1,2,3,4,5,6,7,8,9,10], y=[0,1,2,3,4,5,6,7,8,9,10], label=clusters, title=titles))
#
# #group by cluster
# groups = df.groupby('label')
#
#
# # set up plot
# fig, ax = plt.subplots(figsize=(17, 9)) # set SIZE
# ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
#
# #iterate through groups to layer the plot
# #note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
# for name, group in groups:
#     ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
#             label=cluster_names[name], color=cluster_colors[name],
#             mec='none')
#     ax.set_aspect('auto')
#     ax.tick_params(\
#         axis= 'x',          # changes apply to the x-axis
#         which='both',      # both major and minor ticks are affected
#         bottom='off',      # ticks along the bottom edge are off
#         top='off',         # ticks along the top edge are off
#         labelbottom='off')
#     ax.tick_params(\
#         axis= 'y',         # changes apply to the y-axis
#         which='both',      # both major and minor ticks are affected
#         left='off',      # ticks along the bottom edge are off
#         top='off',         # ticks along the top edge are off
#         labelleft='off')
#
# ax.legend(numpoints=1)  #show legend with only 1 point
#
# #add label in x,y position with the label as the film title
# for i in range(len(df)):
#     ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], SIZE=8)
#
# print("got to plot")
#
# plt.show() #show the plot
# print("passed plot")
# #uncomment the below to SAVE the plot if need be
# #plt.savefig('clusters_small_noaxes.png', dpi=200)
