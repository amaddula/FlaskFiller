import json

name_swaps = {}
with open('name_swaps.json', 'r', encoding='utf-8') as f:
    for line in f:
        k, v = line.strip().split(':')
        name_swaps[k.strip()] = v.strip().strip("")

def replace_names(): 
    with open('clean_data_fractions.json', 'r') as fr:
        data_dict = json.load(fr)

    counter = 0
    for drink in data_dict:
        drink_name = drink
        drink_ings_list = data_dict[drink]
        for ingredient in drink_ings_list:
            ing_name = ingredient[0]
            if ing_name in name_swaps:
                new_ing_name = name_swaps[ing_name]
                counter += 1
            else: new_ing_name = ing_name
            
            ingredient[0] = new_ing_name
    print(str(counter) + " swaps")
            
    data = json.dumps(data_dict, indent=4, separators=(',', ': '))
    with open("clean_data_revised_names.json", "w") as fw:
        fw.write(data)

def update_ingredients_list():
    with open('clean_data_revised_names.json', 'r') as fr:
        data_dict = json.load(fr)
        
    counter = 0
    ings = set()

    for drink in data_dict:
        drink_ings_list = data_dict[drink]
        for ingredient in drink_ings_list:
            ings.add(ingredient[0])

    ings = sorted(ings)
    data = json.dumps(ings, separators=('\n', ": "))
    
    print(str(len(ings)) + " ingredients")
    
    with open('ingredients.json', 'w') as fr:
        fr.write(data)
        
replace_names()
update_ingredients_list()
