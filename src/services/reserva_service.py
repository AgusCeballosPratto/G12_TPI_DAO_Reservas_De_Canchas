from dao.reserva_dao import ReservaDAO
from dao.cliente_dao import ClienteDAO
from dao.cancha_dao import CanchaDAO
from dao.pago_dao import PagoDAO
from datetime import date
from dao.servicio_dao import ServicioDAO
from models.pago import Pago
from services.pago_service import PagoService

class ReservaService:
    
    # Alta
    def crear_reserva(self, reserva):
        reserva_dao = ReservaDAO()
        cliente_dao = ClienteDAO()
        cancha_dao = CanchaDAO()
        pago_service = PagoService()
        
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
        
        # Control de servicio de iluminacion con reflectores en cancha
        self.validar_iluminacion_con_reflectores(cancha_dao.listar_id(reserva.cancha_id)[5], reserva.servicio_id)
        
        # Control de hora con servicio de iluminacion 
        if reserva.hora_inicio >= "19:00" and reserva.servicio_id in [1, 3]:
            raise ValueError("Para reservar en horario nocturno, debe seleccionar un servicio con iluminacion.")
        
        # Creacion de la reserva
        id_nueva_reserva = reserva_dao.alta(reserva)
        
        # Creacion del pago asociado a la reserva
        # Crear nueva instancia del DAO para obtener la reserva creada
        reserva_dao_consulta = ReservaDAO()
        reserva_creada = reserva_dao_consulta.listar_id(id_nueva_reserva)
        pago_service.crear_pago(reserva_creada)
        
        
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
    
    def mostrar_reservas_por_torneo(self, torneo_id):
        reserva_dao = ReservaDAO()
        reservas = reserva_dao.listar_por_torneo(torneo_id)
        return reservas
    
    # Validaciones generales
    def validar_iluminacion_con_reflectores(self, tiene_iluminacion, servicio_id):
        if not tiene_iluminacion and servicio_id == 2:
            raise ValueError("No se puede tener el servicio de iluminacion si la cancha no cuenta con reflectores.")
        if not tiene_iluminacion and servicio_id == 4:
            raise ValueError("No se puede tener el servicio completo, ya que la cancha no cuenta con reflectores.")
    
    def asociar_reserva_a_torneo(self, reserva_id, torneo_id):
        reserva_dao = ReservaDAO()
        
        # Verificar que la reserva existe
        reserva_existe = reserva_dao.existe(reserva_id)
        if not reserva_existe:
            raise ValueError("La reserva con ese ID no existe.")
        
        # Asociar la reserva al torneo
        reserva_dao.adjuntar_torneo(reserva_id, torneo_id)
        
    
        
   
    