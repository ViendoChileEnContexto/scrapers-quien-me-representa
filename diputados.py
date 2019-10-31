import requests
from bs4 import BeautifulSoup as bs


for i in range(1, 16):
    req = requests.post(f"https://www.camara.cl/camara/diputados.aspx?prmTAB=distritos&prmPARAM={i}")
    soup = bs(req.text, "html.parser")
    detalle = soup.find("div", {"id": "ctl00_mainPlaceHolder_pnlDetalleDistritos"})

    contenidos = list(detalle.children)
    while len(contenidos) > 0:
        hijo = contenidos.pop(0)
        if hijo.name == "h2":
            print(f"La región es: {hijo.get_text().strip()}")
        if hijo.name == "h3":
            distrito = hijo.get_text().strip().split('\n')[-1].strip()
            print(f"El distrito es: {distrito}")
        if hijo.name == "h4":
            comunas = hijo.get_text().strip().split(
                '\n')[-1].strip().split(",")
            print(f"Las comunas son: {comunas}")
        if hijo.name == "ul":
            for diputado in hijo.find_all("li"):
                nombre = " ".join(diputado.h4.find("a").get_text().replace(
                    "\r", "").replace("\n", "").split()).title()
                partido = " ".join(diputado.p.find(
                    "a").get_text().split("\n")).strip()
                print(f"{nombre} ({partido})")
    print()
