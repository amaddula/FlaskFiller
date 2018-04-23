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


with open('ingredients_alccontents.json', 'r') as fr:
    ingredients = json.load(fr)

count_undone = 0
for key in ingredients:
    if ingredients[key] == -1:
        count_undone += 1

print (count_undone)
