import pickle
import numpy as np
#import os

#print(os.listdir(os.getcwd()))
#print(os.getcwd())

#unpickle the data structs
ingr_list = pickle.load( open("ingr_lst_pickle.p", "rb" ))
drink_ingr = pickle.load( open( "drink_ingr_pickle.p", "rb" ))
drink_list = pickle.load( open( "drink_dic_pickle.p", "rb" ))
#mixing_instr = pickle.load( open( "mixing_instructions.p", "rb" ))

#clean the unicode off
ingr_list = [x.lower().encode('utf-8') for x in ingr_list]

# new_mix = {}
# for k,v in mixing_instr.items():
#     new_mix[k.encode('utf-8').lower] = v.encode('utf-8')
# mixing_instr = new_mix
#print(mixing_instr)

drink_list_new = {}
for k,v in drink_list.items():
	drink_name = k.lower().encode('utf-8')
	recipe = []
	for tup in v:
		ing_name = tup[0].lower().encode('utf-8')
		ing_amt = tup[1].lower().encode('utf-8')
		recipe.append([ing_name, ing_amt])
	drink_list_new[drink_name] = recipe
drink_list = drink_list_new

#create helper methods and arrays
ingr_to_num = {}
i=0
for ingr in ingr_list:
    ingr_to_num[ingr] = i
    i=i+1

drink_to_num = {}
num_to_drink = {}
j=0
for k,v in drink_list.items():
    drink_to_num[k] = j
    num_to_drink[j] = k
    j=j+1

def drink_to_index(dr):
    return drink_to_num[dr]
def index_to_drink(num):
    return num_to_drink[num]

def ingredient_to_index(ingredient_str):
    return ingr_to_num[ingredient_str.lower()]
def number_list_of_drinks(ing_str_lst):
    newlst = []
    for ingr in ing_str_lst:
        newlst.append(ingredient_to_index(ingr))
    return newlst

def get_ingredients_for_drink(drink_num, drink_lst):
    #print(drink_num)
    curr_ingredients = drink_lst[index_to_drink(drink_num).lower()]
    final = []
    for ing in curr_ingredients:
        final.append(ingredient_to_index(ing[0]))
    return final

#returns a numpy array of 1 by size of drink_list. each entry is the jaccard similarity between the user input and drink
def drink_jaccard_sim(user_ingredients_lst):
    #print(drink_lst)
    drink_lst = drink_list
    final_mat = np.zeros(len(drink_lst))
    #cat1 will be the user set. It should just have a list of numbers that correspond to drinks
    cat1 = set(number_list_of_drinks(user_ingredients_lst))
    for i in range(len(drink_lst)):
        #cat2 will be the ingredients of each individual drink
        cat2 = set(get_ingredients_for_drink(i, drink_lst))
        #do the jaccard
        intersect = len(set.intersection(cat1, cat2))
        union = len(set.union(cat1, cat2))
        final_mat[i] = intersect/(union+1)
    #print(np.sum(final_mat))
    return final_mat

# def get_mixing_instructions(drink_name):
#     return mixing_instr[drink_name]

def get_top_k_drinks(lst, k):
    #lst should have a list of ranked values, just need to do an argsort for the best ones
    sorted_lst = lst.argsort()[-k:][::-1]
    #print(sorted_lst)
    top_drinks = []
    for drink_num in sorted_lst:
        #stuff = get_ingredients_for_drink(drink_num, drink_list)
        stuff2 = drink_list[index_to_drink(drink_num).lower()]
        #mix = get_mixing_instructions(index_to_drink(drink_num))
        top_drinks.append([index_to_drink(drink_num), lst[drink_num], stuff2])
    #print(top_drinks)
    return top_drinks

#thing = get_top_k_drinks(sim_lst, 10)
#print(thing)
