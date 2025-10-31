import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
try:
    from tkcalendar import DateEntry
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False
    print("Advertencia: tkcalendar no está instalado. Se usarán campos de texto para las fechas.")

# Configurar el path para importar los módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

from services.cancha_service import CanchaService
from services.cliente_service import ClienteService
from services.reserva_service import ReservaService
from reports.reportes import ReportesService
from models.cancha import Cancha
from models.cliente import Cliente
from models.reserva import Reserva

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Canchas")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Inicializar servicios
        self.cancha_service = CanchaService()
        self.cliente_service = ClienteService()
        self.reserva_service = ReservaService()
        self.reportes_service = ReportesService()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Crear el notebook para las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.create_cancha_tab()
        self.create_cliente_tab()
        self.create_reserva_tab()
        self.create_reportes_tab()
        
    def create_cancha_tab(self):
        # Pestaña de Canchas
        cancha_frame = ttk.Frame(self.notebook)
        self.notebook.add(cancha_frame, text="Canchas")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(cancha_frame, text="Datos de la Cancha", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.cancha_id_entry = ttk.Entry(form_frame, width=10)
        self.cancha_id_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.cancha_nombre_entry = ttk.Entry(form_frame, width=20)
        self.cancha_nombre_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Tipo:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.cancha_tipo_combo = ttk.Combobox(form_frame, values=["Futbol", "Tenis", "Padel"], width=15)
        self.cancha_tipo_combo.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Costo por Hora:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.cancha_costo_entry = ttk.Entry(form_frame, width=15)
        self.cancha_costo_entry.grid(row=1, column=3, sticky='w', padx=5, pady=2)
        
        # Botones
        button_frame = ttk.Frame(cancha_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Crear", command=self.crear_cancha).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.buscar_cancha).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Modificar", command=self.modificar_cancha).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cancha).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_cancha_form).pack(side='left', padx=5)
        
        # Lista de canchas
        list_frame = ttk.LabelFrame(cancha_frame, text="Lista de Canchas", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para mostrar canchas
        columns = ('ID', 'Nombre', 'Tipo', 'Costo por Hora', 'Estado')
        self.cancha_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.cancha_tree.heading(col, text=col)
            self.cancha_tree.column(col, width=120)
        
        scrollbar_cancha = ttk.Scrollbar(list_frame, orient='vertical', command=self.cancha_tree.yview)
        self.cancha_tree.configure(yscrollcommand=scrollbar_cancha.set)
        
        self.cancha_tree.pack(side='left', fill='both', expand=True)
        scrollbar_cancha.pack(side='right', fill='y')
        
        # Botón para actualizar lista
        ttk.Button(list_frame, text="Actualizar Lista", command=self.actualizar_lista_canchas).pack(pady=5)
        
        # Cargar lista inicial
        self.actualizar_lista_canchas()
        
        # Bind para seleccionar cancha
        self.cancha_tree.bind('<<TreeviewSelect>>', self.seleccionar_cancha)
        
    def create_cliente_tab(self):
        # Pestaña de Clientes
        cliente_frame = ttk.Frame(self.notebook)
        self.notebook.add(cliente_frame, text="Clientes")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(cliente_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="DNI:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.cliente_dni_entry = ttk.Entry(form_frame, width=15)
        self.cliente_dni_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.cliente_nombre_entry = ttk.Entry(form_frame, width=20)
        self.cliente_nombre_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.cliente_apellido_entry = ttk.Entry(form_frame, width=20)
        self.cliente_apellido_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.cliente_email_entry = ttk.Entry(form_frame, width=25)
        self.cliente_email_entry.grid(row=1, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Telefono:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.cliente_telefono_entry = ttk.Entry(form_frame, width=15)
        self.cliente_telefono_entry.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        # Botones
        button_frame = ttk.Frame(cliente_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Crear", command=self.crear_cliente).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.buscar_cliente).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Modificar", command=self.modificar_cliente).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cliente).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_cliente_form).pack(side='left', padx=5)
        
        # Lista de clientes
        list_frame = ttk.LabelFrame(cliente_frame, text="Lista de Clientes", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para mostrar clientes
        columns = ('DNI', 'Nombre', 'Apellido', 'Email', 'Telefono')
        self.cliente_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.cliente_tree.heading(col, text=col)
            self.cliente_tree.column(col, width=120)
        
        scrollbar_cliente = ttk.Scrollbar(list_frame, orient='vertical', command=self.cliente_tree.yview)
        self.cliente_tree.configure(yscrollcommand=scrollbar_cliente.set)
        
        self.cliente_tree.pack(side='left', fill='both', expand=True)
        scrollbar_cliente.pack(side='right', fill='y')
        
        # Botón para actualizar lista
        ttk.Button(list_frame, text="Actualizar Lista", command=self.actualizar_lista_clientes).pack(pady=5)
        
        # Cargar lista inicial
        self.actualizar_lista_clientes()
        
        # Bind para seleccionar cliente
        self.cliente_tree.bind('<<TreeviewSelect>>', self.seleccionar_cliente)
        
    def create_reserva_tab(self):
        # Pestaña de Reservas
        reserva_frame = ttk.Frame(self.notebook)
        self.notebook.add(reserva_frame, text="Reservas")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(reserva_frame, text="Datos de la Reserva", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.reserva_id_entry = ttk.Entry(form_frame, width=10)
        self.reserva_id_entry.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="DNI Cliente:").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.reserva_cliente_entry = ttk.Entry(form_frame, width=15)
        self.reserva_cliente_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="ID Cancha:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.reserva_cancha_entry = ttk.Entry(form_frame, width=10)
        self.reserva_cancha_entry.grid(row=1, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Fecha:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        if CALENDAR_AVAILABLE:
            self.reserva_fecha_entry = DateEntry(form_frame, width=12, background='darkblue',
                                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        else:
            self.reserva_fecha_entry = ttk.Entry(form_frame, width=15)
        self.reserva_fecha_entry.grid(row=1, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Hora Inicio:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.reserva_hora_inicio_entry = ttk.Entry(form_frame, width=10)
        self.reserva_hora_inicio_entry.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        ttk.Label(form_frame, text="Hora Fin:").grid(row=2, column=2, sticky='w', padx=5, pady=2)
        self.reserva_hora_fin_entry = ttk.Entry(form_frame, width=10)
        self.reserva_hora_fin_entry.grid(row=2, column=3, sticky='w', padx=5, pady=2)
        
        # Checkboxes
        self.reserva_iluminacion_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Iluminacion", variable=self.reserva_iluminacion_var).grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        self.reserva_arbitro_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Arbitro", variable=self.reserva_arbitro_var).grid(row=3, column=2, columnspan=2, sticky='w', padx=5, pady=2)
        
        # Botones
        button_frame = ttk.Frame(reserva_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Crear", command=self.crear_reserva).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.buscar_reserva).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Finalizar", command=self.finalizar_reserva).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_reserva).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_reserva_form).pack(side='left', padx=5)
        
        # Lista de reservas
        list_frame = ttk.LabelFrame(reserva_frame, text="Lista de Reservas", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para mostrar reservas
        columns = ('ID', 'Cliente DNI', 'Cancha ID', 'Fecha', 'Hora Inicio', 'Hora Fin', 'Estado', 'Iluminacion', 'Arbitro')
        self.reserva_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.reserva_tree.heading(col, text=col)
            self.reserva_tree.column(col, width=100)
        
        scrollbar_reserva = ttk.Scrollbar(list_frame, orient='vertical', command=self.reserva_tree.yview)
        self.reserva_tree.configure(yscrollcommand=scrollbar_reserva.set)
        
        self.reserva_tree.pack(side='left', fill='both', expand=True)
        scrollbar_reserva.pack(side='right', fill='y')
        
        # Botón para actualizar lista
        ttk.Button(list_frame, text="Actualizar Lista", command=self.actualizar_lista_reservas).pack(pady=5)
        
        # Cargar lista inicial
        self.actualizar_lista_reservas()
        
        # Bind para seleccionar reserva
        self.reserva_tree.bind('<<TreeviewSelect>>', self.seleccionar_reserva)
        
    def create_reportes_tab(self):
        # Pestaña de Reportes
        reportes_frame = ttk.Frame(self.notebook)
        self.notebook.add(reportes_frame, text="Reportes")
        
        # Frame para controles de reportes
        controls_frame = ttk.LabelFrame(reportes_frame, text="Generacion de Reportes", padding=20)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        # Reporte 1: Reservas por cliente
        ttk.Label(controls_frame, text="1. Reservas por Cliente", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=5)
        ttk.Button(controls_frame, text="Generar Reporte", command=self.generar_reporte_clientes).grid(row=0, column=2, padx=10, pady=5)
        
        # Reporte 2: Reservas por cancha en periodo
        ttk.Label(controls_frame, text="2. Reservas por Cancha en Periodo", font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        ttk.Label(controls_frame, text="Fecha Inicio:").grid(row=2, column=0, sticky='w', padx=5)
        if CALENDAR_AVAILABLE:
            self.fecha_inicio_entry = DateEntry(controls_frame, width=10, background='darkblue',
                                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        else:
            self.fecha_inicio_entry = ttk.Entry(controls_frame, width=12)
        self.fecha_inicio_entry.grid(row=2, column=1, sticky='w', padx=5)
        
        ttk.Label(controls_frame, text="Fecha Fin:").grid(row=3, column=0, sticky='w', padx=5)
        if CALENDAR_AVAILABLE:
            self.fecha_fin_entry = DateEntry(controls_frame, width=10, background='darkblue',
                                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        else:
            self.fecha_fin_entry = ttk.Entry(controls_frame, width=12)
        self.fecha_fin_entry.grid(row=3, column=1, sticky='w', padx=5)
        
        ttk.Button(controls_frame, text="Generar Reporte", command=self.generar_reporte_periodo).grid(row=2, column=2, rowspan=2, padx=10, pady=5)
        
        # Reporte 3: Canchas mas utilizadas
        ttk.Label(controls_frame, text="3. Canchas Mas Utilizadas", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, sticky='w', pady=5)
        ttk.Button(controls_frame, text="Generar Reporte", command=self.generar_reporte_canchas_utilizadas).grid(row=4, column=2, padx=10, pady=5)
        
        # Reporte 4: Grafico utilizacion mensual
        ttk.Label(controls_frame, text="4. Grafico Utilizacion Mensual", font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, sticky='w', pady=5)
        ttk.Button(controls_frame, text="Generar Grafico", command=self.generar_grafico_mensual).grid(row=5, column=2, padx=10, pady=5)
        
        # Frame para mensajes
        self.mensaje_frame = ttk.LabelFrame(reportes_frame, text="Mensajes", padding=10)
        self.mensaje_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.mensaje_text = tk.Text(self.mensaje_frame, height=10, wrap='word')
        scrollbar_mensaje = ttk.Scrollbar(self.mensaje_frame, orient='vertical', command=self.mensaje_text.yview)
        self.mensaje_text.configure(yscrollcommand=scrollbar_mensaje.set)
        
        self.mensaje_text.pack(side='left', fill='both', expand=True)
        scrollbar_mensaje.pack(side='right', fill='y')
        
    # Métodos para Canchas
    def crear_cancha(self):
        try:
            nombre = self.cancha_nombre_entry.get().strip()
            tipo = self.cancha_tipo_combo.get().strip()
            costo = float(self.cancha_costo_entry.get().strip()) if self.cancha_costo_entry.get().strip() else 0
            
            cancha = Cancha(nombre, tipo, costo)
            self.cancha_service.crear_cancha(cancha)
            
            messagebox.showinfo("Exito", "Cancha creada exitosamente")
            self.limpiar_cancha_form()
            self.actualizar_lista_canchas()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def buscar_cancha(self):
        try:
            id_cancha = int(self.cancha_id_entry.get().strip()) if self.cancha_id_entry.get().strip() else None
            if not id_cancha:
                messagebox.showwarning("Advertencia", "Ingrese un ID de cancha para buscar")
                return
                
            cancha = self.cancha_service.mostrar_cancha_id(id_cancha)
            if cancha:
                self.cancha_nombre_entry.delete(0, tk.END)
                self.cancha_nombre_entry.insert(0, cancha[1])
                self.cancha_tipo_combo.set(cancha[2])
                self.cancha_costo_entry.delete(0, tk.END)
                self.cancha_costo_entry.insert(0, str(cancha[3]))
            else:
                messagebox.showinfo("Informacion", "Cancha no encontrada")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def modificar_cancha(self):
        try:
            id_cancha = int(self.cancha_id_entry.get().strip()) if self.cancha_id_entry.get().strip() else None
            nombre = self.cancha_nombre_entry.get().strip()
            tipo = self.cancha_tipo_combo.get().strip()
            costo = float(self.cancha_costo_entry.get().strip()) if self.cancha_costo_entry.get().strip() else 0
            
            if not id_cancha:
                messagebox.showwarning("Advertencia", "Ingrese un ID de cancha para modificar")
                return
                
            # Validaciones
            self.cancha_service.validar_nombre(nombre)
            self.cancha_service.validar_tipo(tipo)
            self.cancha_service.validar_costo_por_hora(costo)
            
            from dao.cancha_dao import CanchaDAO
            cancha_dao = CanchaDAO()
            cancha_dao.modificar(id_cancha, nombre, tipo, costo)
            
            messagebox.showinfo("Exito", "Cancha modificada exitosamente")
            self.limpiar_cancha_form()
            self.actualizar_lista_canchas()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def eliminar_cancha(self):
        try:
            id_cancha = int(self.cancha_id_entry.get().strip()) if self.cancha_id_entry.get().strip() else None
            if not id_cancha:
                messagebox.showwarning("Advertencia", "Ingrese un ID de cancha para eliminar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Esta seguro de eliminar esta cancha?")
            if respuesta:
                self.cancha_service.eliminar_cancha_id(id_cancha)
                messagebox.showinfo("Exito", "Cancha eliminada exitosamente")
                self.limpiar_cancha_form()
                self.actualizar_lista_canchas()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def limpiar_cancha_form(self):
        self.cancha_id_entry.delete(0, tk.END)
        self.cancha_nombre_entry.delete(0, tk.END)
        self.cancha_tipo_combo.set('')
        self.cancha_costo_entry.delete(0, tk.END)
        
    def actualizar_lista_canchas(self):
        # Limpiar el treeview
        for item in self.cancha_tree.get_children():
            self.cancha_tree.delete(item)
            
        try:
            canchas = self.cancha_service.mostrar_canchas()
            if canchas:
                for cancha in canchas:
                    # cancha = (id, nombre, tipo, costo_por_hora, estado_id)
                    estado = "Activa" if cancha[4] == 1 else "Inactiva"
                    self.cancha_tree.insert('', 'end', values=(cancha[0], cancha[1], cancha[2], cancha[3], estado))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las canchas: {str(e)}")
            
    def seleccionar_cancha(self, event):
        selection = self.cancha_tree.selection()
        if selection:
            item = self.cancha_tree.item(selection[0])
            values = item['values']
            
            self.cancha_id_entry.delete(0, tk.END)
            self.cancha_id_entry.insert(0, str(values[0]))
            self.cancha_nombre_entry.delete(0, tk.END)
            self.cancha_nombre_entry.insert(0, values[1])
            self.cancha_tipo_combo.set(values[2])
            self.cancha_costo_entry.delete(0, tk.END)
            self.cancha_costo_entry.insert(0, str(values[3]))
            
    # Métodos para Clientes
    def crear_cliente(self):
        try:
            dni = self.cliente_dni_entry.get().strip()
            nombre = self.cliente_nombre_entry.get().strip()
            apellido = self.cliente_apellido_entry.get().strip()
            email = self.cliente_email_entry.get().strip()
            telefono = self.cliente_telefono_entry.get().strip()
            
            cliente = Cliente(dni, nombre, apellido, email, telefono)
            self.cliente_service.crear_cliente(cliente)
            
            messagebox.showinfo("Exito", "Cliente creado exitosamente")
            self.limpiar_cliente_form()
            self.actualizar_lista_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def buscar_cliente(self):
        try:
            dni = self.cliente_dni_entry.get().strip()
            if not dni:
                messagebox.showwarning("Advertencia", "Ingrese un DNI para buscar")
                return
                
            cliente = self.cliente_service.mostrar_cliente_id(dni)
            if cliente:
                self.cliente_nombre_entry.delete(0, tk.END)
                self.cliente_nombre_entry.insert(0, cliente[1])
                self.cliente_apellido_entry.delete(0, tk.END)
                self.cliente_apellido_entry.insert(0, cliente[2])
                self.cliente_email_entry.delete(0, tk.END)
                self.cliente_email_entry.insert(0, cliente[3])
                self.cliente_telefono_entry.delete(0, tk.END)
                self.cliente_telefono_entry.insert(0, str(cliente[4]))
            else:
                messagebox.showinfo("Informacion", "Cliente no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def modificar_cliente(self):
        try:
            dni = self.cliente_dni_entry.get().strip()
            email = self.cliente_email_entry.get().strip()
            telefono = self.cliente_telefono_entry.get().strip()
            
            if not dni:
                messagebox.showwarning("Advertencia", "Ingrese un DNI para modificar")
                return
                
            # Validaciones
            self.cliente_service.validar_email(email)
            self.cliente_service.validar_telefono(telefono)
            
            from dao.cliente_dao import ClienteDAO
            cliente_dao = ClienteDAO()
            cliente_dao.modificar(dni, email, telefono)
            
            messagebox.showinfo("Exito", "Cliente modificado exitosamente")
            self.limpiar_cliente_form()
            self.actualizar_lista_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def eliminar_cliente(self):
        try:
            dni = self.cliente_dni_entry.get().strip()
            if not dni:
                messagebox.showwarning("Advertencia", "Ingrese un DNI para eliminar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Esta seguro de eliminar este cliente?")
            if respuesta:
                self.cliente_service.eliminar_cliente_id(dni)
                messagebox.showinfo("Exito", "Cliente eliminado exitosamente")
                self.limpiar_cliente_form()
                self.actualizar_lista_clientes()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def limpiar_cliente_form(self):
        self.cliente_dni_entry.delete(0, tk.END)
        self.cliente_nombre_entry.delete(0, tk.END)
        self.cliente_apellido_entry.delete(0, tk.END)
        self.cliente_email_entry.delete(0, tk.END)
        self.cliente_telefono_entry.delete(0, tk.END)
        
    def actualizar_lista_clientes(self):
        # Limpiar el treeview
        for item in self.cliente_tree.get_children():
            self.cliente_tree.delete(item)
            
        try:
            clientes = self.cliente_service.mostrar_clientes()
            if clientes:
                for cliente in clientes:
                    # cliente = (dni, nombre, apellido, email, telefono)
                    self.cliente_tree.insert('', 'end', values=cliente)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los clientes: {str(e)}")
            
    def seleccionar_cliente(self, event):
        selection = self.cliente_tree.selection()
        if selection:
            item = self.cliente_tree.item(selection[0])
            values = item['values']
            
            self.cliente_dni_entry.delete(0, tk.END)
            self.cliente_dni_entry.insert(0, str(values[0]))
            self.cliente_nombre_entry.delete(0, tk.END)
            self.cliente_nombre_entry.insert(0, values[1])
            self.cliente_apellido_entry.delete(0, tk.END)
            self.cliente_apellido_entry.insert(0, values[2])
            self.cliente_email_entry.delete(0, tk.END)
            self.cliente_email_entry.insert(0, values[3])
            self.cliente_telefono_entry.delete(0, tk.END)
            self.cliente_telefono_entry.insert(0, str(values[4]))
            
    # Métodos para Reservas
    def crear_reserva(self):
        try:
            cliente_id = self.reserva_cliente_entry.get().strip()
            cancha_id = int(self.reserva_cancha_entry.get().strip()) if self.reserva_cancha_entry.get().strip() else 0
            # Obtener fecha del widget (DateEntry o Entry)
            if CALENDAR_AVAILABLE and hasattr(self.reserva_fecha_entry, 'get_date'):
                fecha = self.reserva_fecha_entry.get_date().strftime('%Y-%m-%d')
            else:
                fecha = self.reserva_fecha_entry.get().strip()
            hora_inicio = self.reserva_hora_inicio_entry.get().strip()
            hora_fin = self.reserva_hora_fin_entry.get().strip()
            tiene_iluminacion = self.reserva_iluminacion_var.get()
            tiene_arbitro = self.reserva_arbitro_var.get()
            
            reserva = Reserva(cliente_id, cancha_id, fecha, hora_inicio, hora_fin, tiene_iluminacion, tiene_arbitro)
            self.reserva_service.crear_reserva(reserva)
            
            messagebox.showinfo("Exito", "Reserva creada exitosamente")
            self.limpiar_reserva_form()
            self.actualizar_lista_reservas()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def buscar_reserva(self):
        try:
            id_reserva = int(self.reserva_id_entry.get().strip()) if self.reserva_id_entry.get().strip() else None
            if not id_reserva:
                messagebox.showwarning("Advertencia", "Ingrese un ID de reserva para buscar")
                return
                
            reserva = self.reserva_service.mostrar_reserva_id(id_reserva)
            if reserva:
                self.reserva_cliente_entry.delete(0, tk.END)
                self.reserva_cliente_entry.insert(0, str(reserva[1]))
                self.reserva_cancha_entry.delete(0, tk.END)
                self.reserva_cancha_entry.insert(0, str(reserva[2]))
                if CALENDAR_AVAILABLE and hasattr(self.reserva_fecha_entry, 'set_date'):
                    from datetime import datetime
                    fecha_obj = datetime.strptime(reserva[3], '%Y-%m-%d').date()
                    self.reserva_fecha_entry.set_date(fecha_obj)
                else:
                    self.reserva_fecha_entry.delete(0, tk.END)
                    self.reserva_fecha_entry.insert(0, reserva[3])
                self.reserva_hora_inicio_entry.delete(0, tk.END)
                self.reserva_hora_inicio_entry.insert(0, reserva[4])
                self.reserva_hora_fin_entry.delete(0, tk.END)
                self.reserva_hora_fin_entry.insert(0, reserva[5])
                self.reserva_iluminacion_var.set(bool(reserva[7]))
                self.reserva_arbitro_var.set(bool(reserva[8]))
            else:
                messagebox.showinfo("Informacion", "Reserva no encontrada")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def finalizar_reserva(self):
        try:
            id_reserva = int(self.reserva_id_entry.get().strip()) if self.reserva_id_entry.get().strip() else None
            if not id_reserva:
                messagebox.showwarning("Advertencia", "Ingrese un ID de reserva para finalizar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Esta seguro de finalizar esta reserva?")
            if respuesta:
                self.reserva_service.finalizar_reserva_id(id_reserva)
                messagebox.showinfo("Exito", "Reserva finalizada exitosamente")
                self.limpiar_reserva_form()
                self.actualizar_lista_reservas()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def eliminar_reserva(self):
        try:
            id_reserva = int(self.reserva_id_entry.get().strip()) if self.reserva_id_entry.get().strip() else None
            if not id_reserva:
                messagebox.showwarning("Advertencia", "Ingrese un ID de reserva para eliminar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Esta seguro de eliminar esta reserva?")
            if respuesta:
                self.reserva_service.eliminar_reserva_id(id_reserva)
                messagebox.showinfo("Exito", "Reserva eliminada exitosamente")
                self.limpiar_reserva_form()
                self.actualizar_lista_reservas()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def limpiar_reserva_form(self):
        self.reserva_id_entry.delete(0, tk.END)
        self.reserva_cliente_entry.delete(0, tk.END)
        self.reserva_cancha_entry.delete(0, tk.END)
        if CALENDAR_AVAILABLE and hasattr(self.reserva_fecha_entry, 'set_date'):
            from datetime import date
            self.reserva_fecha_entry.set_date(date.today())
        else:
            self.reserva_fecha_entry.delete(0, tk.END)
        self.reserva_hora_inicio_entry.delete(0, tk.END)
        self.reserva_hora_fin_entry.delete(0, tk.END)
        self.reserva_iluminacion_var.set(False)
        self.reserva_arbitro_var.set(False)
        
    def actualizar_lista_reservas(self):
        # Limpiar el treeview
        for item in self.reserva_tree.get_children():
            self.reserva_tree.delete(item)
            
        try:
            reservas = self.reserva_service.mostrar_reservas()
            if reservas:
                for reserva in reservas:
                    # reserva = (id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, tiene_iluminacion, tiene_arbitro)
                    estado = "Activa" if reserva[6] == 3 else "Finalizada"
                    iluminacion = "Si" if reserva[7] else "No"
                    arbitro = "Si" if reserva[8] else "No"
                    valores = (reserva[0], reserva[1], reserva[2], reserva[3], reserva[4], reserva[5], estado, iluminacion, arbitro)
                    self.reserva_tree.insert('', 'end', values=valores)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las reservas: {str(e)}")
            
    def seleccionar_reserva(self, event):
        selection = self.reserva_tree.selection()
        if selection:
            item = self.reserva_tree.item(selection[0])
            values = item['values']
            
            self.reserva_id_entry.delete(0, tk.END)
            self.reserva_id_entry.insert(0, str(values[0]))
            self.reserva_cliente_entry.delete(0, tk.END)
            self.reserva_cliente_entry.insert(0, str(values[1]))
            self.reserva_cancha_entry.delete(0, tk.END)
            self.reserva_cancha_entry.insert(0, str(values[2]))
            if CALENDAR_AVAILABLE and hasattr(self.reserva_fecha_entry, 'set_date'):
                from datetime import datetime
                try:
                    fecha_obj = datetime.strptime(str(values[3]), '%Y-%m-%d').date()
                    self.reserva_fecha_entry.set_date(fecha_obj)
                except ValueError:
                    # Si hay error en el formato, usar el método tradicional
                    if hasattr(self.reserva_fecha_entry, 'delete'):
                        self.reserva_fecha_entry.delete(0, tk.END)
                        self.reserva_fecha_entry.insert(0, values[3])
            else:
                self.reserva_fecha_entry.delete(0, tk.END)
                self.reserva_fecha_entry.insert(0, values[3])
            self.reserva_hora_inicio_entry.delete(0, tk.END)
            self.reserva_hora_inicio_entry.insert(0, values[4])
            self.reserva_hora_fin_entry.delete(0, tk.END)
            self.reserva_hora_fin_entry.insert(0, values[5])
            self.reserva_iluminacion_var.set(values[7] == "Si")
            self.reserva_arbitro_var.set(values[8] == "Si")
            
    # Métodos para Reportes
    def generar_reporte_clientes(self):
        try:
            self.reportes_service.reservas_por_cliente()
            mensaje = "Reporte de reservas por cliente generado exitosamente.\nArchivo: reporte_reservas_por_cliente_[fecha].pdf"
            self.agregar_mensaje(mensaje)
            messagebox.showinfo("Exito", mensaje)
        except Exception as e:
            error_msg = f"Error al generar reporte: {str(e)}"
            self.agregar_mensaje(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def generar_reporte_periodo(self):
        try:
            # Obtener fechas de los widgets (DateEntry o Entry)
            if CALENDAR_AVAILABLE and hasattr(self.fecha_inicio_entry, 'get_date'):
                fecha_inicio = self.fecha_inicio_entry.get_date().strftime('%Y-%m-%d')
                fecha_fin = self.fecha_fin_entry.get_date().strftime('%Y-%m-%d')
            else:
                fecha_inicio = self.fecha_inicio_entry.get().strip()
                fecha_fin = self.fecha_fin_entry.get().strip()
            
            if not fecha_inicio or not fecha_fin:
                messagebox.showwarning("Advertencia", "Seleccione ambas fechas")
                return
                
            self.reportes_service.reservas_por_cancha_en_periodo(fecha_inicio, fecha_fin)
            mensaje = f"Reporte de reservas por cancha en periodo {fecha_inicio} - {fecha_fin} generado exitosamente.\nArchivo: reporte_reservas_por_cancha_en_periodo_[fecha].pdf"
            self.agregar_mensaje(mensaje)
            messagebox.showinfo("Exito", mensaje)
        except Exception as e:
            error_msg = f"Error al generar reporte: {str(e)}"
            self.agregar_mensaje(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def generar_reporte_canchas_utilizadas(self):
        try:
            self.reportes_service.canchas_mas_utilizadas()
            mensaje = "Reporte de canchas mas utilizadas generado exitosamente.\nArchivo: reporte_canchas_mas_utilizadas_[fecha].pdf"
            self.agregar_mensaje(mensaje)
            messagebox.showinfo("Exito", mensaje)
        except Exception as e:
            error_msg = f"Error al generar reporte: {str(e)}"
            self.agregar_mensaje(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def generar_grafico_mensual(self):
        try:
            self.reportes_service.grafico_utilizacion_mensual_canchas()
            mensaje = "Grafico de utilizacion mensual generado exitosamente.\nArchivo: reporte_grafico_utilizacion_mensual_canchas_[fecha].pdf"
            self.agregar_mensaje(mensaje)
            messagebox.showinfo("Exito", mensaje)
        except Exception as e:
            error_msg = f"Error al generar grafico: {str(e)}"
            self.agregar_mensaje(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def agregar_mensaje(self, mensaje):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje_completo = f"[{timestamp}] {mensaje}\n\n"
        self.mensaje_text.insert(tk.END, mensaje_completo)
        self.mensaje_text.see(tk.END)

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()