import pytest
import mysql.connector

@pytest.fixture(scope="module")
def pripojeni_db():
    # Připojení k testovací databázi
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nove.Heslo.123",
        database="test_task_manager"  
    )
    cursor = conn.cursor()
    
    # Vytvoření tabulky před spuštěním testů
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(50) NOT NULL CHECK (nazev <> ''),
            popis VARCHAR(100) NOT NULL CHECK (popis<> ''),
            stav ENUM('nezahajeno', 'hotovo', 'probiha') NOT NULL DEFAULT 'nezahajeno',
            datum_vytvoreni DATE NOT NULL
        )
    """)
    conn.commit()
    
    yield conn 
    
    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()
    
    cursor.close()
    conn.close()