class Torneo:
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, tipo, reservas=None):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo
        self.reservas = reservas if reservas is not None else []
