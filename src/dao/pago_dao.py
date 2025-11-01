import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.pago import Pago

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)


class PagoDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.db_path = db_path
        
    def existe(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pagos WHERE id = ?", (id,))
        result = cursor.fetchone() is not None
        conn.close()
        return result
    
    def alta(self, pago):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagos (reserva_id, monto, fecha_pago, metodo_pago, estado_id, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pago.reserva_id, pago.monto, pago.fecha_pago, pago.metodo_pago, pago.estado_id, pago.cliente_id))
        conn.commit()
        conn.close()
    
    def listar(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pagos")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def listar_id(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pagos WHERE id = ?", (id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def listar_reservas_pagadas(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*
            FROM reservas r
            JOIN pagos p ON r.id = p.reserva_id
            WHERE p.estado_id = 6
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def listar_reservas_pendientes_pago(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*
            FROM reservas r
            JOIN pagos p ON r.id = p.reserva_id
            WHERE p.estado_id = 5
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def listar_pago_de_metodo_pago(self, metodo_pago):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM pagos
            WHERE metodo_pago = ?
        """, (metodo_pago,))
        result = cursor.fetchall()
        conn.close()
        return result

    
    def modificar(self, id, fecha_pago, metodo_pago):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pagos
            SET fecha_pago = ?, metodo_pago = ?, estado_id = 6
            WHERE id = ?
        """, (fecha_pago, metodo_pago, id))
        conn.commit()
        conn.close()
        
    def borrar(self, id):
        pass
