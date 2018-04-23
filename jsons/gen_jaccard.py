import json
from collections import OrderedDict
from collections import Counter
import math
import numpy as np



n_drinks = 2314
ids_names = OrderedDict()

def build_inverted_index(drinks_dict):
    inverted_index = OrderedDict()
    id_counter = 0
    for drink in drinks_dict:
        drink_name = drink
        ids_names[id_counter] = drink_name
        drink_ings_list = drinks_dict[drink_name]
        for ingredient in drink_ings_list:
            ing_name = ingredient[0].lower()
            ing_amt = ingredient[1]
            if ing_name in inverted_index:
                inverted_index[ing_name].append(drink_name)
            else:
                inverted_index[ing_name] = [drink_name]
    return inverted_index

def find_relevant(query,index):
    relevant = set()
    for ing in query:
        for drink in index[ing]:
            relevant.add(drink)
    return relevant

def tf(ing, drink):
    for tup in drinks_dict[drink]:
        if ing.lower() == tup[0].lower():
            return tup[1]
    return 0

def gen_jaccard_index_search (query, relevant, drinks_dict):
    query_tf = 1.0/(len(query))
    results_dict = {}
    drinks_scores = {}
    for drink in relevant:
        sum_min = 0
        sum_max = 0
        for ingredient in drinks_dict[drink]:
            sum_min += min(query_tf, tf(ingredient, drink))
            sum_max += max(query_tf, tf(ingredient, drink))
        for ingredient in query:
            sum_min += min(query_tf, tf(ingredient, drink))
            sum_max += max(query_tf, tf(ingredient, drink))
        similarity = sum_min/sum_max
        results_dict[drink] = similarity
    return results_dict

def get_results(query):
    with open('gen_jaccard_normed.json', 'r') as fr:
        drinks_dict = json.load(fr)
    inv_idx = build_inverted_index(drinks_dict)
    rel = sorted(find_relevant(query, inv_idx))
    results_dict = gen_jaccard_index_search(query, rel, drinks_dict)
    results = []
    sorted_drinks = sorted(results_dict, key=lambda x:results_dict[x], reverse=True)
    for drink in sorted_drinks[:10]:
        results.append((results_dict[drink], drink))
    return results
