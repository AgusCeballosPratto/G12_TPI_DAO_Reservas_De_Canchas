from src.services.reserva_service import ReservaService
from src.services.cancha_service import CanchaService
from src.services.cliente_service import ClienteService
from src.services.torneo_service import TorneoService
from src.services.pago_service import PagoService
from src.reports.reportes import ReportesService


class ControladorReservas:
    def __init__(self):
        self.reserva_service = ReservaService()
        self.cancha_service = CanchaService()
        self.cliente_service = ClienteService()
        self.torneo_service = TorneoService()
        self.pagos_service = PagoService()
        self.reportes_service = ReportesService()
    
    # Métodos para Reservas
    def crear_reserva(self, reserva):
        return self.reserva_service.crear_reserva(reserva)
    
    def obtener_reserva(self, id_reserva):
        return self.reserva_service.mostrar_reserva_id(id_reserva)
    
    def listar_reservas(self):
        return self.reserva_service.mostrar_reservas()
    
    def finalizar_reserva(self, id_reserva):
        return self.reserva_service.finalizar_reserva_id(id_reserva)
    
    def eliminar_reserva(self, id_reserva):
        return self.reserva_service.eliminar_reserva_id(id_reserva)
    
    def modificar_reserva(self, id_reserva):
        return self.reserva_service.finalizar_reserva_id(id_reserva)
    
    # Métodos para Canchas
    def crear_cancha(self, cancha):
        return self.cancha_service.crear_cancha(cancha)
    
    def obtener_cancha(self, id_cancha):
        return self.cancha_service.mostrar_cancha_id(id_cancha)
    
    def listar_canchas(self):
        return self.cancha_service.mostrar_canchas()
    
    def modificar_cancha(self, id_cancha):
        return self.cancha_service.modificar_cancha_id(id_cancha)
    
    def eliminar_cancha(self, id_cancha):
        return self.cancha_service.eliminar_cancha_id(id_cancha)

    def mostrar_cancha_iluminacion(self):
        return self.cancha_service.mostrar_cancha_iluminacion()
    
    def mostrar_cancha_nombre(self, nombre):
        return self.cancha_service.mostrar_cancha_nombre(nombre)
    
    
    # Métodos para Clientes
    def crear_cliente(self, cliente):
        return self.cliente_service.crear_cliente(cliente)
    
    def obtener_cliente(self, id_cliente):
        return self.cliente_service.mostrar_cliente_id(id_cliente)
    
    def listar_clientes(self):
        return self.cliente_service.mostrar_clientes()
    
    def modificar_cliente(self, id_cliente):
        return self.cliente_service.modificar_cliente_id(id_cliente)
    
    def eliminar_cliente(self, dni):
        return self.cliente_service.eliminar_cliente_id(dni)
    
    # Pagos
    def mostrar_pagos(self):
        return self.pagos_service.mostrar_pagos()
    
    def mostrar_pagos_id(self, id):
        return self.pagos_service.mostrar_pago_id(id)
    
    def mostrar_reservas_pagadas(self):
        return self.pagos_service.mostrar_reservas_pagadas()
    
    def mostrar_reservas_pendientes_pagos(self):
        return self.pagos_service.mostrar_reservas_pendientes_pago()
    
    def mostrar_pago_de_metodo(self, metodo_pago):
        return self.pagos_service.mostrar_pago_de_metodo_pago(metodo_pago)
    
    def abonar_pago(self, id_pago, metodo_pago):
        return self.pagos_service.abonar_pago(id_pago, metodo_pago)
    
    def calcular_monto_reserva(self, reserva):
        return self.pagos_service.calcular_monto_reserva(reserva)
    
    # Torneos
    def crear_torneo(self, torneo):
        return self.torneo_service.crear_torneo(torneo)

    def eliminar_torneo_id(self, id_torneo):
        return self.torneo_service.eliminar_torneo_id(id_torneo)
    
    def mostrar_torneos(self):
        return self.torneo_service.mostrar_torneos()
    
    def mostrar_torneos_nombre(self, nombre):
        return self.torneo_service.mostrar_torneo_nombre(nombre)
    
    # Reportes
    def reservas_por_cliente(self):
        return self.reportes_service.reservas_por_cliente()
    
    def reservas_por_cancha_en_periodo(self, fecha_inicio, fecha_fin):
        return self.reportes_service.reservas_por_cancha_en_periodo(fecha_inicio, fecha_fin)
    
    def canchas_mas_utilizadas(self):
        return self.reportes_service.canchas_mas_utilizadas()
    
    def grafico_utilizacion_mensual_canchas(self):
        return self.reportes_service.grafico_utilizacion_mensual_canchas()
    
    def facturacion_mensual(self):
        return self.reportes_service.facturacion_mensual()
    

def controlador_reservas():
    return ControladorReservas()