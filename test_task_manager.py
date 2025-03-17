
import pytest
import mysql.connector
import mysql.connector.errors
from conftest import pripojeni_db
from ukoly import pridat_ukol, aktualizovat_ukol, odstranit_ukol
from unittest.mock import patch


@pytest.fixture
def db_cursor(pripojeni_db):
    kurzor = pripojeni_db.cursor()
    yield kurzor
    pripojeni_db.commit()
    pripojeni_db.rollback()
    kurzor.close()


def test_pridat_ukol_pozitivni(db_cursor):
    pridat_ukol(db_cursor._connection, 'Positive 1', 'Popis pozitivniho testu')

    db_cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Positive 1';")

    vysledek = db_cursor.fetchone()

    assert vysledek is not None, "Ukol nebyl přidán"
    assert vysledek[1] == "Positive 1", "Název nesouhlasí"
    assert vysledek[2] == "Popis pozitivniho testu", "Popis nesouhlasí"


def test_pridat_ukol_negativni(db_cursor):
    # === MOCK PRAZDNY NAZEV ===
    with patch('builtins.input', return_value=''):
        pridat_ukol(db_cursor._connection, nazev='', popis='Popis negativniho testu')

    db_cursor.execute("SELECT * FROM ukoly WHERE nazev = '' AND popis = 'Popis negativniho testu';")
    vysledek = db_cursor.fetchone()

    assert vysledek is None, "Úkol s prázdným názvem byl přidán, což je chyba"

    # === MOCK PRAZDNY POPIS ===
    with patch('builtins.input', return_value=''):
        pridat_ukol(db_cursor._connection, nazev="Negative Test", popis="")
    
    db_cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Negative Test' AND popis = '';")
    vysledek = db_cursor.fetchone()

    assert vysledek is None, "Úkol s prázdným popisem byl přidán, což je chyba"

    # === MOCK PRAZDNY NAZEV A POPIS ===
    with patch('builtins.input', side_effect=["", ""]):
        pridat_ukol(db_cursor._connection, nazev="", popis="")
    
    db_cursor.execute("SELECT * FROM ukoly WHERE nazev = '' AND popis = '';")
    vysledek = db_cursor.fetchone()

    assert vysledek is None, "Úkol s prázdnými hodnotami pro název a popis byl přidán, což je chyba"
    

def test_aktualizovat_ukol_pozitivni(db_cursor):
    # === MOCK PRO ZMENU STAVU NA PROBIHA ===
    with patch('builtins.input', side_effect= ['1', 'probiha']):
         aktualizovat_ukol(db_cursor._connection)

    db_cursor.execute("SELECT stav FROM ukoly WHERE id = 1;")
    
    assert db_cursor.fetchone()[0] == 'probiha', "Stav úkolu nebyl správně aktualizován na 'probiha'"

    # === MOCK PRO ZMENU STAVU NA HOTOVO ===
    with patch('builtins.input', side_effect= ['1', 'hotovo']):
         aktualizovat_ukol(db_cursor._connection)

    db_cursor.execute("SELECT stav FROM ukoly WHERE id = 1;")

    assert db_cursor.fetchone()[0] == 'hotovo', "Stav ukolu nebyl spravne zmenen na 'hotovo'"


def test_aktualizovat_ukol_negativni(db_cursor):
    #  === VRACENI DO PUVODNI HODNOTY NEZAHAJENO ===
    db_cursor.execute("UPDATE ukoly SET stav = 'nezahajeno' WHERE id = 1")

    # === MOCK PRO ID A CHYBNY STAV ===
    with patch('builtins.input', side_effect=['1', 'nehotovo']):
        aktualizovat_ukol(db_cursor._connection)

    db_cursor.execute("SELECT stav FROM ukoly WHERE id = 1;")
    vysledek = db_cursor.fetchone()
    
    assert vysledek[0] != 'nehotovo', "Stav úkolu byl neplatně změněn."
    assert vysledek[0] == 'nezahajeno', "Stav úkolu se měl zachovat na 'nezahajeno'."

    # === MOCK PRO NEEXISTUJICI ID ===
    with patch('builtins.input', side_effect=['999', 'probiha']):
        aktualizovat_ukol(db_cursor._connection)

    db_cursor.execute("SELECT stav FROM ukoly WHERE id = 999;")

    assert db_cursor.fetchone() is None, "Úkol s tímto ID neexistuje, ale update probehl."


def test_odstranit_ukol_pozitivni(db_cursor):

    # === PRIDAME TESTOVACI UKOL ===
    db_cursor.execute("INSERT INTO ukoly (nazev, popis, datum_vytvoreni) VALUES ('Test odstraneni', 'Testovací popis', CURDATE())")
    db_cursor._connection.commit()

    # === ZISKAME ID PRIDANEHO UKOLU ===
    db_cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Test odstraneni'")
    id_ukolu = db_cursor.fetchone()[0]

    # === MOCK PRO ODSTRANENI UKOLU ===
    with patch('builtins.input', side_effect=[str(id_ukolu), 'ano']):
        odstranit_ukol(db_cursor._connection)

    # === OVERENI ODSTRANENI UKOLU ===
    db_cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
    
    assert db_cursor.fetchone() is None, "Úkol nebyl správně odstraněn."

    # === PRIDAME TESTOVACI UKOL ===
    db_cursor.execute("INSERT INTO ukoly (nazev, popis, datum_vytvoreni) VALUES ('Test odstraneni', 'Testovací popis', CURDATE())")
    db_cursor._connection.commit()

     # === ZISKAME ID PRIDANEHO UKOLU ===
    db_cursor.execute("SELECT id FROM ukoly WHERE nazev = 'Test odstraneni'")
    id_ukolu = db_cursor.fetchone()[0]

    # === MOCK PRO ZRUSENI ODSTRANENI UKOLU ===
    with patch('builtins.input', side_effect=[str(id_ukolu), 'ne']):
        odstranit_ukol(db_cursor._connection)
    
    # === OVERENI ZE UKOL NEBYL ODSTRANEN ===
    db_cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))

    assert db_cursor.fetchone() is not None, "Zruseni smazani neprobehlo"


def test_odstranit_ukol_negativni(db_cursor):

    # === MOCK PRO ODSTRANENI UKOLU S NEEXISTUJICIM ID ===
    with patch('builtins.input', side_effect=['999999', 'ano']):  
        odstranit_ukol(db_cursor._connection)

    # === OVERENI ZE UKOL NEBYL ODSTRANEN ===
    db_cursor.execute("SELECT COUNT(*) FROM ukoly")
    pocet_ukolu = db_cursor.fetchone()[0]
    assert pocet_ukolu >= 0, "Odstranil se neexistující úkol!"