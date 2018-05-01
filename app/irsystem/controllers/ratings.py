import json
import math

def get_results(weight):
    avg_rating = 6.774448767833966
    avg_weight = 53.06658019887592
    with open('ratings.json', 'r') as fr:
        drinks_ratings_dict = json.load(fr)
    scores = {}
    max_weight = 0
    for drink in drinks_ratings_dict:
        drinks_ratings = drinks_ratings_dict[drink]
        rating = drinks_ratings["rating"]
        weighting = drinks_ratings["weight"]
        delta_rating = rating - avg_rating
        if weighting == 0:
            new_rating = 0
        else:
            delta_weight = weighting/avg_weight
            new_rating = delta_rating * abs(1 + math.log(delta_weight))/100
        score = new_rating*weight
        scores[drink.encode('ascii', 'ignore')] = score
    return scores

d = get_results(1)
r= sorted(d, key=lambda x:d[x], reverse=True)
results = []
for i in r:
    results.append((i, d[i]))
print(results[:10])

