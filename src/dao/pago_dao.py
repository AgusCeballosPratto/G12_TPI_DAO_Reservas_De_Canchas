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
        pass
    
    def alta(self, pago):
        self.cursor.execute("""
            INSERT INTO pagos (reserva_id, monto, fecha_pago, metodo_pago, estado_id, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pago.reserva_id, pago.monto, pago.fecha_pago, pago.metodo_pago, pago.estado_id, pago.cliente_id))
        self.conn.commit()
    
    def listar(self):
        pass
    
    def listar_id(self, id):
        pass
    
    def modificar(self, id, nuevo_nombre):
        pass
    
    def borrar(self, id):
        pass
