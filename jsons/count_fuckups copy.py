import json
from fractions import Fraction
with open('cossim_decimals.json', 'r') as fr:
    data_dict = json.load(fr)

new_data_dict = {}
for drink in data_dict:
    drink_name = drink
    drink_ings_list = data_dict[drink]
    recipe = []
    norm = 0
    for ingredient in drink_ings_list:
        ing_amt = ingredient[1]
        ing_name = ingredient[0]
        norm += ing_amt
        recipe.append([ing_name, ing_amt])
    for i in range(len(recipe)):
        recipe[i][1] /= norm
    new_data_dict[drink_name] = recipe

print(len(new_data_dict))
data = json.dumps(new_data_dict, indent=4, separators=(',', ': '))
with open("gen_jaccard_normed.json", "w") as fw:
    fw.write(data)

