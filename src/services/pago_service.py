from dao.pago_dao import PagoDAO
from dao.cancha_dao import CanchaDAO
from dao.servicio_dao import ServicioDAO
from dao.reserva_dao import ReservaDAO
from models.pago import Pago
from dao.pago_dao import PagoDAO
from datetime import date

class PagoService:
    def crear_pago(self, reserva):
        pago_dao = PagoDAO()
        
        # Creacion del pago de la reserva
        
        # a. Calculo del monto a pagar
        monto = self.calcular_monto_reserva(reserva)
        
        # b. Creacion del objeto Pago
        pago = Pago(reserva[0], monto, reserva[1])
        pago_dao.alta(pago)
    
    # Consulta (listado y busqueda)
    def mostrar_pagos(self):
        pago_dao = PagoDAO()
        pagos = pago_dao.listar()
        return pagos
    
    def mostrar_pago_id(self, id):
        pago_dao = PagoDAO()
        pago = pago_dao.listar_id(id)
        return pago
    
    def mostrar_reservas_pagadas(self):
        pago_dao = PagoDAO()
        reservas_pagadas = pago_dao.listar_reservas_pagadas()
        return reservas_pagadas
    
    def mostrar_reservas_pendientes_pago(self):
        pago_dao = PagoDAO()
        reservas_pendientes_pago = pago_dao.listar_reservas_pendientes_pago()
        return reservas_pendientes_pago
    
    def mostrar_pago_de_metodo_pago(self, metodo_pago):
        pago_dao = PagoDAO()
        pagos_de_metodo_pago = pago_dao.listar_pago_de_metodo_pago(metodo_pago)
        return pagos_de_metodo_pago
    
    #nuevo: 
    def esta_pagado(self, reserva_id):
        pago_dao = PagoDAO()
        return pago_dao.pago_esta_pagado(reserva_id)

    # Modificacion
    def abonar_pago(self, id_pago, metodo_pago):
        """Abonar un pago específico con un método de pago dado"""
        pago_dao = PagoDAO()
        
        # Verificar que el pago existe
        pago_existe = pago_dao.existe(id_pago)
        if not pago_existe:
            raise ValueError("El pago con ese ID no existe.")
        
        # Obtener fecha actual
        fecha_pago = date.today().strftime("%Y-%m-%d")
        
        # Modificar el pago
        pago_dao.modificar(id_pago, fecha_pago, metodo_pago)
        
        
    # Validaciones generales
    def calcular_monto_reserva(self, reserva):
        cancha_dao = CanchaDAO()
        servicio_dao = ServicioDAO()
        
        cancha_de_reserva = cancha_dao.listar_id(reserva[2])
        costo_por_hora_de_cancha_de_reserva = cancha_de_reserva[3]
        adicional_por_servicio = servicio_dao.listar_id(reserva[7])[2]
        
        return costo_por_hora_de_cancha_de_reserva + adicional_por_servicio
        