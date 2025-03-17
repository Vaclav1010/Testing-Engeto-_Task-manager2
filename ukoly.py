def pridat_ukol(spojeni, nazev = None, popis = None):
    if not nazev or not popis:
        nazev = input("\nZadejte název úkolu: ")
        popis = input("Zadejte popis úkolu: ")

    if not nazev or not popis:
        print("Název a popis úkolu jsou povinné!")
        return

    cursor = spojeni.cursor()
    query = "INSERT INTO ukoly (nazev, popis, datum_vytvoreni) VALUES (%s, %s, CURDATE())"
    cursor.execute(query, (nazev, popis))
    spojeni.commit()

    print(f"Úkol '{nazev}' byl úspěšně přidán.")


def zobrazit_ukoly(spojeni):
    cursor = spojeni.cursor()
    query = "SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('nezahajeno', 'probiha')"
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        print("\nŽádné úkoly k zobrazení.")
        
    else:
        for row in result:
            print(f"\nID: {row[0]}, Název: {row[1]}, Popis: {row[2]}, Stav: {row[3]}")

def aktualizovat_ukol(spojeni, id_ukolu = None, novy_stav = None):
    if not id_ukolu:
        id_ukolu = input("\nZadejte ID úkolu k aktualizaci: ")
    
    cursor = spojeni.cursor()
    query = "SELECT id, nazev, stav FROM ukoly WHERE id = %s"
    cursor.execute(query, (id_ukolu,))
    result = cursor.fetchone()

    if result is None:
        print("Úkol s tímto ID neexistuje.")
        return

    print(f"Úkol: {result[1]}, Stav: {result[2]}")
    if not novy_stav:
        novy_stav = input("Zadejte nový stav (probiha/hotovo): ")

    if novy_stav not in ['probiha', 'hotovo']:
        print("Neplatný stav.")
        return

    update_query = "UPDATE ukoly SET stav = %s WHERE id = %s"
    cursor.execute(update_query, (novy_stav, id_ukolu))
    spojeni.commit()

    print(f"Stav úkolu ID {id_ukolu} byl úspěšně aktualizován na '{novy_stav}'.")


def odstranit_ukol(spojeni):
    # Zobrazení všech úkolů v databázi
    cursor = spojeni.cursor()
    query = "SELECT id, nazev, stav FROM ukoly"
    cursor.execute(query)
    vsechny_ukoly = cursor.fetchall()

    if vsechny_ukoly:
        print("\nSeznam všech úkolů v databázi:")
        for ukol in vsechny_ukoly:
            print(f"ID: {ukol[0]}, Název: {ukol[1]}, Stav: {ukol[2]}")
    else:
        print("V databázi nejsou žádné úkoly.")
        return

    # Zadání ID úkolu k odstranění
    id_ukolu = input("\nZadejte ID úkolu k odstranění: ")

    query = "SELECT id, nazev FROM ukoly WHERE id = %s"
    cursor.execute(query, (id_ukolu,))
    result = cursor.fetchone()

    if result is None:
        print("Úkol s tímto ID neexistuje.")
        return

    print(f"Úkol: {result[1]} bude odstraněn.")
    confirm = input("Opravdu chcete úkol odstranit? (ano/ne): ")
    
    if confirm.lower() == 'ano':
        delete_query = "DELETE FROM ukoly WHERE id = %s"
        cursor.execute(delete_query, (id_ukolu,))
        spojeni.commit()
        print(f"Úkol ID {id_ukolu} byl úspěšně odstraněn.")
    else:
        print("Odstranění úkolu bylo zrušeno.")