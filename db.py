
import mysql.connector


def pripojeni_db():
    try:
        spojeni = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nove.Heslo.123",
            database="task_manager"
        )
        return spojeni
    except mysql.connector.Error as error:
        print(f"Chyba při připojení k databázi: {error}")
        return None

def vytvoreni_tabulky(spojeni):
    cursor = spojeni.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(50) NOT NULL CHECK (nazev <> ''),
                popis VARCHAR(100) NOT NULL CHECK (popis <> ''),
                stav ENUM('nezahajeno', 'hotovo', 'probiha') NOT NULL DEFAULT 'nezahajeno',
                datum_vytvoreni DATE NOT NULL
            )
        """)
        spojeni.commit()
    except mysql.connector.Error as error:
        print(f"Chyba při vytváření tabulky: {error}")
    
    cursor.close()
    
    