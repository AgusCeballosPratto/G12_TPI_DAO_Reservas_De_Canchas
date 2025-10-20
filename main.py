#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importaciones estándar
import sys
import os

# Configurar paths
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
config_dir = os.path.join(current_dir, 'config')

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, config_dir)

# Importaciones de configuración de la BD
from config.database_config import init_database

# Importaciones de DAOs
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO  
from dao.reserva_dao import ReservaDAO
from dao.estado_dao import EstadoDAO

# Importaciones de modelos
from models.cliente import Cliente
from models.cancha import Cancha
from models.reserva import Reserva

# Importaciones de los services 
from services.cliente_service import ClienteService
#from services.cancha_service import CanchaService
#from services.reserva_service import ReservaService

# Agregar el directorio src al path para importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    # Creacion de la base de datos, tablas y datos iniciales
    init_database()
    
    # Inicializacion de los services
    cliente_service = ClienteService()
    #reserva_service = ReservaService()
    #cancha_service = CanchaService()
    
    # Inicializacion de los modelos
    cliente_1 = Cliente("98765432", "PEDRO", "Wendler", "juan@gmail.com", "12345678")
    
    # ABMC Cliente
    
    # Alta
    
    #cliente_service.crear_cliente(cliente_1)    
    #cliente_service.crear_cliente(cliente_2)
    
    # Baja 
    #cliente_service.eliminar_cliente_id("18674323")
    
    # Modificacion
    # cliente_service.modificar_cliente_id("98765432")
    
    # Consulta (listado y busqueda)
    # listado
    #cliente_service.mostrar_clientes()
    # busqueda
    #cliente_service.mostrar_cliente_id("9812312")
    # ABMC Reserva
    
    # Alta
    # Baja 
    # Modificacion
    # Consulta (listado y busqueda)
    
    # ABMC Cancha
    
    # Alta
    # Baja 
    # Modificacion
    # Consulta (listado y busqueda)
    
    
    
    
if __name__ == "__main__":
    main()