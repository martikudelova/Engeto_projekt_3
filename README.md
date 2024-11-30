# Projekt: Sběr volebních dat z webu volby.cz

Tento projekt slouží k získání volebních dat územních celků z tohoto dokazu "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ".
Kód sbírá informace o počtech voličů, vydaných obálkách, platných hlasech a výsledcích jednotlivých stran na základě zadaného odkazu.
Data jsou následně exportována do souboru CSV.

## Jak nainstalovat potřebné knihovny

Pro tento projekt budete potřebovat několik knihoven, které lze nainstalovat pomocí "pip". Najdete je v souboru "requirements.txt".
Doporučuji si předem vytvořit virtuální prostředí.

### Jak spustit projekt

Skript lze spustit z příkazové řádky. Potřebujete zadat 2 argumenty:
-odkaz na stránku územního celku
-výstupní soubor

Příklad:
python projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103" "vysledky_karvina.csv"

#### Informace k výstupnímu souboru

Soubor .csv můžete otevřít např. v Excelu.
V záhlaví najdete kód obce, jméno obce, počet voličů, počet vydaných obálek, počet platných hlasů a všechny kandidující strany.
Řádky obsahují informace ke konkrétní obci.
