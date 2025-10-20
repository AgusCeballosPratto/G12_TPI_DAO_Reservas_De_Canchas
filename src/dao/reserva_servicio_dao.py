from models.reserva_servicio import ReservaServicio
from db.database_config import get_connection
from dao.reserva_dao import ReservaDAO
from dao.servicio_dao import ServicioDAO

class ReservaServicioDAO:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.reserva_dao = ReservaDAO()
        self.servicio_dao = ServicioDAO()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservaPorServicio (
                reserva_id INTEGER NOT NULL,
                servicio_id INTEGER NOT NULL,
                FOREIGN KEY(reserva_id) REFERENCES reservas(id),
                FOREIGN KEY(servicio_id) REFERENCES servicios(id),
                PRIMARY KEY (reserva_id, servicio_id)
            )
        """)
        self.conn.commit()

    def existe_asociacion(self, reserva_id, servicio_id):
        self.cursor.execute("""
            SELECT * FROM reservaPorServicio
            WHERE reserva_id = ? AND servicio_id = ?
        """, (reserva_id, servicio_id))
        return self.cursor.fetchone() is not None

    def alta(self, reserva_servicio: ReservaServicio):
        if not self.reserva_dao.existe(reserva_servicio.reserva_id):
            print("❌ No se puede asociar: la reserva NO existe.")
            return False
        if not self.servicio_dao.existe(reserva_servicio.servicio_id):
            print("❌ No se puede asociar: el servicio NO existe.")
            return False
        if self.existe_asociacion(reserva_servicio.reserva_id, reserva_servicio.servicio_id):
            print("⚠️ La asociación ya existe.")
            return False

        self.cursor.execute("""
            INSERT INTO reservaPorServicio (reserva_id, servicio_id)
            VALUES (?, ?)
        """, (reserva_servicio.reserva_id, reserva_servicio.servicio_id))
        self.conn.commit()
        print("✅ Servicio asociado a la reserva.")
        return True

    def listar(self):
        self.cursor.execute("SELECT * FROM reservaPorServicio")
        return self.cursor.fetchall()

    def borrar(self, reserva_id, servicio_id):
        if not self.existe_asociacion(reserva_id, servicio_id):
            print("❌ No se puede eliminar: la asociación no existe.")
            return False

        self.cursor.execute("""
            DELETE FROM reservaPorServicio
            WHERE reserva_id = ? AND servicio_id = ?
        """, (reserva_id, servicio_id))
        self.conn.commit()
        print("🗑️ Asociación eliminada exitosamente.")
        return True
