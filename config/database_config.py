import sqlite3
import sys
import os

# Agregar directorios al path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importar desde el mismo directorio
try:
    from database_init import inicializar_sistema_base_datos
except ImportError:
    from .database_init import inicializar_sistema_base_datos

# Configuración global de la base de datos
DB_NAME = "reservasdecanchas.db"

def get_connection(db_name=None):
    if db_name is None:
        db_name = DB_NAME
    
    inicializar_sistema_base_datos(db_name)
    
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_database(db_name=None):
    if db_name is None:
        db_name = DB_NAME
    
    inicializar_sistema_base_datos(db_name)
