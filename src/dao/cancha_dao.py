import sqlite3
import sys
import os

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)

from models.cancha import Cancha

class CanchaDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


    def existe(self, id):
        self.cursor.execute("SELECT * FROM canchas WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    
    def alta(self, cancha: Cancha):
        self.cursor.execute("""
            INSERT INTO canchas (nombre, tipo, costo_por_hora, estado_id)
            VALUES (?, ?, ?, ?)
        """, (cancha.nombre, cancha.tipo, cancha.costo_por_hora, cancha.estado_id))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM canchas")
        return self.cursor.fetchall()
    
    def listar_id(self, id_cancha):
        self.cursor.execute("SELECT * FROM canchas WHERE id = ?", (id_cancha,))
        return self.cursor.fetchone()

    def modificar(self, id, nuevo_nombre, nuevo_tipo, nuevo_costo):
        self.cursor.execute("""
            UPDATE canchas
            SET nombre = ?, tipo = ?, costo_por_hora = ?
            WHERE id = ?
        """, (nuevo_nombre, nuevo_tipo, nuevo_costo, id))
        self.conn.commit()

    def borrar(self, id):
        self.cursor.execute("DELETE FROM canchas WHERE id = ?", (id,))
        self.conn.commit()
