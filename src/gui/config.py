"""
Configuración de la interfaz gráfica
"""

# Configuración de la ventana principal
WINDOW_CONFIG = {
    'title': 'Sistema de Reservas de Canchas',
    'geometry': '900x700',
    'resizable': True
}

# Configuración de colores y estilos
COLORS = {
    'primary': '#2196F3',
    'secondary': '#FFC107',
    'success': '#4CAF50',
    'danger': '#F44336',
    'warning': '#FF9800',
    'info': '#00BCD4'
}

# Configuración de las pestañas
TABS = {
    'canchas': 'Canchas',
    'clientes': 'Clientes', 
    'reservas': 'Reservas',
    'reportes': 'Reportes'
}

# Tipos de cancha disponibles
TIPOS_CANCHA = ['Futbol', 'Tenis', 'Padel']

# Configuración de formularios
FORM_CONFIG = {
    'padding': 10,
    'field_width': 20,
    'button_padding': 5
}

# Configuración de listas/treeviews
LIST_CONFIG = {
    'height': 10,
    'column_width': 120
}

# Mensajes de la aplicación
MESSAGES = {
    'success_create': '{} creado exitosamente',
    'success_update': '{} modificado exitosamente',
    'success_delete': '{} eliminado exitosamente',
    'confirm_delete': '¿Esta seguro de eliminar este {}?',
    'not_found': '{} no encontrado',
    'empty_field': 'Complete todos los campos obligatorios',
    'invalid_id': 'Ingrese un ID válido'
}