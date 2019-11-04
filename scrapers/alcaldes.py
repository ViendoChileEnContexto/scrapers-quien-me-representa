import json
import os

import requests
from bs4 import BeautifulSoup as bs


BASE_URL = "http://datos.sinim.gov.cl"
DATA = {}
OUTPUT_PATH = os.path.join("..", "data", "alcaldes.json")


# Send request and extract elements
req = requests.get(f"{BASE_URL}/ficha_comunal.php")
soup = bs(req.text, "html5lib")
container = soup.find("select", id="municipio")

# Iterate elements inside container and request content and its structure
for element in container.find_all("option"):
    if not element["value"]:
        continue
    # Request each commune information
    commune, value = element.get_text().split(" - ")
    DATA[commune] = {}
    print(f"Comuna: {commune} ({value})")
    commune_req = requests.post(
        f"{BASE_URL}/ficha_comunal.php",
        data={"municipio": value},
    )
    commune_soup = bs(commune_req.text, "html5lib")
    authorities = commune_soup.find("div", id="tab-autoridades")

    # Mayor information
    mayor_image = authorities.find("div", {"class": "img_alcalde"}).img["src"]
    mayor_container = authorities.find("div", {"class": "nombre_alcalde"})
    mayor_name = mayor_container.h3.get_text()
    mayor_party = mayor_container.find_all("h4")[-1].get_text()
    print(f"Alcalde: {mayor_name} ({mayor_party}) [{mayor_image}]")

    # Councilors information
    councilors = []
    print("Concejales:")
    councilors_container = authorities.find("div", {"class": "despliegue_wrap"})
    for councilor in councilors_container.find_all("div", {"class": "file"}):
        councilor_name = councilor.find("div", {"class": "col_nom"}).get_text()
        councilor_party = councilor.find("div", {"class": "col_partido"}).get_text()
        councilor_data = {
            "nombre": councilor_name,
            "partido": councilor_party
        }
        councilors.append(councilor_data)
        print(f"* {councilor_name} ({councilor_party})")

    more_authorities = authorities.find_all("div", {"class": "info_box"})

    # Senators information
    senators = []
    senators_container = more_authorities.pop(0)
    senators_circumscription = senators_container.h4.get_text()[10:]
    print(f"Senadores ({senators_circumscription}):")
    for senator in senators_container.find_all("p"):
        senator_name, senator_party = senator.get_text().split(" - ", 1)
        senator_data = {
            "nombre": senator_name,
            "partido": senator_party,
        }
        senators.append(senator_data)
        print(f"* {senator_name} ({senator_party})")

    # Deputies information
    deputies = []
    deputies_container = more_authorities.pop(0)
    deputies_district = deputies_container.h4.get_text()[10:]
    print(f"Diputados ({deputies_district}):")
    for deputy in deputies_container.find_all("p"):
        deputy_name, deputy_party = deputy.get_text().split(" - ", 1)
        deputy_data = {
            "nombre": deputy_name,
            "partido": deputy_party,
        }
        deputies.append(deputy_data)
        print(f"* {deputy_name} ({deputy_party})")

    # Regional mayor information
    regional_mayor_container = more_authorities.pop(0)
    regional_mayor_region = regional_mayor_container.h4.get_text()[21:]
    regional_mayor_name = regional_mayor_container.p.get_text()
    print(f"Intendente ({regional_mayor_region}): {regional_mayor_name}")

    # Governor information
    governor_container = more_authorities.pop(0)
    governor_province = governor_container.h4.get_text()[24:]
    governor_name = governor_container.p.get_text()
    print(f"Gobernador ({governor_province}): {governor_name}")

    # Regional councilors information
    cores = []
    cores_container = more_authorities.pop(0)
    cores_area = cores_container.h4.get_text()[6:]
    print(f"COREs ({cores_area}):")
    for core in cores_container.find_all("p"):
        core_name, core_party = core.get_text().split(" - ", 1)
        core_data = {
            "nombre": core_name,
            "partido": core_party,
        }
        cores.append(core_data)
        print(f"* {core_name} ({core_party})")

    # Store data in output dictionary
    DATA[commune] = {
        # Mayor
        "alcalde": {
            "nombre": mayor_name,
            "partido": mayor_party,
            "url_img": mayor_image,
        },
        # Councilors
        "concejales": councilors,
        # Senators
        "circunscripcion": senators_circumscription,
        "senadores": senators,
        # Deputies
        "distrito": deputies_district,
        "diputados": deputies,
        # Regional mayor
        "region": regional_mayor_region,
        "intendente": regional_mayor_name,
        # Governor
        "provincia": governor_province,
        "gobernador": governor_name,
        # Regional councilors
        "area": cores_area,
        "cores": cores,
    }
    print()


# Store data in its own JSON file
with open(OUTPUT_PATH, "w", encoding="utf-8") as mayor_file:
    json.dump(DATA, mayor_file,
              sort_keys=True, indent=4,
              separators=(',', ': '), ensure_ascii=False,
              )
