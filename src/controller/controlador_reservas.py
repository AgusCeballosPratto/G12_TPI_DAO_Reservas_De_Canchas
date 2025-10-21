from src.services.reserva_service import ReservaService
from src.services.cancha_service import CanchaService
from src.services.cliente_service import ClienteService
from src.reports.reportes import ReportesService

class ControladorReservas:
    def __init__(self):
        self.reserva_service = ReservaService()
        self.cancha_service = CanchaService()
        self.cliente_service = ClienteService()
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
    
    # Reportes
    def reservas_por_cliente(self):
        return self.reportes_service.reservas_por_cliente()
    
    def reservas_por_cancha_en_periodo(self):
        pass
    
    def canchas_mas_utilizadas(self):
        pass
    
    def grafico_utilizacion_mensual_canchas(self):
        pass

def controlador_reservas():
    return ControladorReservas()