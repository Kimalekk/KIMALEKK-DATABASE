import csv

# Twoje pierwsze dane (lista produktów)
dane = [
    ["Produkt", "Cena", "Status"],
    ["Test", 2500, "Wysyłka"],
    ["Test1", 1200, "Magazyn"],
    ["Test2", 45, "Wysłano"]
]

# Tworzenie pliku CSV (to taka uproszczona baza danych)
with open('moje_dane.csv', mode='w', newline='', encoding='utf-8') as plik:
    writer = csv.writer(plik)
    writer.writerows(dane)

print("Sukces! Plik moje_dane.csv został utworzony w Twoim folderze.")

nowy_produkt = input("Podaj nazwę produktu: ")
nowa_cena = input("Podaj cenę: ")

print(f"Dodano do bazy: {nowy_produkt} za {nowa_cena} PLN")
