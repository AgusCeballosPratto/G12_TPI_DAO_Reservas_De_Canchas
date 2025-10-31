class Pago:
    def __init__(self, reserva_id, monto, cliente_id):
        self.reserva_id = reserva_id
        self.monto = monto
        self.fecha_pago = "Sin definir"
        self.metodo_pago = "Sin definir"
        self.estado_id = 5
        self.cliente_id = cliente_id