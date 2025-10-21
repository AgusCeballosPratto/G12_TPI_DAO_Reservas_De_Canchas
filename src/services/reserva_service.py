from dao.reserva_dao import ReservaDAO
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO
from datetime import date

class ReservaService:
    
    # Alta
    def crear_reserva(self, reserva):
        reserva_dao = ReservaDAO()
        cliente_dao = ClienteDAO()
        cancha_dao = CanchaDAO()
        
        # Validaciones 
        
        # Cliente
        cliente_existe = cliente_dao.existe(reserva.cliente_id)
        if not cliente_existe:
            raise ValueError("El cliente no existe.")
            
        # Cancha
        cancha_existe = cancha_dao.existe(reserva.cancha_id)
        if not cancha_existe:
            raise ValueError("La cancha no existe.")
        
        # Hora inicio y Hora fin
        if reserva.hora_inicio >= reserva.hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")
        
        # Fecha 
        fecha_hoy = date.today().strftime("%Y-%m-%d")

        if reserva.fecha < fecha_hoy:
            raise ValueError("La fecha de la reserva no puede ser anterior a la fecha actual.")

        # Disponibilidad
        reserva_disponible = reserva_dao.verificar_disponibilidad(reserva)
        if not reserva_disponible:
            raise ValueError("No hay disponibilidad para la creacion de la reserva.")
        
        # Creacion de la reserva
        reserva_dao.alta(reserva)
        
    # Baja
    def eliminar_reserva_id(self, id_reserva):
        reserva_dao = ReservaDAO()
        
        reserva_existe = reserva_dao.existe(id_reserva)
        if reserva_existe: 
            reserva_dao.borrar(id_reserva)
        else: 
            raise ValueError("No se encontro la reserva.")
    
    # Modificacion
    def finalizar_reserva_id(self, id_reserva):
        reserva_dao = ReservaDAO()
        
        reserva_existe = reserva_dao.existe(id_reserva)
        if not reserva_existe:
            raise ValueError("La reserva con ese ID no existe.")
        
        reserva_dao.modificar(id_reserva)

            
     
    # Consulta (listado y busqueda)
    def mostrar_reservas(self):
        reserva_dao = ReservaDAO()
        reservas = reserva_dao.listar()
        return reservas
    
    def mostrar_reserva_id(self, id_reserva):
        reserva_dao = ReservaDAO()
        reserva = reserva_dao.listar_id(id_reserva)
        return reserva
    
    