from models.torneo import Torneo
from dao.torneo_dao import TorneoDAO
from dao.reserva_dao import ReservaDAO

class TorneoService:
    
    # Alta 
    def crear_torneo(self, torneo):
        torneo_dao = TorneoDAO()
        reserva_dao = ReservaDAO()
        
        # Validaciones 
        
        # Nombre no vacio ni repetido
        if not torneo.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        
        torneo_existe = torneo_dao.existe_nombre(torneo.nombre)
        if torneo_existe:
            raise ValueError("El torneo con ese nombre ya existe.")
        
        # Tipo
        if torneo.tipo not in ["Futbol", "Tenis", "Padel"]:
            raise ValueError("El tipo de torneo no es válido.")
        
        # Busqueda de reservas con tipo de cancha igual al tipo de torneo
        reservas_que_puedo_asociar_a_torneo = reserva_dao.listar_reserva_tipo_cancha(torneo.tipo)
        print(reservas_que_puedo_asociar_a_torneo) # borrar despues (se mostraria en la interfaz)
        reservas_por_asociar = []

        while True: # Menu provisorio para validar backend, borrar despues 
            print("1. Asociar una reserva al torneo")
            print("2. Salir")
            opcion = int(input("Seleccione una opción: "))
            
            if opcion == 1:
                id_reserva_a_asociar = int(input("Ingrese el ID de la reserva a asociar: "))
                reservas_por_asociar.append(id_reserva_a_asociar)
                
            elif opcion == 2:
                break
            
            else:
                print("Opción no válida. Intente de nuevo.")
                
        # Obtener menor fecha de inicio y mayor fecha de inicio entre las reservas asociadas
        fechas = set()
        for reserva_id in reservas_por_asociar:
            reserva = reserva_dao.listar_id(reserva_id)
            fechas.add(reserva[3])

        fechas = sorted(fechas)
        
        torneo.fecha_inicio = fechas[0]
        torneo.fecha_fin = fechas[-1]
                 
        # Creacion del torneo
        torneo_dao.alta(torneo)
        
        # Asignacion del torneo creado a las reservas
        id_ultimo_torneo = torneo_dao.cursor.lastrowid
        reservas_a_asociar = [list(reserva_dao.listar_id(reserva_id)) for reserva_id in reservas_por_asociar]
        for reserva in reservas_a_asociar:
            reserva[8] = id_ultimo_torneo
            reserva_dao.adjuntar_torneo(reserva[0], id_ultimo_torneo)
    
    # Baja
    def eliminar_torneo_id(self, id_torneo):
        torneo_dao = TorneoDAO()
        
        torneo_existe = torneo_dao.existe(id_torneo)
        if torneo_existe: 
            torneo_dao.borrar(id_torneo)
        else: 
            raise ValueError("No se encontro el torneo.")  
        