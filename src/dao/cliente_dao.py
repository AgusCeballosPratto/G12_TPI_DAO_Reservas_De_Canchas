import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.cliente import Cliente

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)


class ClienteDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def existe(self, id):
        self.cursor.execute("SELECT * FROM clientes WHERE dni = ?", (id,))
        return self.cursor.fetchone() is not None

    def alta(self, cliente):
        self.cursor.execute("""
            INSERT INTO clientes (dni, nombre, apellido, email, telefono)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente.dni, cliente.nombre, cliente.apellido, cliente.email, cliente.telefono))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()
    
    def listar_id(self, id):
        self.cursor.execute("SELECT * FROM clientes WHERE dni = ?", (id,))
        return self.cursor.fetchone()

    def modificar(self, id, nuevo_email, nuevo_telefono):
        self.cursor.execute("""
            UPDATE clientes
            SET email = ?, telefono = ?
            WHERE dni = ?
        """, (nuevo_email, nuevo_telefono, id))
        self.conn.commit()

    def borrar(self, id):
        self.cursor.execute("DELETE FROM clientes WHERE dni = ?", (id,))
        self.conn.commit()
