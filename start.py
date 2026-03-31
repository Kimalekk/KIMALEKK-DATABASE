import sqlite3
from datetime import datetime

DATABASE = "produkty.db"

def inicjalizuj_baze():
    """Tworzy bazę danych i tabelę jeśli nie istnieje"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produkty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL UNIQUE,
            cena REAL NOT NULL,
            status TEXT NOT NULL,
            data_dodania TEXT NOT NULL,
            ilosc INTEGER DEFAULT 1
        )
        ''')
        
        # Dodaj przykładowe dane jeśli tabela jest pusta
        cursor.execute('SELECT COUNT(*) FROM produkty')
        if cursor.fetchone()[0] == 0:
            przykladowe_dane = [
                ("Karta Graficzna", 2500, "Wysyłka", datetime.now().isoformat(), 2),
                ("Monitor 4K", 1200, "Magazyn", datetime.now().isoformat(), 1),
                ("Kabel HDMI", 45, "Wysłano", datetime.now().isoformat(), 5)
            ]
            cursor.executemany(
                'INSERT INTO produkty (nazwa, cena, status, data_dodania, ilosc) VALUES (?, ?, ?, ?, ?)',
                przykladowe_dane
            )
            print("✓ Baza inicjalizowana z przykładowymi danymi\n")
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Błąd bazy danych: {e}")

def wyswietl_menu():
    """Wyświetla menu główne"""
    print("\n" + "="*50)
    print("📊 SYSTEM ZARZĄDZANIA PRODUKTAMI")
    print("="*50)
    print("1. 📋 Wyświetl wszystkie produkty")
    print("2. ➕ Dodaj nowy produkt")
    print("3. ✏️  Edytuj produkt")
    print("4. 🗑️  Usuń produkt")
    print("5. 🔍 Szukaj produktu")
    print("6. 📈 Statystyki")
    print("0. ❌ Wyjdź")
    print("="*50)

def wyswietl_produkty():
    """Wyświetla wszystkie produkty"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produkty ORDER BY id DESC')
        produkty = cursor.fetchall()
        conn.close()
        
        if not produkty:
            print("\n⚠️  Baza jest pusta!")
            return
        
        print("\n" + "─"*80)
        print(f"{'ID':<5} {'Nazwa':<25} {'Cena':<12} {'Status':<15} {'Ilość':<8}")
        print("─"*80)
        for p in produkty:
            print(f"{p[0]:<5} {p[1]:<25} {p[2]:<12.2f}zł {p[3]:<15} {p[5]:<8}")
        print("─"*80)
        print(f"\nŁączna wartość: {sum([p[2]*p[5] for p in produkty]):.2f}zł")
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def dodaj_produkt():
    """Dodaje nowy produkt"""
    try:
        nazwa = input("\nPodaj nazwę produktu: ").strip()
        if not nazwa:
            print("❌ Nazwa nie może być pusta!")
            return
        
        while True:
            try:
                cena = float(input("Podaj cenę (PLN): "))
                if cena < 0:
                    print("❌ Cena nie może być ujemna!")
                    continue
                break
            except ValueError:
                print("❌ Cena musi być liczbą!")
        
        print("\nDostępne statusy: Magazyn, Wysyłka, Wysłano, Zwrot")
        status = input("Podaj status: ").strip() or "Magazyn"
        
        while True:
            try:
                ilosc = int(input("Podaj ilość: ") or "1")
                if ilosc <= 0:
                    print("❌ Ilość musi być większa od 0!")
                    continue
                break
            except ValueError:
                print("❌ Ilość musi być liczbą!")
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO produkty (nazwa, cena, status, data_dodania, ilosc) VALUES (?, ?, ?, ?, ?)',
            (nazwa, cena, status, datetime.now().isoformat(), ilosc)
        )
        conn.commit()
        conn.close()
        print(f"✓ Produkt '{nazwa}' dodany pomyślnie!")
    except sqlite3.IntegrityError:
        print("❌ Produkt o tej nazwie już istnieje!")
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def edytuj_produkt():
    """Edytuje istniejący produkt"""
    try:
        wyswietl_produkty()
        try:
            id_prod = int(input("\nPodaj ID produktu do edycji: "))
        except ValueError:
            print("❌ ID musi być liczbą!")
            return
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produkty WHERE id = ?', (id_prod,))
        produkt = cursor.fetchone()
        
        if not produkt:
            print("❌ Produkt nie znaleziony!")
            conn.close()
            return
        
        print(f"\nEdytowanie: {produkt[1]} (Cena: {produkt[2]}zł, Status: {produkt[3]})")
        
        nowa_nazwa = input("Nowa nazwa (Enter aby pominąć): ").strip() or produkt[1]
        
        while True:
            try:
                nowa_cena_input = input("Nowa cena (Enter aby pominąć): ").strip()
                nowa_cena = float(nowa_cena_input) if nowa_cena_input else produkt[2]
                if nowa_cena < 0:
                    print("❌ Cena nie może być ujemna!")
                    continue
                break
            except ValueError:
                print("❌ Cena musi być liczbą!")
        
        nowy_status = input("Nowy status (Enter aby pominąć): ").strip() or produkt[3]
        
        while True:
            try:
                nowa_ilosc_input = input("Nowa ilość (Enter aby pominąć): ").strip()
                nowa_ilosc = int(nowa_ilosc_input) if nowa_ilosc_input else produkt[5]
                if nowa_ilosc <= 0:
                    print("❌ Ilość musi być większa od 0!")
                    continue
                break
            except ValueError:
                print("❌ Ilość musi być liczbą!")
        
        cursor.execute(
            'UPDATE produkty SET nazwa = ?, cena = ?, status = ?, ilosc = ? WHERE id = ?',
            (nowa_nazwa, nowa_cena, nowy_status, nowa_ilosc, id_prod)
        )
        conn.commit()
        conn.close()
        print("✓ Produkt zaktualizowany!")
    except sqlite3.IntegrityError:
        print("❌ Produkt o tej nazwie już istnieje!")
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def usun_produkt():
    """Usuwa produkt z bazy"""
    try:
        wyswietl_produkty()
        try:
            id_prod = int(input("\nPodaj ID produktu do usunięcia: "))
        except ValueError:
            print("❌ ID musi być liczbą!")
            return
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT nazwa FROM produkty WHERE id = ?', (id_prod,))
        produkt = cursor.fetchone()
        
        if not produkt:
            print("❌ Produkt nie znaleziony!")
            conn.close()
            return
        
        potwierdzenie = input(f"⚠️  Czy na pewno usunąć '{produkt[0]}'? (tak/nie): ").lower()
        if potwierdzenie == 'tak':
            cursor.execute('DELETE FROM produkty WHERE id = ?', (id_prod,))
            conn.commit()
            print("✓ Produkt usunięty!")
        else:
            print("❌ Anulowano")
        
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def szukaj_produktu():
    """Szuka produktu po nazwie"""
    try:
        szukaj = input("\nPodaj fragmentu nazwy do szukania: ").strip()
        if not szukaj:
            print("❌ Wpisz coś do szukania!")
            return
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produkty WHERE nazwa LIKE ? ORDER BY id DESC', (f'%{szukaj}%',))
        wyniki = cursor.fetchall()
        conn.close()
        
        if not wyniki:
            print(f"\n⚠️  Brak wyników dla '{szukaj}'")
            return
        
        print(f"\n📍 Znalezione {len(wyniki)} produktów:")
        print("─"*80)
        print(f"{'ID':<5} {'Nazwa':<25} {'Cena':<12} {'Status':<15} {'Ilość':<8}")
        print("─"*80)
        for p in wyniki:
            print(f"{p[0]:<5} {p[1]:<25} {p[2]:<12.2f}zł {p[3]:<15} {p[5]:<8}")
        print("─"*80)
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def statystyki():
    """Wyświetla statystyki"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Całkowita wartość
        cursor.execute('SELECT SUM(cena * ilosc) FROM produkty')
        wartosc = cursor.fetchone()[0] or 0
        
        # Liczba produktów
        cursor.execute('SELECT COUNT(*) FROM produkty')
        liczba = cursor.fetchone()[0]
        
        # Średnia cena
        cursor.execute('SELECT AVG(cena) FROM produkty')
        srednia = cursor.fetchone()[0] or 0
        
        # Najdroższy produkt
        cursor.execute('SELECT MAX(cena), nazwa FROM produkty')
        najdrozszy = cursor.fetchone()
        
        # Statusiów
        cursor.execute('SELECT status, COUNT(*) FROM produkty GROUP BY status')
        statusy = cursor.fetchall()
        
        print("\n" + "="*50)
        print("📊 STATYSTYKI")
        print("="*50)
        print(f"💰 Całkowita wartość: {wartosc:.2f}zł")
        print(f"📦 Liczba produktów: {liczba}")
        print(f"📈 Średnia cena: {srednia:.2f}zł")
        if najdrozszy[0]:
            print(f"🔝 Najdroższy: {najdrozszy[1]} ({najdrozszy[0]:.2f}zł)")
        
        print("\nRozkład statusów:")
        for status, count in statusy:
            print(f"  • {status}: {count}")
        print("="*50)
        
        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Błąd: {e}")

def main():
    """Główna pętla programu"""
    inicjalizuj_baze()
    
    while True:
        wyswietl_menu()
        wybor = input("Wybierz opcję (0-6): ").strip()
        
        if wybor == '1':
            wyswietl_produkty()
        elif wybor == '2':
            dodaj_produkt()
        elif wybor == '3':
            edytuj_produkt()
        elif wybor == '4':
            usun_produkt()
        elif wybor == '5':
            szukaj_produktu()
        elif wybor == '6':
            statystyki()
        elif wybor == '0':
            print("\n👋 Do widzenia!")
            break
        else:
            print("❌ Błędny wybór! Spróbuj Ponownie.")

if __name__ == "__main__":
    main()
