from models.estado import Estado
from db.database_config import get_connection

class EstadoDAO:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ambito INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def alta(self, estado: Estado):
        self.cursor.execute(
            "INSERT INTO estados (nombre, ambito) VALUES (?, ?)",
            (estado.nombre, estado.ambito)
        )
        self.conn.commit()
        print("✅ Estado registrado.")

    def listar(self):
        self.cursor.execute("SELECT * FROM estados")
        return self.cursor.fetchall()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM estados WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def borrar(self, id):
        # No se puede eliminar si está asociado a otra entidad
        tablas = ["reservas", "pagos", "canchas"]
        for tabla in tablas:
            self.cursor.execute(f"SELECT * FROM {tabla} WHERE estado_id = ?", (id,))
            if self.cursor.fetchone():
                print(f"❌ No se puede eliminar: el estado está asociado en la tabla '{tabla}'.")
                return False

        self.cursor.execute("DELETE FROM estados WHERE id = ?", (id,))
        self.conn.commit()
        print("🗑️ Estado eliminado.")
        return True
