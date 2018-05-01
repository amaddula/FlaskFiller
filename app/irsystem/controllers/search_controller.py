from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from collections import OrderedDict
import gen_jaccard_app
import alcohol_suggestions
import json
import math
import ratings
import clustering2
#import json_extraction


project_name = "Flask Filler"
net_id = "Jordan Stern (js2592), Anirudh Maddula (aam252), Diana Bank (dmb469)"

with open('ingredients.json', 'r') as fr:
    ingr = json.load(fr)

with open('drinks_data_no_weird_amts.json', 'r') as f:
    drinks_dict_utf = json.load(f)

with open('instructions.json', 'r') as fi:
    instructions_dict = json.load(fi)

with open('drinks_with_alcohol_content.json', 'r') as fa:
    alc_contents_dict = json.load(fa)

with open('ratings.json', 'r') as fs:
    ratings_dict = json.load(fs)

drinks_dict = {}
for drink in drinks_dict_utf:
    drink_name = drink.encode('ascii','ignore')
    recipe = []
    for ing in drinks_dict_utf[drink]:
        ing_name = ing[0].encode('ascii','ignore')
        ing_amt = ing[1].encode('ascii','ignore')
        recipe.append((ing_name, ing_amt))
    drinks_dict[drink_name] = recipe

instructions = {}
for drink in instructions_dict:
    drink_name = drink.encode('ascii','ignore')
    instructions[drink_name] = instructions_dict[drink]

alc_contents = {}
for drink in alc_contents_dict:
    drink_name = drink.encode('ascii','ignore')
    alc_contents[drink_name] = alc_contents_dict[drink]

ratingses = {}
for drink in ratings_dict:
    drink_name = drink.encode('ascii','ignore')
    ratingses[drink_name] = ratings_dict[drink]

ingredients = [item.lower().encode('utf-8') for item in ingr]
#print(ingredients)


@irsystem.route('/', methods=['GET'])
def search():

    query = request.args.get('search')
    query2 = request.args.get('but')
    query3 = request.args.get('switch')
    query4 = request.args.get('checkAlc')
    #'switch' in request.form

    print("~~~~~~~~~~~~~~~~")
    print(query3)
    if not query3:
        # if request.form.get('checkAlc'):
        #     #print("alc selected")

        if query4:
            alc_content = float(query2)/100
            alc = alc_content
        else:
            alc = 0
        #print(type(query))
        #query = query.decode('utf-8').lower()
        search_ing = []
        if not query:
            #print("Blank space baby")
            data = []
            output_message = ''
        else:
            query = query.lower()
            #print(query + "wasup")
            output_message = "Alcohol Content: " + str(query2) + "% | Ingredients: "
            ings = query.split(',')
            ings = [item.lstrip(' ') for item in ings]

            data = [] # change data to output list of drinks
            #search_ing = []
            for ing in ings:
                if str(ing) in ingredients:
                    #print(ing)
                    search_ing.append(ing)
            # for ing in search_ing:
            #     output_message += ing + ',  '
            for i in range(len(search_ing)):
                comma_ending = ""
                if i!=(len(search_ing)-1):
                    comma_ending = ", "
                output_message = output_message + str(search_ing[i].encode('ascii', 'ignore').title()) + comma_ending
            user_list = [x.lower() for x in search_ing]
            if len(user_list)==0:
                data=[]
            else:
                # inter = gen_jaccard_app.get_results(user_list)
                # inter1 = [x[1].encode('ascii', 'ignore') for x in inter[:15]]
                # ingrd1 = []
                # for drink in inter1:
                #     drnk_ings = drink_ingredients[drink]
                #     ingrd1.append(drnk_ings)
                # ingrd1 = [x[1].encode('ascii', 'ignore') for x in inter[:15]]
                # data = [inter1, ingrd1]
                # print(data)
                #print("data " + str(data))

                if query4:
                    jaccard_weight = 0.400
                    ratings_weight = 0.300
                    alc_content_weight = 0.300
                    content_results = alcohol_suggestions.get_results(alc_content, alc_content_weight)
                    jaccard_results = gen_jaccard_app.get_results(user_list, jaccard_weight)
                    rating_results = ratings.get_results(ratings_weight)
                    results_dict = {}
                    for drink in content_results:
                        results_dict[drink] = math.sqrt(jaccard_results[drink] + content_results[drink]) + rating_results[drink]

                else:
                    jaccard_weight = 0.6
                    ratings_weight = 0.4
                    jaccard_results = gen_jaccard_app.get_results(user_list, jaccard_weight)
                    rating_results = ratings.get_results(ratings_weight)
                    results_dict = {}
                    for drink in jaccard_results:
                        results_dict[drink] = math.sqrt(jaccard_results[drink]) + rating_results[drink]



                #print(len(content_results))
                #print(len(jaccard_results))

                inter = sorted(results_dict, key=lambda x:results_dict[x], reverse=True)
                results = []
                results_mixing = []
                for drink in inter[:15]:
                    name = drink.encode('ascii', 'ignore')
                    ingredients_list = drinks_dict[drink]
                    mixing_instructions = instructions[drink]
                    content_percent = round(alc_contents[drink]*100)
                    top_few_drinks = clustering2.get_top_k_similar(name, 10)
                    drink_rating = ratingses[name]["rating"]
                    results.append([name, ingredients_list, mixing_instructions, content_percent, top_few_drinks, drink_rating])
                for i in inter[:20]:
                    print(i + str(results_dict[i]))
                data = (results)
    else:
        drink = query.encode('ascii', 'ignore')
        #print (drink)
        ingredients_list = drinks_dict[drink]
        #print(ingredients_list)
        mixing_instructions = instructions[drink]
        content_percent = round(alc_contents[drink]*100)
        top_few_drinks = clustering2.get_top_k_similar(drink, 10)
        drink_rating = ratingses[drink]["rating"]
        output_message = ""
        alc = ""
        data = [[drink, ingredients_list, mixing_instructions, content_percent, top_few_drinks, drink_rating]]


            #we need to add a section into "data" that will call clustering to get the top few similar drinks
            #might wanna do this in gen jaccard, or do another loop here where you append to each list, we'll decide later
            #will return a list of the top k drinks
            #top_k_drinks = clustering2.get_top_k_similar(drink_name, top_k)

    return render_template('search.html', name=project_name, netid=net_id, alc=alc, output_message=output_message, data=data, ingr=json.dumps(ingr))
