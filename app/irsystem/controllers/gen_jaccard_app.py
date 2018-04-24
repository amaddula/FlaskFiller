import json
from collections import OrderedDict
from collections import Counter
import math
import numpy as np

n_drinks = 2314
ids_names = OrderedDict()

def build_inverted_index(drinks_dict):
    inverted_index = OrderedDict()
    for drink in drinks_dict:
        drink_name = drink
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
        for drink in index[ing.lower()]:
            relevant.add(drink)
    return relevant

def tf(ing, drink, drinks_dict):
    for tup in drinks_dict[drink]:
        if ing == tup[0].lower():
            return tup[1]
    return 0

def gen_jaccard_index_search (query, relevant, drinks_dict, weight):
    query_tf = 1.0/(len(query))
    results_dict = {}
    drinks_scores = {}
    for drink in drinks_dict:
        if drink in relevant:
            relevant_ings = set(query)
            sum_min = 0.0
            sum_max = 0.0

            for tup in drinks_dict[drink]:
                ingredient = tup[0].lower()
                temp_tf = tf(ingredient, drink, drinks_dict)
                relevant_ings.add(ingredient)
            for ing in relevant_ings:
                if ing in query:
                    query_vec = query_tf
                else:
                    query_vec = 0

                temp_tf = tf(ing, drink, drinks_dict)
                sum_min += min(query_vec, temp_tf)
                sum_max += max(query_vec, temp_tf)
                similarity = sum_min/sum_max
            score = similarity * weight
        else: score = 0
        results_dict[drink.encode('ascii', 'ignore')] = score
    return results_dict

def get_results(query, weight):
    with open('gen_jaccard_normed.json', 'r') as fr:
        drinks_dict = json.load(fr)
    inv_idx = build_inverted_index(drinks_dict)
    rel = sorted(find_relevant(query, inv_idx))
    results_dict = gen_jaccard_index_search(query, rel, drinks_dict, weight)
##    sorted_drinks = sorted(results_dict, key=lambda x:results_dict[x], reverse=True)
    # for drink in results_dict:
    #     results[drink] = results_dict[drink]*weight
##        results.append([results_dict[drink]*weight, drink])
    print(len(results_dict))
    return results_dict
