import json
import os

import requests
from bs4 import BeautifulSoup as bs


BASE_URL = "https://www.cdch.cl"
DATA = {}
OUTPUT_PATH = os.path.join("..", "data", "concejales.json")


# Send request and extract elements
req = requests.post(f"{BASE_URL}/concejales-de-chile.aspx")
soup = bs(req.text, "html5lib")
container = soup.find("div", {"class": "containerCDC"})

# Iterate elements inside container and extract structure and content
elements = container.find_all("div", recursive=False)
current_region = None
for element in elements:
    if element.h3:
        # If element is <h3>, contains the region name
        current_region = element.h3.get_text()
        DATA[current_region] = []
        print(f"Región: {current_region}")
    for commune_councilors in element.find_all("ul"):
        # First group with commune information
        commune_name = commune_councilors.parent.a.get_text().strip().title()
        commune_href = commune_councilors.parent.a["href"]
        print(f"Comuna: {commune_name}")
        # Second group with councilors information
        councilors = []
        print("Concejales:")
        for councilor in commune_councilors.find_all("li"):
            name = councilor.get_text()
            councilor_href = councilor.a["href"]
            councilor_data = {
                "nombre": name,
                "url_concejal": BASE_URL + councilor_href,
            }
            councilors.append(councilor_data)
            print(f"* {name}")
        # Store commune details in its corresponding region
        DATA[current_region].append({
            "comuna": commune_name,
            "url_comuna": BASE_URL + commune_href,
            "concejales": councilors,
        })
        print()

    print()
    print()

# Store data in its own JSON file
with open(OUTPUT_PATH, "w", encoding="utf-8") as councilors_file:
    json.dump(DATA, councilors_file,
              sort_keys=True, indent=4,
              separators=(',', ': '), ensure_ascii=False,
              )
