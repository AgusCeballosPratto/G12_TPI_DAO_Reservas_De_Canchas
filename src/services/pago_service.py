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
    
    # Modificacion
    def abonar_pago(self):
        pago_dao = PagoDAO()
        metodos_de_pago = ["Tarjeta de credito", "Tarjeta de debito", "Efectivo", "Transferencia"] # borrar despues (se seleccionaria desde la interfaz)
        
        print(self.mostrar_pagos()) # borrar despues (se mostraria en la interfaz)
        
        id_pago_seleccionado = int(input("Seleccione el pago a abonar (ingrese el numero de id correspondiente): ")) # borrar despues (se seleccionaria desde la interfaz)
        metodo_de_pago_seleccionado = int(input("Seleccione el metodo de pago (ingrese el numero correspondiente): ")) # borrar despues (se seleccionaria desde la interfaz)
        
        self.fecha_pago = date.today().strftime("%Y-%m-%d")
        self.metodo_pago = metodos_de_pago[metodo_de_pago_seleccionado]
        
        pago_existe = pago_dao.existe(id_pago_seleccionado)
        if not pago_existe:
            raise ValueError("El pago con ese ID no existe.")
        
        pago_dao.modificar(id_pago_seleccionado, self.fecha_pago, self.metodo_pago)
        
        
    # Validaciones generales
    def calcular_monto_reserva(self, reserva):
        cancha_dao = CanchaDAO()
        servicio_dao = ServicioDAO()
        
        cancha_de_reserva = cancha_dao.listar_id(reserva[2])
        costo_por_hora_de_cancha_de_reserva = cancha_de_reserva[3]
        adicional_por_servicio = servicio_dao.listar_id(reserva[7])[2]
        
        return costo_por_hora_de_cancha_de_reserva + adicional_por_servicio
        