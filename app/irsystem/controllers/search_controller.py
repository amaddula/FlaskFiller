from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from collections import OrderedDict
import gen_jaccard_app
import alcohol_suggestions
import json
import math
import clustering2
#import json_extraction


project_name = "Flask Filler"
net_id = "Jordan Stern (js2592), Anirudh Maddula (aam252), Diana Bank (dmb469)"

with open('ingredients.json', 'r') as fr:
    ingr = json.load(fr)

with open('drinks_data_no_weird_amts.json', 'r') as f:
    drinks_dict_utf = json.load(f)

drinks_dict = {}
for drink in drinks_dict_utf:
    drink_name = drink.encode('ascii','ignore')
    recipe = []
    for ing in drinks_dict_utf[drink]:
        ing_name = ing[0].encode('ascii','ignore')
        ing_amt = ing[1].encode('ascii','ignore')
        recipe.append((ing_name, ing_amt))
    drinks_dict[drink_name] = recipe

ingredients = [item.lower().encode('utf-8') for item in ingr]
#print(ingredients)

# def alc(data):
#     for i in range(len(data)):




@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    query2 = request.args.get('but')

    # if request.form.get('checkAlc'):
    #     #print("alc selected")

    try:
        alc_content = float(query2)/100
        alc = query2
    except:
        alc_content = 0.0
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
            if not (alc_content > 0):
                jaccard_weight = 0.1
                alc_content_weight = 0.9
            else:
                jaccard_weight = 0.666
                alc_content_weight = 0.334

            content_results = alcohol_suggestions.get_results(alc_content, alc_content_weight)
            jaccard_results = gen_jaccard_app.get_results(user_list, jaccard_weight)
            results_dict = {}
            #print(len(content_results))
            #print(len(jaccard_results))
            for drink in content_results:
                results_dict[drink] = math.sqrt(jaccard_results[drink] + content_results[drink])

            inter = sorted(results_dict, key=lambda x:results_dict[x], reverse=True)
            results = []
            for drink in inter[:15]:
                results.append((drink, drinks_dict[drink]))
            # for i in inter[:20]:
            #     print(i + str(results_dict[i]))
            data = results
            #print(data)

            #we need to add a section into "data" that will call clustering to get the top few similar drinks
            #might wanna do this in gen jaccard, or do another loop here where you append to each list, we'll decide later
            #will return a list of the top k drinks
            #top_k_drinks = clustering2.get_top_k_similar(drink_name, top_k)
    return render_template('search.html', name=project_name, netid=net_id, alc=alc, output_message=output_message, data=data, ingr=json.dumps(ingr))
