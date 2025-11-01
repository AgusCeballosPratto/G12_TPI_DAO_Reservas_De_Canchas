import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from models.reserva import Reserva

class ReservaGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.servicios = {
            1: "Sin Servicio",
            2: "Iluminación",
            3: "Arbitro",
            4: "Completo"
        }
        self.crear_interfaz()
        self.cargar_datos_formulario()
        self.cargar_reservas()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de reservas"""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.parent, bg=self.colores['fondo'])
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="Gestión de Reservas",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Botón actualizar
        refresh_btn = ttk.Button(title_frame,
                                text="Actualizar",
                                command=self.actualizar_todo,
                                style='Primary.TButton')
        refresh_btn.pack(side='right')
        
        # Frame para formulario de creación
        self.crear_formulario_reserva()
        
        # Frame para lista de reservas
        self.crear_lista_reservas()
    
    def crear_formulario_reserva(self):
        """Crear el formulario para agregar reservas"""
        form_frame = ttk.LabelFrame(self.scrollable_frame, 
                                   text="Crear Nueva Reserva",
                                   padding=15)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Variables del formulario
        self.var_cliente = tk.StringVar()
        self.var_cancha = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora_inicio = tk.StringVar()
        self.var_hora_fin = tk.StringVar()
        self.var_servicio = tk.StringVar()
        
        # Datos para los comboboxes
        self.clientes_data = {}
        self.canchas_data = {}
        
        # Grid para el formulario
        # Fila 1: Cliente y Cancha
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.combo_cliente = ttk.Combobox(form_frame, 
                                         textvariable=self.var_cliente,
                                         state="readonly",
                                         width=22)
        self.combo_cliente.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        ttk.Label(form_frame, text="Cancha:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=5)
        self.combo_cancha = ttk.Combobox(form_frame, 
                                        textvariable=self.var_cancha,
                                        state="readonly",
                                        width=22)
        self.combo_cancha.grid(row=0, column=3, sticky='ew', padx=(0, 20), pady=5)
        
        # Fila 2: Fecha y Servicio
        ttk.Label(form_frame, text="Fecha:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.date_entry = DateEntry(form_frame, 
                                   textvariable=self.var_fecha,
                                   date_pattern='yyyy-mm-dd',
                                   mindate=date.today(),
                                   width=20)
        self.date_entry.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        ttk.Label(form_frame, text="Servicio:").grid(row=1, column=2, sticky='w', padx=(0, 10), pady=5)
        self.combo_servicio = ttk.Combobox(form_frame,
                                          textvariable=self.var_servicio,
                                          values=list(self.servicios.values()),
                                          state="readonly",
                                          width=22)
        self.combo_servicio.grid(row=1, column=3, sticky='ew', padx=(0, 20), pady=5)
        self.combo_servicio.set("Sin Servicio")  # Valor por defecto
        
        # Fila 3: Horas
        ttk.Label(form_frame, text="Hora Inicio:").grid(row=2, column=0, sticky='w', padx=(0, 10), pady=5)
        self.combo_hora_inicio = ttk.Combobox(form_frame,
                                             textvariable=self.var_hora_inicio,
                                             values=self.generar_horas(),
                                             state="readonly",
                                             width=22)
        self.combo_hora_inicio.grid(row=2, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        ttk.Label(form_frame, text="Hora Fin:").grid(row=2, column=2, sticky='w', padx=(0, 10), pady=5)
        self.combo_hora_fin = ttk.Combobox(form_frame,
                                          textvariable=self.var_hora_fin,
                                          values=self.generar_horas(),
                                          state="readonly",
                                          width=22)
        self.combo_hora_fin.grid(row=2, column=3, sticky='ew', padx=(0, 20), pady=5)
        
        # Configurar el grid
        for i in range(4):
            form_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(20, 0))
        
        btn_crear = ttk.Button(button_frame,
                              text="Crear Reserva",
                              command=self.crear_reserva,
                              style='Success.TButton')
        btn_crear.pack(side='left', padx=(0, 10))
        
        btn_limpiar = ttk.Button(button_frame,
                                text="Limpiar",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(side='left')
    
    def generar_horas(self):
        """Generar lista de horas para los comboboxes"""
        horas = []
        for hora in range(8, 23):  # De 8:00 a 22:30
            for minuto in ['00', '30']:
                horas.append(f"{hora:02d}:{minuto}")
        return horas
    
    def crear_lista_reservas(self):
        """Crear la lista/tabla de reservas"""
        list_frame = ttk.LabelFrame(self.scrollable_frame,
                                   text="Lista de Reservas",
                                   padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('id', 'cliente', 'cancha', 'fecha', 'hora_inicio', 'hora_fin', 'estado', 'servicio')
        self.tree_reservas = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_reservas.heading('id', text='ID')
        self.tree_reservas.heading('cliente', text='Cliente (DNI)')
        self.tree_reservas.heading('cancha', text='Cancha (ID)')
        self.tree_reservas.heading('fecha', text='Fecha')
        self.tree_reservas.heading('hora_inicio', text='Hora Inicio')
        self.tree_reservas.heading('hora_fin', text='Hora Fin')
        self.tree_reservas.heading('estado', text='Estado')
        self.tree_reservas.heading('servicio', text='Servicio')
        
        # Ajustar ancho de columnas
        self.tree_reservas.column('id', width=50)
        self.tree_reservas.column('cliente', width=100)
        self.tree_reservas.column('cancha', width=80)
        self.tree_reservas.column('fecha', width=100)
        self.tree_reservas.column('hora_inicio', width=90)
        self.tree_reservas.column('hora_fin', width=90)
        self.tree_reservas.column('estado', width=100)
        self.tree_reservas.column('servicio', width=120)
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=tree_scroll.set)
        
        # Layout de la tabla
        self.tree_reservas.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Frame para botones de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        btn_finalizar = ttk.Button(actions_frame,
                                  text="Finalizar",
                                  command=self.finalizar_reserva,
                                  style='Success.TButton')
        btn_finalizar.pack(side='left', padx=(0, 10))
        
        btn_eliminar = ttk.Button(actions_frame,
                                 text="Eliminar",
                                 command=self.eliminar_reserva,
                                 style='Error.TButton')
        btn_eliminar.pack(side='left')
        
        # Bind para selección
        self.tree_reservas.bind('<<TreeviewSelect>>', self.on_reserva_select)
    
    def cargar_datos_formulario(self):
        """Cargar datos para los comboboxes del formulario"""
        try:
            # Cargar clientes
            clientes = self.controlador.listar_clientes()
            cliente_valores = []
            self.clientes_data = {}
            
            for cliente in clientes:
                # cliente = (dni, nombre, apellido, email, telefono)
                texto = f"{cliente[0]} - {cliente[1]} {cliente[2]}"
                cliente_valores.append(texto)
                self.clientes_data[texto] = cliente[0]  # Guardar DNI
            
            self.combo_cliente['values'] = cliente_valores
            
            # Cargar canchas
            canchas = self.controlador.listar_canchas()
            cancha_valores = []
            self.canchas_data = {}
            
            for cancha in canchas:
                # cancha = (id, nombre, tipo, costo_por_hora, estado_id, tiene_iluminacion)
                texto = f"{cancha[0]} - {cancha[1]} ({cancha[2]})"
                cancha_valores.append(texto)
                self.canchas_data[texto] = cancha[0]  # Guardar ID
            
            self.combo_cancha['values'] = cancha_valores
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def crear_reserva(self):
        """Crear una nueva reserva"""
        try:
            # Validar campos obligatorios
            if not all([self.var_cliente.get(), self.var_cancha.get(), 
                       self.var_fecha.get(), self.var_hora_inicio.get(), 
                       self.var_hora_fin.get(), self.var_servicio.get()]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Obtener IDs reales
            cliente_id = self.clientes_data[self.var_cliente.get()]
            cancha_id = self.canchas_data[self.var_cancha.get()]
            
            # Obtener ID del servicio
            servicio_nombre = self.var_servicio.get()
            servicio_id = None
            for sid, snombre in self.servicios.items():
                if snombre == servicio_nombre:
                    servicio_id = sid
                    break
            
            if servicio_id is None:
                messagebox.showerror("Error", "Servicio no válido")
                return
            
            # Crear objeto reserva
            reserva = Reserva(
                cliente_id=cliente_id,
                cancha_id=cancha_id,
                fecha=self.var_fecha.get(),
                hora_inicio=self.var_hora_inicio.get(),
                hora_fin=self.var_hora_fin.get(),
                servicio_id=servicio_id
            )
            
            # Usar el servicio para crear la reserva
            self.controlador.crear_reserva(reserva)
            
            messagebox.showinfo("Éxito", "Reserva creada exitosamente")
            self.limpiar_formulario()
            self.cargar_reservas()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva: {str(e)}")
    
    def cargar_reservas(self):
        """Cargar la lista de reservas en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree_reservas.get_children():
                self.tree_reservas.delete(item)
            
            # Obtener reservas
            reservas = self.controlador.listar_reservas()
            
            # Estados
            estados = {3: "Activa", 4: "Finalizada"}
            
            # Llenar tabla
            for reserva in reservas:
                # reserva = (id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, servicio_id, torneo_id)
                estado_texto = estados.get(reserva[6], "Desconocido")
                servicio_texto = self.servicios.get(reserva[7], "Desconocido")
                
                valores = (
                    reserva[0],  # id
                    reserva[1],  # cliente_id
                    reserva[2],  # cancha_id
                    reserva[3],  # fecha
                    reserva[4],  # hora_inicio
                    reserva[5],  # hora_fin
                    estado_texto,  # estado
                    servicio_texto  # servicio
                )
                
                self.tree_reservas.insert('', 'end', values=valores)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar reservas: {str(e)}")
    
    def on_reserva_select(self, event):
        """Manejar selección de reserva en la tabla"""
        selection = self.tree_reservas.selection()
        if selection:
            item = self.tree_reservas.item(selection[0])
            values = item['values']
            self.reserva_seleccionada = values
    
    def finalizar_reserva(self):
        """Finalizar la reserva seleccionada"""
        if not hasattr(self, 'reserva_seleccionada'):
            messagebox.showwarning("Advertencia", "Seleccione una reserva para finalizar")
            return
        
        if self.reserva_seleccionada[6] == "Finalizada":
            messagebox.showwarning("Advertencia", "La reserva ya está finalizada")
            return
        
        # Confirmar finalización
        respuesta = messagebox.askyesno(
            "Confirmar Finalización",
            f"¿Está seguro de finalizar la reserva ID {self.reserva_seleccionada[0]}?"
        )
        
        if respuesta:
            try:
                id_reserva = self.reserva_seleccionada[0]
                self.controlador.finalizar_reserva(id_reserva)
                
                messagebox.showinfo("Éxito", "Reserva finalizada exitosamente")
                self.cargar_reservas()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al finalizar reserva: {str(e)}")
    
    def eliminar_reserva(self):
        """Eliminar la reserva seleccionada"""
        if not hasattr(self, 'reserva_seleccionada'):
            messagebox.showwarning("Advertencia", "Seleccione una reserva para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la reserva ID {self.reserva_seleccionada[0]}?\n"
            f"Cliente: {self.reserva_seleccionada[1]}, Cancha: {self.reserva_seleccionada[2]}\n"
            f"Fecha: {self.reserva_seleccionada[3]} de {self.reserva_seleccionada[4]} a {self.reserva_seleccionada[5]}"
        )
        
        if respuesta:
            try:
                id_reserva = self.reserva_seleccionada[0]
                self.controlador.eliminar_reserva(id_reserva)
                
                messagebox.showinfo("Éxito", "Reserva eliminada exitosamente")
                self.cargar_reservas()
                delattr(self, 'reserva_seleccionada')
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar reserva: {str(e)}")
    
    def actualizar_todo(self):
        """Actualizar todos los datos"""
        self.cargar_datos_formulario()
        self.cargar_reservas()
    
    def limpiar_formulario(self):
        """Limpiar el formulario de creación"""
        self.var_cliente.set("")
        self.var_cancha.set("")
        self.var_fecha.set("")
        self.var_hora_inicio.set("")
        self.var_hora_fin.set("")
        self.var_servicio.set("Sin Servicio")