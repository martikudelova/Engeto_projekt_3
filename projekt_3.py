"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Martina Kudelova
email: marti.kudelova@gmail.com
discord: martina_44769
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys

def preved_na_int(value):
    """Převede text na celé číslo, nebo vrátí 0, pokud není převod možný."""
    value = value.strip().replace("\xa0", "")  # Odstraní mezery
    try:
        return int(value)
    except ValueError:
        return 0

def ziskej_data(odkaz, zakladni_odkaz):
    """Získá data k obcím."""
    data_odpoved = get(odkaz)
    data_parsovane = bs(data_odpoved.text, features="html.parser")
    pocet_volicu, obalky, platne, hlasy = 0, 0, 0, {}
    if "Okrsek" in data_parsovane.find("tr").text: # Zjistí, jestli stránka obsahuje tabulku se seznamem okrsků
        if data_parsovane.find("tr") is None:
            return (0, 0, 0, {})
        okrsky = data_parsovane.find_all("td")
        odkazy_okrsku = []
        for zaznam in okrsky: # Vytvoří seznam odkazů na okrsky
            castecny_odkaz = zaznam.find("a")
            if castecny_odkaz:
                odkaz_okrsku = zakladni_odkaz + castecny_odkaz["href"]
                odkazy_okrsku.append(odkaz_okrsku)
        for okrsek_odkaz in odkazy_okrsku: # Pro okrsky sečte data
            data_odpoved = get(okrsek_odkaz)
            data_parsovane = bs(data_odpoved.text, features="html.parser")
            pocet_volicu += preved_na_int(data_parsovane.find_all("td")[0].text)
            obalky += preved_na_int(data_parsovane.find_all("td")[1].text)
            platne += preved_na_int(data_parsovane.find_all("td")[4].text)
            tabulky_hlasy = data_parsovane.find_all("table", {"class": "table"})
            for tabulka in tabulky_hlasy[1:]: # Sečte hlasy v okrscích ke každé straně
                for radek in tabulka.find_all("tr")[2:]: # Vynechá záhlaví tabulky
                    strana = radek.find_all("td")[1].text
                    celkem = preved_na_int(radek.find_all("td")[2].text)
                    hlasy[strana] = hlasy.get(strana, 0) + celkem
        
    else: # Pokud není slovo Okrsek, stránka obsahuje rovnou informace k počtům
        pocet_volicu = preved_na_int(data_parsovane.find_all("td")[3].text)
        obalky = preved_na_int(data_parsovane.find_all("td")[4].text)
        platne = preved_na_int(data_parsovane.find_all("td")[7].text)
        tabulky_hlasy = data_parsovane.find_all("table", {"class": "table"})
        for tabulka in tabulky_hlasy[1:]: # Zapíše počet hlasů ke každé straně
            for radek in tabulka.find_all("tr")[2:]: # Vynechá záhlaví tabulky
                strana = radek.find_all("td")[1].text
                celkem = preved_na_int(radek.find_all("td")[2].text)
                hlasy[strana] = celkem
    return (pocet_volicu, obalky, platne, hlasy)

def main():
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty.")
        print("Zadejte: python projekt_3.py 'odkaz' 'vystupni_soubor.csv'")
        sys.exit()

    odkaz = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if not odkaz.startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("Chyba: Zadaný odkaz není správný. Ujistěte se, že zadáváte platný odkaz z webu volby.cz.")
        sys.exit()

    zakladni_odkaz = "https://www.volby.cz/pls/ps2017nss/"
    odpoved = get(odkaz)
    parsovane = bs(odpoved.text, features="html.parser")
    tabulky = parsovane.find_all("table", {"class": "table"})
    obce = [] 
    for tabulka in tabulky:
        for radek in tabulka.find_all("tr")[2:]:  # Vynechá záhlaví tabulky
            zaznam = radek.find_all("td")
            cislo = zaznam[0].text
            nazev = zaznam[1].text
            castecny_odkaz = zaznam[2].find('a')
            if castecny_odkaz:  # Kontrola, zda odkaz existuje
                    odkaz_obce = zakladni_odkaz + castecny_odkaz["href"]
                    obce.append((cislo, nazev, odkaz_obce))

    hlavicka = ["kód obce", "jméno obce", "počet voličů", "vydané obálky", "platné hlasy"]
    odkaz_strany = "https://www.volby.cz/pls/ps2017nss/ps2?xjazyk=CZ"
    odpoved_strany = get(odkaz_strany)
    parsovane_strany = bs(odpoved_strany.text, features="html.parser")
    tabulky_strany = parsovane_strany.find_all("table", {"class": "table"})

    for tabulka in tabulky_strany[1:]: # Připíše strany do hlavičky
        for radek in tabulka.find_all("tr")[2:]:
            strana = radek.find_all("td")[1].text
            if strana.strip() != "-": # Vynechá neplatný záznam
                hlavicka.append(strana)

    with open(vystupni_soubor, mode="w", newline='', encoding="utf-8-sig") as soubor:
        zapisovac = csv.writer(soubor, delimiter=';')  
        zapisovac.writerow(hlavicka)
        for cislo, nazev, odkaz_obce in obce:
            try:
                pocet_volicu, obalky, platne, hlasy = ziskej_data(odkaz_obce, zakladni_odkaz)
                radek = [cislo, nazev, pocet_volicu, obalky, platne]
                for strana in hlavicka[5:]: # Přidá počet hlasů k jednotlivým stranám
                    radek.append(hlasy.get(strana, 0))
                zapisovac.writerow(radek) 
            except Exception as e:
                print(f"Chyba při zpracování obce {nazev}: {e}")

if __name__ == "__main__":
    main()