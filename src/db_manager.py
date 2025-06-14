import sqlite3
import os

DB_NAME = 'sispat_data.db'
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', DB_NAME)

def connect_db():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def create_tables():
    """Creates the 'orgaos' and 'unidades_localizacao' tables if they don't exist."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orgaos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unidades_localizacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
    print("Tabelas 'orgaos' e 'unidades_localizacao' verificadas/criadas.")

def insert_data(table_name: str, data_list: list):
    """Inserts a list of names into the specified table."""
    with connect_db() as conn:
        cursor = conn.cursor()
        for name in data_list:
            try:
                cursor.execute(f"INSERT INTO {table_name} (nome) VALUES (?)", (name,))
            except sqlite3.IntegrityError:
                # This error means the 'nome' already exists due to UNIQUE constraint
                pass # Silently skip duplicates
        conn.commit()
    print(f"Dados inseridos em '{table_name}'. Duplicatas foram ignoradas.")

def get_orgaos() -> list:
    """Retrieves all 'orgaos' names from the database, sorted alphabetically."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM orgaos ORDER BY nome ASC")
        return [row['nome'] for row in cursor.fetchall()]

def get_unidades_localizacao() -> list:
    """Retrieves all 'unidades_localizacao' names from the database, sorted alphabetically."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM unidades_localizacao ORDER BY nome ASC")
        return [row['nome'] for row in cursor.fetchall()]

# Ensure tables are created when this module is imported (or called explicitly)
# This is useful for first-time runs if not using a separate setup script for tables.
create_tables()