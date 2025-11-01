import sqlite3

# Creacion de todas las tablas 
def crear_tablas(cursor):
    """Crear todas las tablas necesarias para el sistema"""
    
    # Tabla servicios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            costo REAL NOT NULL
        )
    """)
    
    # Tabla estados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ambito INTEGER NOT NULL
        )
    """)
    
    # Tabla clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            dni INTEGER PRIMARY KEY,
            nombre TEXT,
            apellido TEXT,
            email TEXT,
            telefono INTEGER
        )
    """)
    
    # Tabla canchas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canchas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            costo_por_hora REAL,
            estado_id INTEGER NOT NULL,
            tiene_iluminacion BOOLEAN DEFAULT 0,
            FOREIGN KEY(estado_id) REFERENCES estados(id)
        )
    """)
    
    # Tabla reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            cancha_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            estado_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            torneo_id INTEGER,
            FOREIGN KEY(cliente_id) REFERENCES clientes(dni),
            FOREIGN KEY(cancha_id) REFERENCES canchas(id),
            FOREIGN KEY(estado_id) REFERENCES estados(id),
            FOREIGN KEY(servicio_id) REFERENCES servicios(id),
            FOREIGN KEY(torneo_id) REFERENCES torneos(id)
        )
    """)
    
    # Tabla pagos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reserva_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            fecha_pago TEXT DEFAULT 'Sin definir',
            estado_id INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL,
            metodo_pago TEXT DEFAULT 'Sin definir',
            FOREIGN KEY(reserva_id) REFERENCES reservas(id),
            FOREIGN KEY(estado_id) REFERENCES estados(id),
            FOREIGN KEY(cliente_id) REFERENCES clientes(dni)    
        )
    """)
    
    # Tabla torneos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS torneos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            tipo TEXT NOT NULL
        )
    """)

# Inicializacion de datos para la tabla estados y servicios
def insertar_datos_iniciales(cursor, conn):
    try:
        cursor.execute("SELECT COUNT(*) FROM estados")
        if cursor.fetchone()[0] == 0:
            estados_iniciales = [
                ('Libre', '2'),        
                ('Ocupada', '2'),      
                ('Activa', '1'),       
                ('Finalizada', '1'),
                ('Pendiente de pago', '3'),
                ('Pagada', '3') 
            ]
            
            cursor.executemany("""
                INSERT INTO estados (nombre, ambito) VALUES (?, ?)
            """, estados_iniciales)
        
        cursor.execute("SELECT COUNT(*) FROM servicios")
        if cursor.fetchone()[0] == 0:
            servicios_iniciales = [
                ('Sin Servicio', 0.0),
                ('Iluminacion', 1000.0),
                ('Arbitro', 2000.0),
                ('Completo', 2500.0)
            ]
            
            cursor.executemany("""
                INSERT INTO servicios (nombre, costo) VALUES (?, ?)
            """, servicios_iniciales)
                
        conn.commit()
        
    except Exception as e:
        print(f"Error al insertar datos iniciales: {e}")
        conn.rollback()

def inicializar_sistema_base_datos(db_name):
    try:
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        
        crear_tablas(cursor)
        insertar_datos_iniciales(cursor, conn)
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        if conn:
            conn.close()
