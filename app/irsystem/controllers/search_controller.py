from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import gen_jaccard_app
import json
#import json_extraction


project_name = "Flask Filler"
net_id = ""
with open('ingredients.json', 'r') as fr:
        ingr = json.load(fr)

ingredients = [item.lower().encode('utf-8') for item in ingr]
#print(ingredients)

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    query2 = request.args.get('but')
    print(query2)
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
            if ing in ingredients:
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
            inter = gen_jaccard_app.get_results(user_list)
            data = [x[1].encode('ascii', 'ignore') for x in inter[:15]]
            #print("data " + str(data))

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
