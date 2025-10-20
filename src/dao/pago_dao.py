from models.pago import Pago
from db.database_config import get_connection
from dao.estado_dao import EstadoDAO

class PagoDAO:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.estado_dao = EstadoDAO()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estado_id INTEGER,
                monto REAL NOT NULL,
                fecha_pago TEXT NOT NULL,
                metodo TEXT NOT NULL,
                FOREIGN KEY(estado_id) REFERENCES estados(id)
            )
        """)
        self.conn.commit()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM pagos WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def alta(self, pago: Pago):
        if pago.estado_id and not self.estado_dao.existe(pago.estado_id):
            print("❌ Error: El estado ingresado no existe.")
            return False

        self.cursor.execute("""
            INSERT INTO pagos (estado_id, monto, fecha_pago, metodo)
            VALUES (?, ?, ?, ?)
        """, (pago.estado_id, pago.monto, pago.fecha_pago, pago.metodo))
        self.conn.commit()
        print("✅ Pago registrado.")
        return True

    def listar(self):
        self.cursor.execute("SELECT * FROM pagos")
        return self.cursor.fetchall()

    def borrar(self, id):
        # Verificar si está asociado a una reserva
        self.cursor.execute("SELECT * FROM reservas WHERE pagos_id = ?", (id,))
        if self.cursor.fetchone():
            print("❌ No se puede eliminar: pago asociado a una reserva.")
            return False

        self.cursor.execute("DELETE FROM pagos WHERE id = ?", (id,))
        self.conn.commit()
        print("🗑️ Pago eliminado.")
        return True
