import json
from collections import OrderedDict

def get_results(amt, weight):
    with open('drinks_with_alcohol_content.json', 'r') as fr:
        drinks_alcs = json.load(fr)
    scores = {}
    for drink in drinks_alcs:
        score = (1-abs(drinks_alcs[drink] - amt)) * weight
        scores[drink.encode('ascii', 'ignore')]= score
    return scores
