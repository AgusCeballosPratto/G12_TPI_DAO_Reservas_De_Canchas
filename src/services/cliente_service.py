from dao.cliente_dao import ClienteDAO
import re

class ClienteService():   
    
    # Alta 
    def crear_cliente(self, cliente):
        cliente_dao = ClienteDAO()
        
        # Validaciones

        # Email
        self.validar_email(cliente.email)
        
        # Telefono 
        self.validar_telefono(cliente.telefono)
        
        # DNI 
        cliente_existe = cliente_dao.existe(cliente.dni)
        if cliente_existe:
            raise ValueError("El cliente con ese DNI ya existe.")
        if not cliente.dni:
            raise ValueError("El DNI no puede estar vacío.")
        dni_limpio = cliente.dni.strip()
        if not (dni_limpio.isdigit() and 7 <= len(dni_limpio) <= 8):
            raise ValueError("El DNI debe ser un número de 7 u 8 dígitos.")

        # Nombre y Apellido
        if not cliente.nombre or not cliente.apellido:
            raise ValueError("El nombre y apellido no pueden estar vacíos.")
        
        
        # Creacion del cliente
        cliente_dao.alta(cliente)
    
        
    
    # Baja
    def eliminar_cliente_id(self, dni):
        cliente_dao = ClienteDAO()
        
        cliente_existe = cliente_dao.existe(dni)
        if cliente_existe: 
            cliente_dao.borrar(dni)
        else: 
            raise ValueError("No se encontro el cliente.")
    
    # Consulta (listado y busqueda)
    def mostrar_clientes(self):
        cliente_dao = ClienteDAO()
        clientes = cliente_dao.listar()
        for cliente in clientes:
            print(cliente) # borrar despues
    
    def mostrar_cliente_id(self, id_cliente):
        cliente_dao = ClienteDAO()
        cliente = cliente_dao.listar_id(id_cliente)
        print(cliente) #borrar despues
    
    # Modificacion
    def modificar_cliente_id(self, id_cliente):
        cliente_dao = ClienteDAO()
        
        cliente_existe = cliente_dao.existe(id_cliente)
        if not cliente_existe:
            raise ValueError("El cliente con ese DNI no existe.")
        
        email = input("Nuevo email: ") # borrar despues
        telefono = int(input("Nuevo telefono: ")) # borrar despues
        self.validar_email(email)
        self.validar_telefono(telefono)
        cliente_dao.modificar(id_cliente, email, telefono)
        
    # Validaciones generales
    
    def validar_email(self, email):
        if not email:
            raise ValueError("El email no puede estar vacío.")
        patron = r'^[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        if not re.match(patron, email.strip()):
            raise ValueError("El email no tiene un formato válido.")
        
    def validar_telefono(self, telefono):
        if not telefono:
            raise ValueError("El teléfono no puede estar vacío.")
        telefono_limpio = re.sub(r'[^\d]', '', telefono)
        if not (8 <= len(telefono_limpio) <= 15):
            raise ValueError("El teléfono debe tener entre 8 y 15 dígitos.")
        
        