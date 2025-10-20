from models.torneo import Torneo
from db.database_config import get_connection

class TorneoDAO:
    def __init__(self):
        super().__init__()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS torneos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def alta(self, torneo: Torneo):
        self.cursor.execute("""
            INSERT INTO torneos (nombre, fecha_inicio, fecha_fin, tipo)
            VALUES (?, ?, ?, ?)
        """, (torneo.nombre, torneo.fecha_inicio, torneo.fecha_fin, torneo.tipo))
        self.conn.commit()
        print("✅ Torneo agregado.")

    def listar(self):
        self.cursor.execute("SELECT * FROM torneos")
        return self.cursor.fetchall()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM torneos WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def borrar(self, id):
        self.cursor.execute("SELECT * FROM reservas WHERE torneo_id = ?", (id,))
        if self.cursor.fetchone():
            print("❌ No se puede eliminar: torneo asociado a reservas.")
            return False

        self.cursor.execute("DELETE FROM torneos WHERE id = ?", (id,))
        self.conn.commit()
        print("🗑️ Torneo eliminado.")
        return True
