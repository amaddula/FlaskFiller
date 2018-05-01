import json
from collections import OrderedDict

with open('ingredients.json', 'r') as fr:
    ingredients = json.load(fr)
ingredients = sorted(ingredients)
alc_contents = OrderedDict()
for i in ingredients:
    alc_contents[i] = -1


with open('ingredients_alccontents.json', 'w') as fw:
    data = json.dumps(alc_contents, indent=4, separators=(',', ': '))
    fw.write(data)


