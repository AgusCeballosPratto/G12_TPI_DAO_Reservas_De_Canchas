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

# Importaciones de modelos
from models.cliente import Cliente
from models.cancha import Cancha
from models.reserva import Reserva

# Importaciones de los services 
from services.cliente_service import ClienteService
from services.cancha_service import CanchaService
from services.reserva_service import ReservaService

# Import de controlador
from controller.controlador_reservas import ControladorReservas

# Agregar el directorio src al path para importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    # Creacion de la base de datos, tablas y datos iniciales
    init_database()
    
    # Inicializacion del controlador
    controlador = ControladorReservas()
    
    # Inicializacion de los services
    cliente_service = ClienteService()
    reserva_service = ReservaService()
    cancha_service = CanchaService()
    
    # Inicializacion de los modelos
    cliente_1 = Cliente("12345678", "MARIA", "Wendler", "juan@gmail.com", "12345678")
    cancha_1 = Cancha("Cancha Central", "Futbol", 5000, True)
    reserva_1 = Reserva("12345678", 1, "2025-11-11", "14:00", "17:00", 2)
    reserva_2 = Reserva("98765432", 1, "2025-12-24", "16:10", "17:00")
    
    # Reportes
    #controlador.reservas_por_cliente()
    #controlador.reservas_por_cancha_en_periodo("2024-10-01", "2025-10-23")
    #controlador.canchas_mas_utilizadas()
    #controlador.grafico_utilizacion_mensual_canchas()
    
    # ABMC Reserva

    # Alta
    reserva_service.crear_reserva(reserva_1)
    #reserva_service.crear_reserva(reserva_2)
    #reserva_service.crear_reserva(reserva_1)
    
    # Baja
    #reserva_service.eliminar_reserva_id(7)
     
    # Modificacion
    #reserva_service.finalizar_reserva_id(1)
    
    # Consulta (listado y busqueda)
    #reserva_service.mostrar_reservas()
    #reserva_service.mostrar_reserva_id(6)
    
    
    
    
    # ABMC Cancha
    
    # Alta
    #cancha_service.crear_cancha(cancha_1)
    
    # Baja 
    # cancha_service.eliminar_cancha_id(1)
    
    # Modificacion
    # cancha_service.modificar_cancha_id(2)
    
    # Consulta (listado y busqueda)
    #cancha_service.mostrar_canchas()
    #cancha_service.mostrar_cancha_id(2)
    
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
    #cliente_service.mostrar_cliente_id("11")
    
    
    
    
    
    
if __name__ == "__main__":
    main()