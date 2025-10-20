from models.servicio import Servicio
from db.database_config import get_connection

class ServicioDAO:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                costo REAL
            )
        """)
        self.conn.commit()

    def alta(self, servicio: Servicio):
        self.cursor.execute(
            "INSERT INTO servicios (nombre, costo) VALUES (?, ?)",
            (servicio.nombre, servicio.costo)
        )
        self.conn.commit()
        print("✅ Servicio agregado.")

    def listar(self):
        self.cursor.execute("SELECT * FROM servicios")
        return self.cursor.fetchall()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM servicios WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def borrar(self, id):
        # No eliminar si está asociado a reservas
        self.cursor.execute("SELECT * FROM reservaPorServicio WHERE servicio_id = ?", (id,))
        if self.cursor.fetchone():
            print("❌ No se puede eliminar: el servicio está asociado a reservas.")
            return False

        self.cursor.execute("DELETE FROM servicios WHERE id = ?", (id,))
        self.conn.commit()
        print("🗑️ Servicio eliminado.")
        return True
