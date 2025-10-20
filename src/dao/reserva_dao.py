import sqlite3
import sys
import os

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)

from models.reserva import Reserva

class ReservaDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                cancha_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                estado_id INTEGER NOT NULL,
                tiene_iluminacion BOOLEAN DEFAULT 0,
                tiene_arbitro BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY(cliente_id) REFERENCES clientes(dni),
                FOREIGN KEY(cancha_id) REFERENCES canchas(id),
                FOREIGN KEY(estado_id) REFERENCES estados(id)
            )
        """)
        self.conn.commit()

    def existe(self, id):
        self.cursor.execute("SELECT * FROM reservas WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def verificar_disponibilidad(self, cancha_id, fecha, hora_inicio, hora_fin):
        """
        Verifica que la cancha esté libre durante el horario solicitado.
        """
        self.cursor.execute("""
            SELECT * FROM reservas
            WHERE cancha_id = ? AND fecha = ?
            AND (? < hora_fin AND ? > hora_inicio)
        """, (cancha_id, fecha, hora_inicio, hora_fin))
        return self.cursor.fetchone() is None

    def alta(self, reserva: Reserva):
        # Validaciones de existencia
        if not self.cliente_dao.existe(reserva.cliente_id):
            print("❌ No se puede crear reserva: el cliente NO existe.")
            return False
        if not self.cancha_dao.existe(reserva.cancha_id):
            print("❌ No se puede crear reserva: la cancha NO existe.")
            return False
        if not self.estado_dao.existe(reserva.estado_id):
            print("❌ No se puede crear reserva: el estado NO existe.")
            return False
        if reserva.torneo_id and not self.torneo_dao.existe(reserva.torneo_id):
            print("❌ No se puede crear reserva: el torneo NO existe.")
            return False
        if reserva.pagos_id and not self.pago_dao.existe(reserva.pagos_id):
            print("❌ No se puede crear reserva: el pago NO existe.")
            return False
        if reserva.servicio_id and not self.servicio_dao.existe(reserva.servicio_id):
            print("❌ No se puede crear reserva: el servicio NO existe.")
            return False

        # Validación de disponibilidad
        if not self.verificar_disponibilidad(reserva.cancha_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin):
            print("❌ La cancha ya está reservada en ese horario.")
            return False

        # Inserción
        self.cursor.execute("""
            INSERT INTO reservas (cliente_id, cancha_id, torneo_id, estado_id, pagos_id, fecha, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (reserva.cliente_id, reserva.cancha_id, reserva.torneo_id, reserva.estado_id,
              reserva.pagos_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin))
        self.conn.commit()
        print("✅ Reserva creada exitosamente.")
        return True

    def listar(self):
        self.cursor.execute("SELECT * FROM reservas")
        return self.cursor.fetchall()

    def modificar(self, id, nueva_fecha, nueva_inicio, nueva_fin):
        if not self.existe(id):
            print("❌ No se puede modificar: reserva inexistente.")
            return False
        self.cursor.execute("""
            UPDATE reservas
            SET fecha = ?, hora_inicio = ?, hora_fin = ?
            WHERE id = ?
        """, (nueva_fecha, nueva_inicio, nueva_fin, id))
        self.conn.commit()
        print("✏️ Reserva modificada.")
        return True

    def borrar(self, id):
        if not self.existe(id):
            print("❌ No se puede eliminar: reserva inexistente.")
            return False
        self.cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
        self.conn.commit()
        print("🗑️ Reserva eliminada.")
        return True
