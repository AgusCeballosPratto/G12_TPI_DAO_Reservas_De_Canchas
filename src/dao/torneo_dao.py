import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.torneo import Torneo

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)

class TorneoDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def existe(self, id):
        self.cursor.execute("SELECT * FROM torneos WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None
    
    def existe_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM torneos WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone() is not None
    
    def alta(self, torneo):
        self.cursor.execute("""
            INSERT INTO torneos (nombre, fecha_inicio, fecha_fin, tipo)
            VALUES (?, ?, ?, ?)
        """, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin, torneo.tipo))
        self.conn.commit()
        self.conn.close()
    
    def listar(self):
        self.cursor.execute("SELECT * FROM torneos")
        return self.cursor.fetchall()
    
    def listar_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM torneos WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone()
    
    def listar_id(self, id):
        pass
    
    def modificar(self, id):
        pass
        
    # borrar en cascada torneo y reservas asociadas
    def borrar(self, id):
        self.cursor.execute("DELETE FROM torneos WHERE id = ?", (id,))
        self.cursor.execute("DELETE FROM reservas WHERE torneo_id = ?", (id,))
        self.conn.commit()
        self.conn.close()