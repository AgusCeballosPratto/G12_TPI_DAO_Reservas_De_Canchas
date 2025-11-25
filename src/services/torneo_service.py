from models.torneo import Torneo
from models.reserva import Reserva
from dao.torneo_dao import TorneoDAO
from dao.reserva_dao import ReservaDAO


class TorneoService:
    CLIENTE_TORNEO = 99999999  # Cliente especial para torneos  
    SERVICIO_TORNEO = 1  # Servicio sin para torneos
    def crear_torneo(self, torneo, canchas_ids, fecha, hora_inicio, hora_fin):
        torneo_dao = TorneoDAO()
        reserva_dao = ReservaDAO()

        # VALIDACIONES BÁSICAS
        if not torneo.nombre:
            raise ValueError("El nombre del torneo no puede estar vacío.")

        if torneo_dao.existe_nombre(torneo.nombre):
            raise ValueError("El torneo con ese nombre ya existe.")

        if torneo.tipo not in ["Futbol", "Tenis", "Padel"]:
            raise ValueError("El tipo de torneo no es válido.")

        # FECHA DEL TORNEO (misma para inicio y fin)
        torneo.fecha_inicio = fecha
        torneo.fecha_fin = fecha

        # CREAR TORNEO
        id_torneo = torneo_dao.alta(torneo)

        # CREAR RESERVAS AUTOMÁTICAS PARA CADA CANCHA
        for cancha_id in canchas_ids:
            nueva_reserva = Reserva(
                cliente_id=self.CLIENTE_TORNEO,
                cancha_id=cancha_id,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                servicio_id=self.SERVICIO_TORNEO
            )
            nueva_reserva.torneo_id = id_torneo
            reserva_dao.alta(nueva_reserva)

        return id_torneo

    # ------------------------------
    # RESTO DE LOS MÉTODOS ORIGINALES
    # ------------------------------

    def eliminar_torneo_id(self, id_torneo):
        torneo_dao = TorneoDAO()

        if torneo_dao.existe(id_torneo):
            torneo_dao.borrar(id_torneo)
        else:
            raise ValueError("No se encontró el torneo.")

    def mostrar_torneos(self):
        return TorneoDAO().listar()

    def mostrar_torneo_nombre(self, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        return TorneoDAO().listar_nombre(nombre)
