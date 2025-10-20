import sqlite3
from models.cancha import Cancha

class CanchaDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS canchas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT,
                costo_por_hora REAL,
                capacidad INTEGER,
                estado_id INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM canchas WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    
    def alta(self, cancha: Cancha):
        self.cursor.execute("""
            INSERT INTO canchas (nombre, tipo, costo_por_hora, capacidad, estado_id)
            VALUES (?, ?, ?, ?, ?)
        """, (cancha.nombre, cancha.tipo, cancha.costo_por_hora, cancha.capacidad, cancha.estado_id))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM canchas")
        return self.cursor.fetchall()

    def modificar(self, id, nuevo_nombre, nuevo_tipo, nuevo_costo, nueva_capacidad):
        self.cursor.execute("""
            UPDATE canchas
            SET nombre = ?, tipo = ?, costo_por_hora = ?, capacidad = ?
            WHERE id = ?
        """, (nuevo_nombre, nuevo_tipo, nuevo_costo, nueva_capacidad, id))
        self.conn.commit()

    def borrar(self, id):
        self.cursor.execute("DELETE FROM canchas WHERE id = ?", (id,))
        self.conn.commit()
