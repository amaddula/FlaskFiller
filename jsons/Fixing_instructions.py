import json

name_swaps = {}
with open('alcoholic_cocktails_webtender_mixing.json', 'r') as f:
    instructions_dict = json.load(f)

with open('drinks_data_no_weird_amts.json', 'r') as fr:
    data_dict = json.load(fr)

new_dict= {}
for drink in instructions_dict:
    if drink in data_dict:
        new_dict[drink] = instructions_dict[drink]
        
data = json.dumps(new_dict, indent=4, separators=(',', ': '))

with open("instructions.json", "w") as fw:
    fw.write(data)
