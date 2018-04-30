import re
import requests 
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BS

last_drink_number = 6217

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0', 'Accept-Encoding': 'identity'}
base_url = "https://www.webtender.com/db/drink/"

drinks_dict = {}

def getSoup(url):
    html = requests.post(url, headers=headers)
    soup = BS(html.content, "html.parser")
    return soup

for i in range(last_drink_number):
    try:
        URL_new = base_url + str(i+1)
        soup = getSoup(URL_new)
        rating_mess = soup.findAll("small")[7].get_text().split("<b>")[0].replace("\xa0", "").split("-")
        try:
            rating = float(rating_mess[0])
            weight = int(rating_mess[1].strip().split(" ")[0])
        except:
            rating = 0.0
            weight = 0
        title = soup.find().find("h1").get_text()
        drinks_dict[title] = {"rating": rating, "weight": weight}
    except:
        print("Failed on" + str(i+1))

import json
data = json.dumps(drinks_dict, indent=4, separators=(',', ': '))
with open("alcohol_ratings.json", "w") as f:
    f.write(data)
