import requests
from bs4 import BeautifulSoup as bs


req = requests.post(f"https://www.senado.cl/appsenado/templates/senadores/regiones_2018.html")
soup = bs(req.text, "html.parser")
detalle = soup.find("div", {"class": "mtabs"})

RIDS = [
	"mtabrm" if i == 13
	else f"mtab{i}"
	for i in range(1, 16)
]

s = 0
for rid in RIDS:
	tab = detalle.find("div", {"id": rid})
	hgroup = tab.hgroup
	print(hgroup.h1.get_text())
	print(hgroup.h2.get_text())
	print(hgroup.h3.get_text())
	for td in tab.find_all("td"):
		if not td.find("h1"):
			continue
		s += 1
		print(">", td.h1.get_text().split("\n")[0])
		print(">>", td.img["src"])
		print(">>", td.a["href"])
	print()
print(f"Información de {s} senadores")
