class Reserva:
    def __init__(self, id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, tiene_iluminacion, tiene_arbitro):
        self.id = id
        self.cliente_id = cliente_id
        self.cancha_id = cancha_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado_id = estado_id
        self.tiene_iluminacion = tiene_iluminacion
        self.tiene_arbitro = tiene_arbitro
