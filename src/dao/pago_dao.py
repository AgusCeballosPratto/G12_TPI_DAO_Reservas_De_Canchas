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
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def existe(self, id):
        self.cursor.execute("SELECT * FROM pagos WHERE id = ?", (id,))
        return self.cursor.fetchone() is not None
    
    def alta(self, pago):
        self.cursor.execute("""
            INSERT INTO pagos (reserva_id, monto, fecha_pago, metodo_pago, estado_id, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pago.reserva_id, pago.monto, pago.fecha_pago, pago.metodo_pago, pago.estado_id, pago.cliente_id))
        self.conn.commit()
    
    def listar(self):
        self.cursor.execute("SELECT * FROM pagos")
        return self.cursor.fetchall()
    
    def listar_id(self, id):
        self.cursor.execute("SELECT * FROM pagos WHERE id = ?", (id,))
        return self.cursor.fetchone()

    
    def modificar(self, id, fecha_pago, metodo_pago):
        self.cursor.execute("""
            UPDATE pagos
            SET fecha_pago = ?, metodo_pago = ?, estado_id = 6
            WHERE id = ?
        """, (fecha_pago, metodo_pago, id))
        self.conn.commit()
        
    def borrar(self, id):
        pass
