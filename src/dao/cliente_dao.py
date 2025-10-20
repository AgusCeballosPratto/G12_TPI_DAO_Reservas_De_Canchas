import sqlite3
import sys
import os

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)

from models.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def existe(self, dni):
        self.cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni,))
        return self.cursor.fetchone() is not None
    
    


    def alta(self, cliente: Cliente):
        self.cursor.execute("""
            INSERT INTO clientes (dni, nombre, apellido, email, telefono)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente.dni, cliente.nombre, cliente.apellido, cliente.email, cliente.telefono))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()
    
    def listar_id(self, dni):
        self.cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni,))
        return self.cursor.fetchone()

    def modificar(self, dni, nuevo_email, nuevo_telefono):
        self.cursor.execute("""
            UPDATE clientes
            SET email = ?, telefono = ?
            WHERE dni = ?
        """, (nuevo_email, nuevo_telefono, dni))
        self.conn.commit()

    def borrar(self, dni):
        self.cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni,))
        self.conn.commit()
