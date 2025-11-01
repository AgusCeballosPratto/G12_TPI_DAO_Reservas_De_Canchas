from dao.cancha_dao import CanchaDAO

class CanchaService:
    
    # Alta 
    def crear_cancha(self, cancha):
        cancha_dao = CanchaDAO()
        
        # Validaciones 
        
        # Nombre
        self.validar_nombre(cancha.nombre)

        # Tipo (Futbol, Tenis, Padel)
        self.validar_tipo(cancha.tipo)
        
        # Costo 
        self.validar_costo_por_hora(cancha.costo_por_hora)
        
        # Creacion de la cancha
        cancha_dao.alta(cancha)

    # Baja
    def eliminar_cancha_id(self, id_cancha):
        cancha_dao = CanchaDAO()
        
        cancha_existe = cancha_dao.existe(id_cancha)
        if cancha_existe: 
            cancha_dao.borrar(id_cancha)
        else: 
            raise ValueError("No se encontro la cancha.")
    
    # Modificacion
    def modificar_cancha_id(self, id_cancha):
        cancha_dao = CanchaDAO()
        
        cancha_existe = cancha_dao.existe(id_cancha)
        if not cancha_existe:
            raise ValueError("La cancha con ese ID no existe.")
        
        nombre = input("Nuevo nombre: ") # borrar despues
        tipo = input("Nuevo tipo: ") # borrar despues
        costo_por_hora = float(input("Nuevo costo: ")) # borrar despues
        
        self.validar_nombre(nombre)
        self.validar_tipo(tipo)
        self.validar_costo_por_hora(costo_por_hora)
        cancha_dao.modificar(id_cancha, nombre, tipo, costo_por_hora)
        
    
    # Consulta (listado y busqueda)
    def mostrar_canchas(self):
        cancha_dao = CanchaDAO()
        canchas = cancha_dao.listar()
        return canchas
    
    def mostrar_cancha_id(self, id_cancha):
        cancha_dao = CanchaDAO()
        cancha = cancha_dao.listar_id(id_cancha)
        return cancha
    
    # Validaciones generales
    def validar_nombre(self, nombre):
        cancha_dao = CanchaDAO()
        
        if not nombre:
            raise ValueError("El nombre de la cancha no puede estar vacío.")
        
        cancha_existe = cancha_dao.existe_nombre(nombre)
        if cancha_existe:
            raise ValueError("Ya existe una cancha con ese nombre.")
        
    def validar_tipo(self, tipo):
        if not tipo:
            raise ValueError("El tipo de la cancha no puede estar vacío.")
        if tipo not in ["Futbol", "Tenis", "Padel"]:
            raise ValueError("El tipo de la cancha debe ser 'Futbol', 'Tenis' o 'Padel'.")
        
    def validar_costo_por_hora(self, costo_por_hora):
        if costo_por_hora <= 0:
            raise ValueError("El costo por hora debe ser un número positivo.")
    
    