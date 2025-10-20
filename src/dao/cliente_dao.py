import sqlite3
from models.cliente import Cliente

class ClienteDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                dni INTEGER PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                email TEXT,
                telefono INTEGER,
                created_at TEXT
            )
        """)
        self.conn.commit()
        
    def existe(self, dni):
        self.cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni,))
        return self.cursor.fetchone() is not None


    def alta(self, cliente: Cliente):
        self.cursor.execute("""
            INSERT INTO clientes (dni, nombre, apellido, email, telefono, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (cliente.dni, cliente.nombre, cliente.apellido, cliente.email, cliente.telefono))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM clientes")
        return self.cursor.fetchall()

    def modificar(self, dni, nuevo_nombre, nuevo_apellido):
        self.cursor.execute("""
            UPDATE clientes
            SET nombre = ?, apellido = ?
            WHERE dni = ?
        """, (nuevo_nombre, nuevo_apellido, dni))
        self.conn.commit()

    def borrar(self, dni):
        self.cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni,))
        self.conn.commit()
