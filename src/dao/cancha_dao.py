import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.cancha import Cancha

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)


class CanchaDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


    def existe(self, id):
        self.cursor.execute("SELECT * FROM canchas WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None
    
    def existe_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM canchas WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone() is not None

    
    def alta(self, cancha):
        self.cursor.execute("""
            INSERT INTO canchas (nombre, tipo, costo_por_hora, estado_id, tiene_iluminacion)
            VALUES (?, ?, ?, ?, ?)
        """, (cancha.nombre, cancha.tipo, cancha.costo_por_hora, cancha.estado_id, cancha.tiene_iluminacion))
        self.conn.commit()
        self.conn.close()

    def listar(self):
        self.cursor.execute("SELECT * FROM canchas")
        return self.cursor.fetchall()
    
    def listar_id(self, id):
        self.cursor.execute("SELECT * FROM canchas WHERE id = ?", (id,))
        return self.cursor.fetchone()
    
    def listar_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM canchas WHERE nombre = ?", (nombre,))
        return self.cursor.fetchone()
    
    def listar_iluminacion(self):
        self.cursor.execute("SELECT * FROM canchas WHERE tiene_iluminacion = 1")
        return self.cursor.fetchall()

    def modificar(self, id, nuevo_nombre, nuevo_tipo, nuevo_costo):
        self.cursor.execute("""
            UPDATE canchas
            SET nombre = ?, tipo = ?, costo_por_hora = ?
            WHERE id = ?
        """, (nuevo_nombre, nuevo_tipo, nuevo_costo, id))
        self.conn.commit()
        self.conn.close()

    def borrar(self, id):
        self.cursor.execute("DELETE FROM canchas WHERE id = ?", (id,))
        self.conn.commit()
        self.conn.close()

