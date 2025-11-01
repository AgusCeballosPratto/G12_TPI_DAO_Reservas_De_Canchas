"""
Métodos auxiliares para la GUI que adaptan los servicios existentes
"""
import sys
import os
from datetime import date

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from database_manager import DatabaseManager
from services.cliente_service import ClienteService
from services.cancha_service import CanchaService

class GUIHelpers:
    """Métodos auxiliares para adaptar servicios a la GUI"""
    
    @staticmethod
    def modificar_cliente_gui(dni, nuevo_email, nuevo_telefono):
        """Modificar cliente desde la GUI"""
        db_manager = DatabaseManager()
        cliente_service = ClienteService()
        
        # Verificar que existe
        query_existe = "SELECT * FROM clientes WHERE dni = ?"
        cliente_existe = db_manager.execute_query(query_existe, (dni,), fetch='one')
        
        if not cliente_existe:
            raise ValueError("El cliente con ese DNI no existe.")
        
        # Validar con los métodos del servicio
        cliente_service.validar_email(nuevo_email)
        cliente_service.validar_telefono(nuevo_telefono)
        
        # Modificar
        query_update = """
            UPDATE clientes 
            SET email = ?, telefono = ? 
            WHERE dni = ?
        """
        db_manager.execute_query(query_update, (nuevo_email, nuevo_telefono, dni))
    
    @staticmethod
    def modificar_cancha_gui(id_cancha, nuevo_nombre, nuevo_tipo, nuevo_costo):
        """Modificar cancha desde la GUI"""
        db_manager = DatabaseManager()
        cancha_service = CanchaService()
        
        # Verificar que existe
        query_existe = "SELECT * FROM canchas WHERE id = ?"
        cancha_existe = db_manager.execute_query(query_existe, (id_cancha,), fetch='one')
        
        if not cancha_existe:
            raise ValueError("La cancha con ese ID no existe.")
        
        # Validar costo
        cancha_service.validar_costo_por_hora(nuevo_costo)
        
        # Validar tipo
        if nuevo_tipo not in ["Futbol", "Tenis", "Padel"]:
            raise ValueError("El tipo de la cancha debe ser 'Futbol', 'Tenis' o 'Padel'.")
        
        # Modificar
        query_update = """
            UPDATE canchas 
            SET nombre = ?, tipo = ?, costo_por_hora = ? 
            WHERE id = ?
        """
        db_manager.execute_query(query_update, (nuevo_nombre, nuevo_tipo, nuevo_costo, id_cancha))
    
    @staticmethod
    def abonar_pago_gui(id_pago, metodo_pago):
        """Abonar pago desde la GUI"""
        db_manager = DatabaseManager()
        
        # Verificar que el pago existe
        query_existe = "SELECT * FROM pagos WHERE id = ?"
        pago_existe = db_manager.execute_query(query_existe, (id_pago,), fetch='one')
        
        if not pago_existe:
            raise ValueError("El pago con ese ID no existe.")
        
        # Obtener fecha actual
        fecha_pago = date.today().strftime("%Y-%m-%d")
        
        # Modificar el pago
        query_update = """
            UPDATE pagos 
            SET fecha_pago = ?, metodo_pago = ?, estado_id = 6 
            WHERE id = ?
        """
        db_manager.execute_query(query_update, (fecha_pago, metodo_pago, id_pago))