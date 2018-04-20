import json
import re
from fractions import Fraction
        
with open('clean_data_revised_names.json', 'r') as fr:
    data_dict = json.load(fr)
    
counter = 0
ings = set()

for drink in data_dict:
    drink_ings_list = data_dict[drink]
    for ingredient in drink_ings_list:
        ings.add(ingredient[0])

ings = sorted(ings)
print(len(ings))
data = json.dumps(ings, separators=(',\n', ": "))

with open('ingredients.json', 'w') as fr:
    fr.write(data)

##
##for drink in data_dict:
##    rip = False
##    drink_name = drink
##    drink_ings_list = data_dict[drink]
##    for ingredient in drink_ings_list:
##        ing_name = ingredient[0]
##        ing_amt = ingredient[1]
##        if "" is ing_amt:
##            rip = True
##           
##    if rip:
##        counter += 1
##print (counter)
