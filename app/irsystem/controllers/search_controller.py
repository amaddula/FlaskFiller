from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from collections import OrderedDict
import gen_jaccard_app
import alcohol_suggestions
import json
#import json_extraction


project_name = "Flask Filler"
net_id = "Anirudh Maddula (aam252), Jordan Stern (js2592), Diana Bank (dmb469)"

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

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    query2 = request.args.get('but')
    try:
        alc_content = float(query2)/100
    except: alc_content = 0.0
    #print(type(query))
    #query = query.decode('utf-8').lower()
    search_ing = []
    if not query:
        print("Blank space baby")
        data = []
        output_message = ''
    else:
        query = query.lower()
        print(query + "wasup")
        output_message = "ingredients: "
        ings = query.split(',')
        ings = [item.lstrip(' ') for item in ings]

        data = [] # change data to output list of drinks
        #search_ing = []
        for ing in ings:
            if str(ing) in ingredients:
                print(ing)
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
            print(len(content_results))
            print(len(jaccard_results))
            for drink in content_results:
                results_dict[drink] = jaccard_results[drink] + content_results[drink]

            inter = sorted(results_dict, key=lambda x:results_dict[x], reverse=True)
            results = []
            for drink in inter[:15]:
                results.append((drink, drinks_dict[drink]))
            data = results

        #drink_list = [x.encode('ascii', 'ignore') for x in search_ing]

        # ranked_list = helpers.drink_jaccard_sim(user_list)
        # #ranked_list = json_extraction.drink_jaccard_sim(user_list)
        # for i in range(10):
        #   print(ranked_list[i])

        #data=(helpers.get_top_k_drinks(ranked_list, 10))
        #data= json_extraction.get_top_k_drinks(ranked_list, 10)
        #data = [('Pineberry', 0.3333333333333333), ('CT', 0.3333333333333333), ("Tinyee's Orange Smoothie", 0.25), ('Fruit Cooler', 0.25), ("Laura's Surprise", 0.25), ('Hennyville Slugger', 0.2222222222222222), ('Belfast Bomber', 0.2222222222222222)]
        #data = [('Ice Pick #2', 0.3333333333333333), ('Christer Petterson', 0.3333333333333333), ('The Vaitkus', 0.3333333333333333), ('Naked Navel', 0.3333333333333333), ('Purple Cow', 0.3333333333333333), ('Zimartini', 0.3333333333333333), ('Frisky Witch', 0.3333333333333333), ('Vodka Russian', 0.3333333333333333), ('Copperhead', 0.3333333333333333), ('Ersh', 0.3333333333333333)]
        #data = [('Caribbean Orange Liqueur', 0.75), ('Saurian Brandy', 0.6), ('Stockholm "75"', 0.5), ('The Power of Milk', 0.4), ('Piggelin #1', 0.4), ('Top Banana', 0.4), ('Lemon Shooters', 0.4), ('St. Petersburg', 0.4), ('Sjarsk', 0.4), ('Raspberry Cordial', 0.4)]
        #data = [('Pine-Sol Shooter', 0.0), ('Black Army', 0.0), ('Cactus Juice', 0.0), ('Tidal Wave', 0.0), ('Drunk Watermelon', 0.0), ('The Seminole', 0.0), ('Dr. Pepper #1', 0.0), ('Pixie Stick', 0.0), ('Candy Corn #2', 0.0), ('Dark and Stormy #2', 0.0)]
        #print(data)
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, ingr=json.dumps(ingr))
