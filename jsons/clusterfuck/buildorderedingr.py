from collections import OrderedDict
import json

# data_dict = OrderedDict()

with open('drinks_data_no_weird_amts.json', 'r') as fr:
    data_dict = json.load(fr)

# ingredients = [item.lower().encode('utf-8') for item in ingr]

print(data_dict)

documents = []
ordered_drinks_lst = []
for k,v in data_dict.items():
    ordered_drinks_lst.append(k)
    doc_words = ""
    for pair in v:
        doc_words = doc_words + " " + str(pair[0])
    doc_words = doc_words.strip()
    documents.append(doc_words)

print(documents)
print(ordered_drinks_lst)

data = json.dumps(documents, separators=(',\n', ": "))
data2 = json.dumps(ordered_drinks_lst, separators=(',\n'))

# print(data)
# print(data2)
with open('ordered_ingredient_concat.json', 'w') as fr:
    fr.write(data)
with open('ordered_drinks.json', 'w') as fr:
    fr.write(data2)
