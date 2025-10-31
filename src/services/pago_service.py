from dao.pago_dao import PagoDAO
from dao.cancha_dao import CanchaDAO
from dao.servicio_dao import ServicioDAO
from dao.reserva_dao import ReservaDAO
from models.pago import Pago
from dao.pago_dao import PagoDAO

class PagoService:
    def crear_pago(self, reserva):
        pago_dao = PagoDAO()
        
        # Creacion del pago de la reserva
        
        # a. Calculo del monto a pagar
        monto = self.calcular_monto_reserva(reserva)
        
        # b. Creacion del objeto Pago
        pago = Pago(reserva[0], monto, reserva[1])
        pago_dao.alta(pago)
    
    # Validaciones generales
    def calcular_monto_reserva(self, reserva):
        cancha_dao = CanchaDAO()
        servicio_dao = ServicioDAO()
        
        cancha_de_reserva = cancha_dao.listar_id(reserva[2])
        costo_por_hora_de_cancha_de_reserva = cancha_de_reserva[3]
        adicional_por_servicio = servicio_dao.listar_id(reserva[7])[2]
        
        return costo_por_hora_de_cancha_de_reserva + adicional_por_servicio
        