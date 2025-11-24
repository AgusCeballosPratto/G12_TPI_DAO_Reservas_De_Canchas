import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.reserva import Reserva

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)


class ReservaDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.db_path = db_path

    def existe(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (id,))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def verificar_disponibilidad(self, reserva, excluir_reserva_id=False):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
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

            cursor.execute(query, params)
            conflictos = cursor.fetchone()[0]
            conn.close()

            return conflictos == 0  

        except Exception as e:
            if 'conn' in locals():
                conn.close()
            print(f"Error verificando disponibilidad: {e}")
            return False


    def alta(self, reserva):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (cliente_id, cancha_id, estado_id, fecha, hora_inicio, hora_fin, servicio_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (reserva.cliente_id, reserva.cancha_id, reserva.estado_id, reserva.fecha, reserva.hora_inicio, reserva.hora_fin, reserva.servicio_id))
        conn.commit()
        # Guardar el ID antes de cerrar la conexión
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def listar(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def listar_id(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def listar_reserva_tipo_cancha(self, tipo_cancha):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*
            FROM reservas r
            JOIN canchas c ON r.cancha_id = c.id
            WHERE c.tipo = ?
        """, (tipo_cancha,))
        result = cursor.fetchall()
        conn.close()
        return result

    def modificar(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservas
            SET estado_id = 4
            WHERE id = ?
        """, (id,))
        conn.commit()
        conn.close()
        
    def adjuntar_torneo(self, reserva_id, torneo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservas
            SET torneo_id = ?
            WHERE id = ?
        """, (torneo_id, reserva_id))
        conn.commit()
        conn.close()
    
    def listar_por_torneo(self, torneo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, servicio_id, torneo_id
            FROM reservas
            WHERE torneo_id = ?
            ORDER BY fecha, hora_inicio
        """, (torneo_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    def borrar(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def cancelar(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE reservas
            SET estado_id = 8
            WHERE id = ?
        """, (id,))
        conn.commit()
        conn.close()
    
    def obtener_estado(self, id_reserva):
        """Devuelve el estado_id de la reserva"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT estado_id FROM reservas WHERE id = ?", (id_reserva,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    #nuevo 
    def horarios_ocupados(self, cancha_id, fecha):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hora_inicio, hora_fin
            FROM reservas
            WHERE cancha_id = ?
            AND fecha = ?
            AND estado_id != 8   -- excluye canceladas
            AND estado_id != 4   -- excluye finalizadas
        """, (cancha_id, fecha))
        
        result = cursor.fetchall()
        conn.close()
        return result

    # Reportes 
    
    # Reserva por cliente 
    def reservas_por_cliente(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.dni, c.nombre, c.apellido, COUNT(*) as total_reservas
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.dni
            GROUP BY c.dni, c.nombre, c.apellido
            ORDER BY total_reservas DESC
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    
    # Reserva por cancha en periodo 
    def reservas_por_cancha_en_periodo(self, fecha_inicio, fecha_fin):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                ? AS fecha_inicio,
                ? AS fecha_fin,
                c.nombre,
                COUNT(*) AS total_reservas
            FROM reservas r
            JOIN canchas c ON r.cancha_id = c.id
            WHERE r.fecha BETWEEN ? AND ?
            GROUP BY r.cancha_id, c.nombre
            ORDER BY total_reservas DESC
        """, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
        result = cursor.fetchall()
        conn.close()
        return result
    
    # Reporte de canchas mas utilizadas
    def canchas_mas_utilizadas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, COUNT(r.id) as total_reservas
            FROM reservas r
            JOIN canchas c ON r.cancha_id = c.id
            GROUP BY c.id, c.nombre
            ORDER BY total_reservas DESC
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    
    # Datos para reporte grafico utilizacion mensual de canchas
    def grafico_utilizacion_mensual_canchas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', r.fecha) as mes, COUNT(r.id) as total_reservas
            FROM reservas r
            GROUP BY mes
            ORDER BY mes
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    
    # Facturacion mensual
    def facturacion_mensual(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', p.fecha_pago) as mes, SUM(p.monto) as total_facturacion
            FROM pagos p
            WHERE p.estado_id = 6
            GROUP BY mes
            ORDER BY mes
        """)
        result = cursor.fetchall()
        conn.close()
        return result

