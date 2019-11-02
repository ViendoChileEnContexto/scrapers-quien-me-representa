import requests
from bs4 import BeautifulSoup as bs


req = requests.get(f"http://datos.sinim.gov.cl/ficha_comunal.php")
soup = bs(req.text, "html5lib")
detalle = soup.find("select", {"id": "municipio"})

for option in detalle.find_all("option"):
    if option["value"]:
        municipio, codigo = option.get_text().split(" - ")
        req_ = requests.post(
            f"http://datos.sinim.gov.cl/ficha_comunal.php",
            data={"municipio": codigo}
        )
        soup_ = bs(req_.text, "html5lib")
        autoridades = soup_.find("div", {"id": "tab-autoridades"})
        alcalde = autoridades.find("div", {"class": "nombre_alcalde"}).h3.get_text()
        concejales = list(map(lambda c: c.get_text(), autoridades.find_all("div", {"class": "col_nom"})))[1:]
        print(municipio, alcalde, concejales)
        for info_box in autoridades.find_all("div", {"class": "info_box"}):
            categoria = info_box.h4.get_text().title()
            miembros = list(
                map(lambda m: m.get_text(), info_box.find_all("p")))
            print(f"{categoria}: {miembros}")
        print()
