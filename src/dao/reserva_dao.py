import sqlite3
import sys
import os
from datetime import date, time

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)

from models.reserva import Reserva

class ReservaDAO:
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()


    def existe(self, id):
        self.cursor.execute("SELECT * FROM reservas WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None

    def verificar_disponibilidad(self, reserva, excluir_reserva_id=False):
        try:
            query = """
                SELECT COUNT(*) 
                FROM reservas
                WHERE cancha_id = ?
                AND fecha = ?
                AND estado_id != 4
                AND NOT (hora_fin <= ? OR hora_inicio >= ?)
            """

            params = [reserva.cancha_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin]

            if excluir_reserva_id:
                query += " AND id != ?"
                params.append(excluir_reserva_id)

            self.cursor.execute(query, params)
            conflictos = self.cursor.fetchone()[0]

            return conflictos == 0  

        except Exception as e:
            print(f"Error verificando disponibilidad: {e}")
            return False


    def alta(self, reserva: Reserva):
        self.cursor.execute("""
            INSERT INTO reservas (cliente_id, cancha_id, estado_id, fecha, hora_inicio, hora_fin, tiene_iluminacion, tiene_arbitro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (reserva.cliente_id, reserva.cancha_id, reserva.estado_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin, reserva.tiene_iluminacion, reserva.tiene_arbitro))
        self.conn.commit()


    def listar(self):
        self.cursor.execute("SELECT * FROM reservas")
        return self.cursor.fetchall()

    def modificar(self, id_reserva):
        self.cursor.execute("""
            UPDATE reservas
            SET estado_id = 4
            WHERE id = ?
        """, (id_reserva,))
        self.conn.commit()


    def borrar(self, id):
        self.cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
        self.conn.commit()
