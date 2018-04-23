import json
from fractions import Fraction
with open('drinks_data_no_weird_amts.json', 'r') as fr:
    data_dict = json.load(fr)

new_data_dict = {}
for drink in data_dict:
    drink_name = drink
    drink_ings_list = data_dict[drink]
    recipe = []
    for ingredient in drink_ings_list:
        ing_name = ingredient[0]
        recipe.append(ing_name)
    new_data_dict[drink_name] = recipe

print(len(new_data_dict))
data = json.dumps(new_data_dict, indent=4, separators=(',', ': '))
with open("cossim_no_amts.json", "w") as fw:
    fw.write(data)

