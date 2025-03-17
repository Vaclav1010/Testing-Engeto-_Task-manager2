from db import pripojeni_db,vytvoreni_tabulky
from ukoly import pridat_ukol,zobrazit_ukoly,aktualizovat_ukol,odstranit_ukol

def hlavni_menu():
    spojeni = pripojeni_db()
    if spojeni is None:
        return

    vytvoreni_tabulky(spojeni)

    while True:
        print("\nSprávce úkolů - Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        
        user_choice = input("Vyberte možnost (1-5): ")

        if user_choice == "1":
            pridat_ukol(spojeni)
        elif user_choice == "2":
            zobrazit_ukoly(spojeni)
        elif user_choice == "3":
            zobrazit_ukoly(spojeni)
            aktualizovat_ukol(spojeni)
        elif user_choice == "4":
            odstranit_ukol(spojeni)
        elif user_choice == "5":
            print("\nKonec programu.")
            break
        else:
            print("\nNeplatná volba!")

    spojeni.close()
    
if __name__ == "__main__":
    hlavni_menu()