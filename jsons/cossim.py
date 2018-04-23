import json
from collections import defaultdict
from collections import Counter
import math
import numpy as np

with open('cossim_decimals.json', 'r') as fr:
    drinks_dict = json.load(fr)

n_drinks = 2314
ids_names = {}
def build_inverted_index(drinks_dict):
    inverted_index = defaultdict()
    id_counter = 0
    for drink in drinks_dict:
        drink_name = drink
        ids_names[id_counter] = drink_name
        drink_ings_list = drinks_dict[drink_name]
        for ingredient in drink_ings_list:
            ing_name = ingredient[0]
            ing_amt = ingredient[1]
            if ing_name in inverted_index:
                inverted_index[ing_name].append((id_counter, ing_amt))
            else:
                inverted_index[ing_name] = [(id_counter, ing_amt)]
            id_counter += 1
    return inverted_index, 

def compute_idf(inv_idx, n_drinks):
    idf = defaultdict()
    for key in inv_idx:
        print (key)
        num_docs_key = len(inv_idx[key])
        idf[key] = math.log((n_drinks/(1.0+num_docs_key)), 2)
    return idf

def compute_drink_norms(index, idf, n_drinks):
    norms = np.zeros(n_drinks)
    for ingredient in index:
        if ingredient in idf:
            for tup in index[ingredient]:
                print(tup)
                norms[tup[0]] += np.power((tup[1] * idf[ingredient]), 2)
    return np.sqrt(norms)

def index_search(query, index, idf, doc_norms):
    q = query
    q_norm = 0.0
    results = []
    drink_scores = {}
    for ing in q:
        if ing in idf:
            q = idf[ing]
            q_norm += np.power(q,2)
            for tup in index[ing]:
                d = idf[ing] * tup[1]
                if tup[0] in drink_scores:
                    drink_scores[tup[0]] += d * q
                else:
                    drink_scores[tup[0]] = d * q
    q_norm = math.sqrt(q_norm)
    for drink_id in drink_scores:
        drink_scores[drink_id] /= (q_norm*drink_scores[drink_id])
    sorted_drinks = sorted(drink_scores, key=lambda x:drink_scores[x], reverse=True)
    for drink in sorted_drinks:
        results.append((drink_scores[drink], drink))
    return results[:10]

query1 = ["Bailey's irish cream", "7-Up"]

inv_idx = build_inverted_index(drinks_dict)
idf = compute_idf(inv_idx, n_drinks)
##drink_norms = compute_drink_norms(inv_idx, idf, n_drinks)
##results = index_search(query1, inv_idx, idf, drink_norms)


##data = json.dumps(new_data_dict, indent=4, separators=(',', ': '))
##with open("cossim_no_amts.json", "w") as fw:
##    fw.write(data)

