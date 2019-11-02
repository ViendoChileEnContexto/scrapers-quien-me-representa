import requests
from bs4 import BeautifulSoup as bs


req = requests.post(f"https://www.cdch.cl/concejales-de-chile.aspx")
soup = bs(req.text, "html5lib")
detalle = soup.find("div", {"class": "containerCDC"})

for div in detalle.find_all("div"):
    h3 = div.h3
    if h3:
        print(h3.get_text().upper())
    for ul in div.find_all("ul"):
        a = ul.parent.div.a
        print(a.get_text().title().strip())
        for li in ul.find_all("li"):
            print("*", li.get_text().title())
        print()
