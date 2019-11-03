import json
import os

import requests
from bs4 import BeautifulSoup as bs


BASE_URL = "https://www.senado.cl"
DATA = {}
OUTPUT_PATH = os.path.join("..", "data", "senadores.json")


# Send request and extract elements
req = requests.post(f"{BASE_URL}/appsenado/templates/senadores/regiones_2018.html")
soup = bs(req.text, "html5lib")
container = soup.find("div", {"class": "mtabs"})

# Iterate elements inside container and extract structure and content
elements = container.find_all("div")
for element in elements:
    if element.get("id") == "mtabinfo":
        continue
    # First group with region information
    circumscription = element.hgroup.h1.get_text()
    region = element.hgroup.h2.get_text()
    region_capital = element.hgroup.h3.get_text()
    DATA[region] = {
        "circunscripcion": circumscription,
        "capital": region_capital,
    }
    print(f"Circunscripción: {circumscription}")
    print(f"Región: {region}")
    print(f"Capital regional: {region_capital}")
    # Second group with senators information
    senators = []
    print("Senadores:")
    for senator in element.find_all("td"):
        # Skip element if does not contain a senator information
        if not senator.find("h1"):
            continue
        name = senator.h1.get_text()
        senator_href = senator.a["href"]
        senator_data = {
            "nombre": name,
            "url_img": BASE_URL + senator.img["src"],
            "url_senador": BASE_URL + senator_href,
        }
        senators.append(senator_data)
        print(f"* {name}")
    DATA[region]["senadores"] = senators

    print()

# Store data in its own JSON file
with open(OUTPUT_PATH, "w", encoding="utf-8") as senatores_file:
    json.dump(DATA, senatores_file,
              sort_keys=True, indent=4,
              separators=(',', ': '), ensure_ascii=False,
              )
