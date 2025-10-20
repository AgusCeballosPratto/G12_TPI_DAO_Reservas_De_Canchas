import sqlite3
import sys
import os
from dao.base_dao import IBaseDAO
from models.estado import Estado

# Configurar path para encontrar modelos
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_dir)


class EstadoDAO(IBaseDAO):
    def __init__(self, db_path="reservasdecanchas.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tabla()
        
    def existe(self, id):
        pass
    
    def alta(self, estado):
        pass
    
    def listar(self):
        pass
    
    def listar_id(self, id):
        pass
    
    def modificar(self, id, nuevo_nombre):
        pass
    
    def borrar(self, id):
        pass
