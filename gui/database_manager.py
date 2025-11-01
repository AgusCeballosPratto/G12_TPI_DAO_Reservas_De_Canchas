"""
Clase para mejorar el manejo de conexiones de base de datos en los DAOs
"""
import sqlite3
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

class DatabaseManager:
    """Gestiona las conexiones a la base de datos de forma centralizada"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self, db_path="reservasdecanchas.db"):
        """Obtener una conexión a la base de datos"""
        if self._connection is None:
            self._connection = sqlite3.connect(db_path)
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection
    
    def close_connection(self):
        """Cerrar la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def execute_query(self, query, params=None, fetch=False, db_path="reservasdecanchas.db"):
        """Ejecutar una consulta de forma segura"""
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall() if fetch == 'all' else cursor.fetchone()
                conn.close()
                return result
            else:
                conn.commit()
                last_id = cursor.lastrowid
                conn.close()
                return last_id
                
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            raise e