import json
from collections import OrderedDict

##with open('ingredients.json', 'r') as fr:
##    ingredients = json.load(fr)
##ingredients = sorted(ingredients)
##alc_contents = OrderedDict()
##for i in ingredients:
##    alc_contents[i] = -1

##
##with open('ingredients_alccontents.json', 'w') as fw:
##    data = json.dumps(alc_contents, indent=4, separators=(',', ': '))
##    fw.write(data)

##
with open('ingredients.json', 'r') as fr:
    ingredients = json.load(fr)
with open('ingredients_alccontents.json', 'r') as f:
    ingredients_alcs = json.load(f)
##
##count_undone = 0
##for key in ingredients:
##    if ingredients[key] == -1:
##        count_undone += 1
##
##print (count_undone)

##with open("webtender_ingredients_alcohol_content.json", 'r') as f:
##    alc_contents = json.load(f)
##
##new_data = {}
##count = 0
##for ing in alc_contents:
##    if ing in ingredients:
##        if ingredients[ing] == -1:
##            new_data[ing] = alc_contents[ing]
##        else:
##            new_data[ing] = ingredients[ing]
##
##with open('ingredients_alccontents.json', 'w') as fw:
##    data = json.dumps(new_data, indent=4, separators=(',', ': '))
##    fw.write(data)

##for ing in ingredients:
##    amt = ingredients[ing]
##    if type(amt) is str:
##        if "%" in amt: 
##            new_amt = float(ingredients[ing].split("%")[0])/100.0
##            ingredients[ing] = new_amt
##            print(ing)
##            print(new_amt)
##        elif "Non alcoholic" in amt:
##            ingredients[ing] = 0
##
##with open('ingredients_alccontents.json', 'w') as fw:
##    data = json.dumps(ingredients, indent=4, separators=(',', ': '))
##    fw.write(data)

new_data = {}
for ing in ingredients_alcs:
    if ing in ingredients:
        new_data[ing] = ingredients_alcs[ing]
sorteddic = sorted(new_data.keys(), key=lambda x:x)
sorteddict = OrderedDict()
for key in sorteddic:
    sorteddict[key] = new_data[key]


with open('ingredients_alccontents_relevant.json', 'w') as fw:
    data = json.dumps(sorteddict, indent=4, separators=(',', ': '))
    fw.write(data)
