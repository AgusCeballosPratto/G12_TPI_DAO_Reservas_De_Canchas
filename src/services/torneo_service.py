from models.torneo import Torneo
from dao.torneo_dao import TorneoDAO
from dao.reserva_dao import ReservaDAO

class TorneoService:
    
    # Alta 
    def crear_torneo(self, torneo, reservas_ids=None):
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
        
        # Si se proporcionan reservas, calcular fechas de inicio y fin
        if reservas_ids and len(reservas_ids) > 0:
            # Obtener fechas de las reservas seleccionadas
            fechas = set()
            for reserva_id in reservas_ids:
                reserva = reserva_dao.listar_id(reserva_id)
                if reserva:
                    fechas.add(reserva[3])  # reserva[3] es la fecha
            
            if fechas:
                fechas_ordenadas = sorted(fechas)
                torneo.fecha_inicio = fechas_ordenadas[0]
                torneo.fecha_fin = fechas_ordenadas[-1]
            else:
                torneo.fecha_inicio = "Sin definir"
                torneo.fecha_fin = "Sin definir"
        else:
            # Si no hay reservas, usar fechas por defecto
            torneo.fecha_inicio = "Sin definir"
            torneo.fecha_fin = "Sin definir"
                 
        # Creacion del torneo
        torneo_dao.alta(torneo)
        
        # Obtener el ID del torneo recién creado
        id_torneo = torneo_dao.cursor.lastrowid if hasattr(torneo_dao, 'cursor') else None
        
        # Si se proporcionaron reservas, asociarlas al torneo
        if reservas_ids and id_torneo:
            for reserva_id in reservas_ids:
                reserva_dao.adjuntar_torneo(reserva_id, id_torneo)
        
        return id_torneo
    
    # Baja
    def eliminar_torneo_id(self, id_torneo):
        torneo_dao = TorneoDAO()
        
        torneo_existe = torneo_dao.existe(id_torneo)
        if torneo_existe: 
            torneo_dao.borrar(id_torneo)
        else: 
            raise ValueError("No se encontro el torneo.")  
        
    # Consulta (listado y busqueda)
    def mostrar_torneos(self):
        torneo_dao = TorneoDAO()
        torneos = torneo_dao.listar()
        return torneos
    
    def mostrar_torneo_nombre(self, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        
        torneo_dao = TorneoDAO()
        torneo = torneo_dao.listar_nombre(nombre)
        return torneo
    
    def asociar_reserva_a_torneo(self, reserva_id, torneo_id):
        reserva_dao = ReservaDAO()
        
        # Verificar que la reserva y el torneo existen
        reserva = reserva_dao.listar_id(reserva_id)
        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID {reserva_id}")
        
        torneo_dao = TorneoDAO()
        if not torneo_dao.existe(torneo_id):
            raise ValueError(f"No se encontró el torneo con ID {torneo_id}")
        
        # Asociar la reserva al torneo
        reserva_dao.adjuntar_torneo(reserva_id, torneo_id)
        
        return True
