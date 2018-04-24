import json
from collections import OrderedDict

with open('drinks_with_alcohol_content.json', 'r') as fr:
    data_dict = json.load(fr)

d = sorted(data_dict.items(), key=lambda x:x[1], reverse=True)
