import json
import re
from fractions import Fraction
        
with open('clean_data.json', 'r') as fr:
    data_dict = json.load(fr)

    
def check_if_decimal(num):
    if "." in num:
        return True
    return False

def go_through_list(drink_ings_list):
    for ingredient in drink_ings_list:
        ing_name = ingredient[0]
        ing_amt = ingredient[1]
        if 'oz' in ing_amt.lower():
            ing_amt = re.sub("[^0-9./ ]", "", ing_amt).strip()
            if check_if_decimal(ing_amt):
                frac = Fraction(float(ing_amt)).limit_denominator(4)
                num = frac.numerator
                denom = frac.denominator
                if num > denom and ((num % denom) != 0):
                    ing_amt = str(num // denom) + " " + str(num % denom) + "/" + str(denom)
                else:
                    ing_amt = frac
            ingredient[1] = str(ing_amt) +" oz"

for drink in data_dict:
    drink_name = drink
    drink_ings_list = data_dict[drink]
    try:
        go_through_list(drink_ings_list)
    except:
        print ("Failed on: " + drink)
        
data = json.dumps(data_dict, indent=4, separators=(',', ': '))
with open("clean_data_fractions.json", "w") as fw:
    fw.write(data)
