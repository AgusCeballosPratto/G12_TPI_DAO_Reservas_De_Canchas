class Pago:
    def __init__(self, id, estado_id, monto, fecha_pago, metodo):
        self.id = id
        self.estado_id = estado_id
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.metodo = metodo
