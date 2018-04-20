import json
import re

with open('clean_data.json', 'r') as fr:
    data_dict = json.load(fr)

new_dict = {}

'''
    CONVERSION FACTORS:
    1 part = 1.5 oz
    1 centiliter (cl) = 0.33814 oz
    1 shot = 1.5 oz
'''

for cock in data_dict:
    recipe = []

    for ingredient in data_dict[cock]:

        ing = ingredient[1].encode('utf-8')
        ing = str(ing)
        ing = " ".join(ing.split())
        
        amt = re.findall(r"[-+]?\d*\.\d+|\d+", ing)
        amt = [float(s) for s in amt]

        val = 0

        if(len(amt) == 0): 
            recipe.append(ingredient)
            continue

        elif len(amt) == 1: val = amt[0]
        elif len(amt) == 2: val = amt[0] / amt[1]
        elif len(amt) == 3: val = amt[0] + (amt[1] / amt[2])
        

        if "part" in ingredient[1]:

            val *= 1.5
            recipe.append([ingredient[0], str(val) + " oz"])

        elif "cl" in ingredient[1]:

            val *= 0.33814
            recipe.append([ingredient[0], str(val) + " oz"])

        elif "shot" in ingredient[1]:

            val *= 1.5
            recipe.append([ingredient[0], str(val) + " oz"])

        elif " L" in ingredient[1]:
            val *= 33.814
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "ml" in ingredient[1]:
            val *= 0.033814
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "tsp" in ingredient[1]:
            val /= 8
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "tblsp" in ingredient[1]:
                        val *= 0.5
                        recipe.append([ingredient[0], str(val) + " oz"])
        elif "pint" in ingredient[1]:
            val *= 16
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "cup" in ingredient[1]:
            val *= 8
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "glass" in ingredient[1]:
            val *= 8
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "can" in ingredient[1]:
            val *= 12
            recipe.append([ingredient[0], str(val) + " oz"])
        elif "jigger" in ingredient[1]:
            val *= 1.5
            recipe.append([ingredient[0], str(val) + " oz"])
        
        else:
            recipe.append(ingredient)

    new_dict[cock] = recipe

data = json.dumps(new_dict, indent=4, separators=(',', ': '))
with open("clean_data.json", "w") as fw:
    fw.write(data)


