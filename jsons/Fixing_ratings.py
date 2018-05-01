import json

name_swaps = {}
with open('alcohol_ratings.json', 'r') as f:
    ratings_dict = json.load(f)

with open('drinks_data_no_weird_amts.json', 'r') as fr:
    data_dict = json.load(fr)

new_dict= {}
for drink in ratings_dict:
    if drink in data_dict:
        new_dict[drink] = ratings_dict[drink]
        
data = json.dumps(new_dict, indent=4, separators=(',', ': '))

with open("ratings.json", "w") as fw:
    fw.write(data)
