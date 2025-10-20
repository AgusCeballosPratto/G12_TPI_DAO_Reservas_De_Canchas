class Reserva:
    def __init__(self, id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, servicio_id, estado_id=1):
        self.id = id
        self.cliente_id = cliente_id
        self.cancha_id = cancha_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.servicio_id = servicio_id
        self.estado_id = estado_id
