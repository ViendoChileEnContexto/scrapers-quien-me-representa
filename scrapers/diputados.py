import json
import os
import re

import requests
from bs4 import BeautifulSoup as bs


BASE_URL = "https://www.camara.cl"
DATA = {}
OUTPUT_PATH = os.path.join("..", "data", "diputados.json")


for region in range(1, 16):
    # Send request and extract container element
    params = {"prmTAB": "distritos", "prmPARAM": region}
    req = requests.post(f"{BASE_URL}/camara/diputados.aspx", params=params)
    soup = bs(req.text, "html5lib")
    container = soup.find(id="ctl00_mainPlaceHolder_pnlDetalleDistritos")

    # Iterate elements inside container and extract structure and content
    elements = list(container.children)
    current_region = None
    while elements:
        # Retrieve next element to process
        element = elements.pop(0)
        # Different information is contained in different tags
        if element.name == "h2":
            # If element is <h2>, contains the region name
            current_region = element.get_text(strip=True)
            DATA[current_region] = []  # Each region contains its districts
            print(f"Región: {current_region}")
        elif element.name == "h3":
            # If element is <h3>, contains the district number
            district = element.get_text(strip=True)
            district = district.split("\n")[-1].strip()
            DATA[current_region].append({})
            # Use -1 to access most recent district
            DATA[current_region][-1]["distrito"] = district
            DATA[current_region][-1]["url_region"] = req.url
            print(f"Distrito: {district}")
        elif element.name == "h4":
            # If element is <h4>, contains the district communes
            communes = element.get_text(strip=True)
            communes = communes.split("\n")[-1].strip()
            communes = re.split(r"\s*,\s*", communes)
            # Use -1 to access most recent district
            DATA[current_region][-1]["comunas"] = communes
            print(f"Comunas: {', '.join(communes)}")
        elif element.name == "ul":
            # If element is <ul>, contains the list of deputies
            deputies = []
            print("Diputados:")
            for deputy in element.find_all("li"):
                name = deputy.h4.get_text(strip=True)
                name = name.split("\n")[-1].strip().title()
                party = deputy.p.get_text(strip=True)
                deputy_href = deputy.h4.a["href"].partition("#")[0]
                party_href = deputy.p.a["href"].partition("#")[0]
                deputy_data = {
                    "nombre": name,
                    "partido": party,
                    "url_img": BASE_URL + deputy.img["src"],
                    "url_diputado": BASE_URL + "/camara/" + deputy_href,
                    "url_partido": BASE_URL + "/camara/" + party_href,
                }
                deputies.append(deputy_data)
                print(f"* {name} ({party})")
            # Use -1 to access most recent district
            DATA[current_region][-1]["diputados"] = deputies

    print()

# Store data in its own JSON file
with open(OUTPUT_PATH, "w", encoding="utf-8") as deputies_file:
    json.dump(DATA, deputies_file,
              sort_keys=True, indent=4,
              separators=(',', ': '), ensure_ascii=False,
              )
