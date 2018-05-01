import json
import re
from fractions import Fraction
        
with open('alcoholic_cocktails_webtender_mixing.json', 'r') as fr:
    instructions_dict = json.load(fr)
with open('drinks_data_no_weird_amts.json', 'r') as f:
    data_dict = json.load(f)


for drink in instructions_dict:
    print(drink)

##data = json.dumps(ings, separators=(',\n', ": "))
##
##with open('ingredients.json', 'w') as fr:
##    fr.write(data)

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
