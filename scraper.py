import requests
from bs4 import BeautifulSoup


def validate_number(min, max):
    flag = True
    while flag:
        number = input("Podaj liczbe z zakresu: " + str(min) + " - " + str(max) + "\n")
        if number.isdigit():
            number = int(number)
            flag = False
        else:
            print("Wpisales niepoprawna wartosc ")
    return number


def pick_province():
    print("Wybierz województwo do przeszukania:\n"
          "1. Dolnośląskie\n"
          "2. Kujawsko-pomorskie\n"
          "3. Lubelskie\n"
          "4. Lubuskie\n"
          "5. Łódzkie\n"
          "6. Małopolskie\n"
          "7. Mazowieckie\n"
          "8. Opolskie\n"
          "9. Podkarpackie\n"
          "10. Podlaskie\n"
          "11. Pomorskie\n"
          "12. Śląskie\n"
          "13. Świętokrzyskie\n"
          "14. Warmińsko-mazurskie\n"
          "15. Wielkopolskie\n"
          "16. Zachodniopomorskie\n"
          "17. Cała polska")
    provinceNumber = validate_number(int(1), int(17))
    return provinceNumber


def pagesToScrap(url):
    page_check = requests.get(url)
    soup_page = BeautifulSoup(page_check.content, 'html.parser')
    links = soup_page.find(class_="pager")
    links = links.find_all('a', class_="")
    pages = []

    for x in range(0, len(links)):
        if links[x].text == "":
            continue
        else:
            pages.append(links[x].text)
    print("Ile stron chcesz sprawdzić? \n")
    numberOfPages = validate_number(int(1), int(pages[len(pages) - 1]))
    return numberOfPages


housePrice = []
houseArea = []
usableArea = []
URL = 'https://www.otodom.pl/sprzedaz/dom/?search%5Border%5D=created_at%3Adesc'
provinceNumber = pick_province()
if int(provinceNumber) != int(17):
    URL += "&search%5Bregion_id%5D=" + str(provinceNumber)

pagesToCheck = pagesToScrap(URL)
URL += "&page="

for x in range(1, pagesToCheck):
    url = URL
    url += str(x)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    offer = soup.find_all(class_="offer-item-price")
    area = soup.find_all(class_="offer-item-area")

    for offers in offer:
        if offers.text.replace(" ", "").replace("zł", "").replace("~", "").replace(",", ".").strip() == "Zapytajocenę":
            continue
        housePrice.append(offers.text.replace(" ", "").replace("zł", "").replace("~", "").replace(",", ".").strip())

    i = 1
    while i < len(area):
        if "działka" in area[i].text:
            usableArea.append(area[i].text.replace(" ", "").replace("m²", "").replace("działka", "").replace(",", "."))
        elif "m²" in area[i].text:
            houseArea.append(area[i].text.replace(" ", "").replace("m²", "").replace(",", "."))
        i += 1

priceTotal = 0.0
houseAreaTotal = 0.0
usableAreaTotal = 0.0

print("Wyszukanych ofert: " + str(len(housePrice)))

for prices in housePrice:
    priceTotal += float(prices)
avgPrice = priceTotal/len(housePrice)

for houseAreas in houseArea:
    houseAreaTotal += float(houseAreas)
houseAreaTotal = houseAreaTotal / len(houseArea)

for usableAreas in usableArea:
    usableAreaTotal += float(usableAreas)
usableAreaTotal = usableAreaTotal / len(usableArea)
pricePerSquaredMeter = avgPrice / len(housePrice)

print("Średnia powerzchnia mieszkan: " + format(houseAreaTotal, '.2f'))
print("Średnia powerzchnia działek: " + format(usableAreaTotal, '.2f'))
print("Średnia cena: " + format(avgPrice, '.2f') + " zł")
print("Całkowita suma w ogłoszeniach: " + str(priceTotal))
print("Średnia cena za m2: " + str(format(pricePerSquaredMeter, '.2f')))
