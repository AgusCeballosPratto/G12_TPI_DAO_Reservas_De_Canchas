import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from models.torneo import Torneo

class TorneoGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.tipos_torneo = ["Futbol", "Tenis", "Padel"]
        self.crear_interfaz()
        self.cargar_torneos()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de torneos"""
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
                               text="Gestión de Torneos",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Botón actualizar
        refresh_btn = ttk.Button(title_frame,
                                text="Actualizar",
                                command=self.cargar_torneos,
                                style='Primary.TButton')
        refresh_btn.pack(side='right')
        
        # Frame para formulario de creación
        self.crear_formulario_torneo()
        
        # Frame para lista de torneos
        self.crear_lista_torneos()
    
    def crear_formulario_torneo(self):
        """Crear el formulario para agregar torneos"""
        form_frame = ttk.LabelFrame(self.scrollable_frame, 
                                   text="Crear Nuevo Torneo",
                                   padding=15)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Variables del formulario
        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar()
        
        # Grid para el formulario
        # Fila 1: Nombre y Tipo
        ttk.Label(form_frame, text="Nombre del Torneo:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        entry_nombre = ttk.Entry(form_frame, textvariable=self.var_nombre, width=30)
        entry_nombre.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        ttk.Label(form_frame, text="Tipo de Torneo:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=5)
        combo_tipo = ttk.Combobox(form_frame, 
                                 textvariable=self.var_tipo, 
                                 values=self.tipos_torneo,
                                 state="readonly",
                                 width=27)
        combo_tipo.grid(row=0, column=3, sticky='ew', padx=(0, 20), pady=5)
        
        # Configurar el grid
        for i in range(4):
            form_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Información adicional
        info_frame = ttk.Frame(form_frame)
        info_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky='ew')
        
        info_text = ("Después de crear el torneo, se mostrarán las reservas disponibles\n"
                    "del mismo tipo para asociar al torneo. Las fechas de inicio y fin\n"
                    "se calcularán automáticamente según las reservas seleccionadas.")
        
        ttk.Label(info_frame, text=info_text, 
                 foreground=self.colores['texto'], 
                 font=('Segoe UI', 9, 'italic')).pack(anchor='w')
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(20, 0))
        
        btn_crear = ttk.Button(button_frame,
                              text="Crear Torneo",
                              command=self.crear_torneo,
                              style='Success.TButton')
        btn_crear.pack(side='left', padx=(0, 10))
        
        btn_limpiar = ttk.Button(button_frame,
                                text="Limpiar",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(side='left')
    
    def crear_lista_torneos(self):
        """Crear la lista/tabla de torneos"""
        list_frame = ttk.LabelFrame(self.scrollable_frame,
                                   text="Lista de Torneos",
                                   padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('id', 'nombre', 'fecha_inicio', 'fecha_fin', 'tipo')
        self.tree_torneos = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_torneos.heading('id', text='ID')
        self.tree_torneos.heading('nombre', text='Nombre')
        self.tree_torneos.heading('fecha_inicio', text='Fecha Inicio')
        self.tree_torneos.heading('fecha_fin', text='Fecha Fin')
        self.tree_torneos.heading('tipo', text='Tipo')
        
        # Ajustar ancho de columnas
        self.tree_torneos.column('id', width=50)
        self.tree_torneos.column('nombre', width=200)
        self.tree_torneos.column('fecha_inicio', width=120)
        self.tree_torneos.column('fecha_fin', width=120)
        self.tree_torneos.column('tipo', width=100)
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_torneos.yview)
        self.tree_torneos.configure(yscrollcommand=tree_scroll.set)
        
        # Layout de la tabla
        self.tree_torneos.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Frame para botones de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        btn_eliminar = ttk.Button(actions_frame,
                                 text="Eliminar Torneo",
                                 command=self.eliminar_torneo,
                                 style='Error.TButton')
        btn_eliminar.pack(side='left')
        
        btn_ver_reservas = ttk.Button(actions_frame,
                                     text="Ver Reservas",
                                     command=self.mostrar_reservas_torneo,
                                     style='Primary.TButton')
        btn_ver_reservas.pack(side='left', padx=(10, 0))
        
        # Bind para selección
        self.tree_torneos.bind('<<TreeviewSelect>>', self.on_torneo_select)
    
    def crear_torneo(self):
        """Crear un nuevo torneo con selección de reservas"""
        try:
            # Validar campos obligatorios
            if not all([self.var_nombre.get(), self.var_tipo.get()]):
                messagebox.showerror("Error", "Nombre y tipo son obligatorios")
                return
            
            # Obtener reservas del tipo seleccionado
            reservas_disponibles = self.obtener_reservas_por_tipo(self.var_tipo.get())
            
            if not reservas_disponibles:
                messagebox.showwarning("Advertencia", 
                                     f"No hay reservas disponibles para torneos de tipo {self.var_tipo.get()}")
                return
            
            # Mostrar ventana de selección de reservas
            self.mostrar_seleccion_reservas(reservas_disponibles)
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear torneo: {str(e)}")
    
    def obtener_reservas_por_tipo(self, tipo_torneo):
        """Obtener reservas que coincidan con el tipo de torneo"""
        try:
            # Usar el método del controlador para obtener reservas por tipo de cancha
            reservas = self.controlador.listar_reservas()
            canchas = self.controlador.listar_canchas()
            
            # Crear un mapeo de cancha_id -> tipo
            cancha_tipos = {cancha[0]: cancha[2] for cancha in canchas}
            
            # Filtrar reservas por tipo de cancha y que no tengan torneo asignado
            reservas_filtradas = []
            for reserva in reservas:
                cancha_id = reserva[2]
                torneo_id = reserva[8] if len(reserva) > 8 else None
                estado_id = reserva[6] if len(reserva) > 6 else reserva[3]
                
                # Solo reservas activas (estado 3), sin torneo y del tipo correcto
                if (cancha_id in cancha_tipos and 
                    cancha_tipos[cancha_id] == tipo_torneo and 
                    torneo_id is None and
                    estado_id == 3):
                    reservas_filtradas.append(reserva)
            
            return reservas_filtradas
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener reservas: {str(e)}")
            return []
    
    def mostrar_seleccion_reservas(self, reservas_disponibles):
        """Mostrar ventana para seleccionar reservas del torneo"""
        self.ventana_reservas = tk.Toplevel(self.parent)
        self.ventana_reservas.title("Seleccionar Reservas para el Torneo")
        self.ventana_reservas.geometry("800x500")
        self.ventana_reservas.resizable(True, True)
        
        # Centrar ventana
        self.ventana_reservas.transient(self.parent.winfo_toplevel())
        self.ventana_reservas.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana_reservas, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(main_frame, 
                 text=f"Reservas disponibles para torneo de {self.var_tipo.get()}",
                 font=('Segoe UI', 12, 'bold')).pack(pady=(0, 20))
        
        # Frame para la lista de reservas con checkboxes
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Crear Treeview con checkboxes (simulados)
        columns = ('select', 'id', 'cliente_id', 'cancha_id', 'fecha', 'hora_inicio', 'hora_fin')
        self.tree_reservas_torneo = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_reservas_torneo.heading('select', text='Seleccionar')
        self.tree_reservas_torneo.heading('id', text='ID')
        self.tree_reservas_torneo.heading('cliente_id', text='Cliente')
        self.tree_reservas_torneo.heading('cancha_id', text='Cancha')
        self.tree_reservas_torneo.heading('fecha', text='Fecha')
        self.tree_reservas_torneo.heading('hora_inicio', text='Hora Inicio')
        self.tree_reservas_torneo.heading('hora_fin', text='Hora Fin')
        
        # Ajustar ancho de columnas
        self.tree_reservas_torneo.column('select', width=80)
        self.tree_reservas_torneo.column('id', width=50)
        self.tree_reservas_torneo.column('cliente_id', width=80)
        self.tree_reservas_torneo.column('cancha_id', width=80)
        self.tree_reservas_torneo.column('fecha', width=100)
        self.tree_reservas_torneo.column('hora_inicio', width=90)
        self.tree_reservas_torneo.column('hora_fin', width=90)
        
        # Scrollbar
        tree_scroll_reservas = ttk.Scrollbar(list_frame, orient='vertical', 
                                           command=self.tree_reservas_torneo.yview)
        self.tree_reservas_torneo.configure(yscrollcommand=tree_scroll_reservas.set)
        
        # Layout
        self.tree_reservas_torneo.pack(side='left', fill='both', expand=True)
        tree_scroll_reservas.pack(side='right', fill='y')
        
        # Llenar la tabla con reservas
        self.reservas_seleccionadas = {}
        for reserva in reservas_disponibles:
            # reserva = (id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, servicio_id, torneo_id)
            item_id = self.tree_reservas_torneo.insert('', 'end', values=(
                '☐',  # Checkbox no seleccionado
                reserva[0],  # id
                reserva[1],  # cliente_id
                reserva[2],  # cancha_id
                reserva[3],  # fecha
                reserva[4],  # hora_inicio
                reserva[5]   # hora_fin
            ))
            self.reservas_seleccionadas[item_id] = {'reserva': reserva, 'selected': False}
        
        # Bind para selección/deselección
        self.tree_reservas_torneo.bind('<Double-1>', self.toggle_selection)
        
        # Instrucción para el usuario
        instruction_frame = ttk.Frame(main_frame)
        instruction_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(instruction_frame, 
                 text="Haga doble clic en una fila para seleccionar/deseleccionar la reserva",
                 font=('Segoe UI', 9, 'italic'),
                 foreground=self.colores.get('texto', '#2C3E50')).pack(side='left')
        
        # Botones de selección masiva
        selection_buttons_frame = ttk.Frame(instruction_frame)
        selection_buttons_frame.pack(side='right')
        
        ttk.Button(selection_buttons_frame,
                  text="Seleccionar Todas",
                  command=self.seleccionar_todas_reservas,
                  style='Primary.TButton').pack(side='left', padx=(0, 5))
        
        ttk.Button(selection_buttons_frame,
                  text="Deseleccionar Todas",
                  command=self.deseleccionar_todas_reservas).pack(side='left')
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame,
                  text="Crear Torneo con Reservas Seleccionadas",
                  command=self.confirmar_creacion_torneo,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cancelar",
                  command=self.ventana_reservas.destroy).pack(side='left')
    
    def toggle_selection(self, event):
        """Alternar selección de reserva"""
        try:
            # Obtener el item seleccionado
            selection = self.tree_reservas_torneo.selection()
            if not selection:
                return
            
            item = selection[0]
            
            # Verificar que el item existe en nuestro diccionario
            if item in self.reservas_seleccionadas:
                # Alternar selección
                self.reservas_seleccionadas[item]['selected'] = not self.reservas_seleccionadas[item]['selected']
                
                # Actualizar visual
                if self.reservas_seleccionadas[item]['selected']:
                    checkbox = '☑'
                else:
                    checkbox = '☐'
                
                values = list(self.tree_reservas_torneo.item(item, 'values'))
                values[0] = checkbox
                self.tree_reservas_torneo.item(item, values=values)
                    
        except Exception as e:
            print(f"Error en toggle_selection: {e}")  # Para debug
            messagebox.showerror("Error", f"Error al seleccionar reserva: {str(e)}")
    
    def seleccionar_todas_reservas(self):
        """Seleccionar todas las reservas disponibles"""
        try:
            for item_id in self.reservas_seleccionadas:
                self.reservas_seleccionadas[item_id]['selected'] = True
                # Actualizar visual
                values = list(self.tree_reservas_torneo.item(item_id, 'values'))
                values[0] = '☑'
                self.tree_reservas_torneo.item(item_id, values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar todas las reservas: {str(e)}")
    
    def deseleccionar_todas_reservas(self):
        """Deseleccionar todas las reservas"""
        try:
            for item_id in self.reservas_seleccionadas:
                self.reservas_seleccionadas[item_id]['selected'] = False
                # Actualizar visual
                values = list(self.tree_reservas_torneo.item(item_id, 'values'))
                values[0] = '☐'
                self.tree_reservas_torneo.item(item_id, values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Error al deseleccionar todas las reservas: {str(e)}")
    
    def confirmar_creacion_torneo(self):
        """Confirmar la creación del torneo con las reservas seleccionadas"""
        try:
            # Obtener reservas seleccionadas
            reservas_para_torneo = []
            for item_id, data in self.reservas_seleccionadas.items():
                if data['selected']:
                    reservas_para_torneo.append(data['reserva'][0])  # ID de la reserva
            
            if not reservas_para_torneo:
                messagebox.showwarning("Advertencia", "Debe seleccionar al menos una reserva")
                return
            
            # Crear el torneo usando el método adaptado
            self.crear_torneo_gui(self.var_nombre.get(), self.var_tipo.get(), reservas_para_torneo)
            
            messagebox.showinfo("Éxito", "Torneo creado exitosamente")
            self.ventana_reservas.destroy()
            self.limpiar_formulario()
            self.cargar_torneos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear torneo: {str(e)}")
    
    def crear_torneo_gui(self, nombre, tipo, reservas_ids):
        """Método adaptado para crear torneo desde la GUI"""
        try:
            # Verificar que el nombre no existe
            torneos_existentes = self.controlador.mostrar_torneos()
            
            for torneo in torneos_existentes:
                if torneo[1] == nombre:  # torneo[1] es el nombre
                    raise ValueError("El torneo con ese nombre ya existe.")
            
            # Usar el modelo Torneo para crear el objeto
            torneo = Torneo(nombre, tipo)
            
            # Crear el torneo usando el controlador, pasando las reservas
            # El servicio calculará automáticamente las fechas de inicio y fin
            id_torneo = self.controlador.crear_torneo(torneo, reservas_ids)
            
            if not id_torneo:
                raise Exception("No se pudo crear el torneo")
                
        except Exception as e:
            raise e  # Re-lanzar la excepción para que la maneje el método que llama
    
    def cargar_torneos(self):
        """Cargar la lista de torneos en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree_torneos.get_children():
                self.tree_torneos.delete(item)
            
            # Obtener torneos
            torneos = self.controlador.mostrar_torneos()
            
            # Llenar tabla
            for torneo in torneos:
                # torneo = (id, nombre, fecha_inicio, fecha_fin, tipo)
                valores = (
                    torneo[0],  # id
                    torneo[1],  # nombre
                    torneo[2],  # fecha_inicio
                    torneo[3],  # fecha_fin
                    torneo[4]   # tipo
                )
                
                self.tree_torneos.insert('', 'end', values=valores)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar torneos: {str(e)}")
    
    def on_torneo_select(self, event):
        """Manejar selección de torneo en la tabla"""
        selection = self.tree_torneos.selection()
        if selection:
            item = self.tree_torneos.item(selection[0])
            values = item['values']
            self.torneo_seleccionado = values
    
    def eliminar_torneo(self):
        """Eliminar el torneo seleccionado"""
        if not hasattr(self, 'torneo_seleccionado'):
            messagebox.showwarning("Advertencia", "Seleccione un torneo para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el torneo '{self.torneo_seleccionado[1]}'?\n"
            f"ID: {self.torneo_seleccionado[0]}\n"
            f"Esto también eliminará las reservas asociadas al torneo."
        )
        
        if respuesta:
            try:
                id_torneo = self.torneo_seleccionado[0]
                self.controlador.eliminar_torneo_id(id_torneo)
                
                messagebox.showinfo("Éxito", "Torneo eliminado exitosamente")
                self.cargar_torneos()
                delattr(self, 'torneo_seleccionado')
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar torneo: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar el formulario de creación"""
        self.var_nombre.set("")
        self.var_tipo.set("")
    
    def mostrar_reservas_torneo(self):
        """Mostrar las reservas asociadas al torneo seleccionado en un pop-up"""
        if not hasattr(self, 'torneo_seleccionado'):
            messagebox.showwarning("Advertencia", "Seleccione un torneo para ver sus reservas")
            return
        
        try:
            torneo_id = self.torneo_seleccionado[0]
            torneo_nombre = self.torneo_seleccionado[1]
            
            # Obtener las reservas del torneo
            reservas = self.controlador.listar_reservas_por_torneo(torneo_id)
            
            if not reservas:
                messagebox.showinfo("Información", 
                                   f"El torneo '{torneo_nombre}' no tiene reservas asociadas")
                return
            
            # Crear la ventana pop-up
            self.ventana_reservas_torneo = tk.Toplevel(self.parent)
            self.ventana_reservas_torneo.title(f"Reservas del Torneo: {torneo_nombre}")
            self.ventana_reservas_torneo.geometry("900x600")
            self.ventana_reservas_torneo.resizable(True, True)
            
            # Centrar ventana
            self.ventana_reservas_torneo.transient(self.parent.winfo_toplevel())
            self.ventana_reservas_torneo.grab_set()
            
            # Frame principal
            main_frame = ttk.Frame(self.ventana_reservas_torneo, padding=20)
            main_frame.pack(fill='both', expand=True)
            
            # Título
            title_label = ttk.Label(main_frame, 
                                   text=f"Reservas del Torneo: {torneo_nombre}",
                                   font=('Segoe UI', 14, 'bold'))
            title_label.pack(pady=(0, 10))
            
            # Información del torneo
            info_frame = ttk.Frame(main_frame)
            info_frame.pack(fill='x', pady=(0, 20))
            
            info_text = f"Torneo ID: {torneo_id} | Tipo: {self.torneo_seleccionado[4]} | " \
                       f"Fecha Inicio: {self.torneo_seleccionado[2]} | Fecha Fin: {self.torneo_seleccionado[3]}"
            
            ttk.Label(info_frame, 
                     text=info_text,
                     font=('Segoe UI', 10, 'italic'),
                     foreground=self.colores.get('texto', '#2C3E50')).pack()
            
            # Frame para la tabla de reservas
            table_frame = ttk.Frame(main_frame)
            table_frame.pack(fill='both', expand=True, pady=(0, 20))
            
            # Crear Treeview para mostrar las reservas
            columns = ('id', 'cliente_id', 'cancha_id', 'fecha', 'hora_inicio', 'hora_fin', 'estado_id')
            self.tree_reservas_popup = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
            
            # Configurar columnas
            self.tree_reservas_popup.heading('id', text='ID Reserva')
            self.tree_reservas_popup.heading('cliente_id', text='Cliente ID')
            self.tree_reservas_popup.heading('cancha_id', text='Cancha ID')
            self.tree_reservas_popup.heading('fecha', text='Fecha')
            self.tree_reservas_popup.heading('hora_inicio', text='Hora Inicio')
            self.tree_reservas_popup.heading('hora_fin', text='Hora Fin')
            self.tree_reservas_popup.heading('estado_id', text='Estado')
            
            # Ajustar ancho de columnas
            self.tree_reservas_popup.column('id', width=80)
            self.tree_reservas_popup.column('cliente_id', width=90)
            self.tree_reservas_popup.column('cancha_id', width=90)
            self.tree_reservas_popup.column('fecha', width=100)
            self.tree_reservas_popup.column('hora_inicio', width=90)
            self.tree_reservas_popup.column('hora_fin', width=90)
            self.tree_reservas_popup.column('estado_id', width=70)
            
            # Scrollbar para la tabla
            tree_scroll_popup = ttk.Scrollbar(table_frame, orient='vertical', 
                                             command=self.tree_reservas_popup.yview)
            self.tree_reservas_popup.configure(yscrollcommand=tree_scroll_popup.set)
            
            # Layout de la tabla
            self.tree_reservas_popup.pack(side='left', fill='both', expand=True)
            tree_scroll_popup.pack(side='right', fill='y')
            
            # Llenar la tabla con las reservas
            for reserva in reservas:
                # reserva = (id, cliente_id, cancha_id, fecha, hora_inicio, hora_fin, estado_id, servicio_id, torneo_id)
                estado_texto = self.obtener_texto_estado(reserva[6])
                
                self.tree_reservas_popup.insert('', 'end', values=(
                    reserva[0],   # id
                    reserva[1],   # cliente_id
                    reserva[2],   # cancha_id
                    reserva[3],   # fecha
                    reserva[4],   # hora_inicio
                    reserva[5],   # hora_fin
                    estado_texto  # estado_id convertido a texto
                ))
            
            # Estadísticas del torneo
            stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas del Torneo", padding=10)
            stats_frame.pack(fill='x', pady=(10, 10))
            
            stats_text = f"Total de reservas: {len(reservas)} | " \
                        f"Fechas cubiertas: {self.torneo_seleccionado[2]} - {self.torneo_seleccionado[3]}"
            
            ttk.Label(stats_frame, text=stats_text, font=('Segoe UI', 10)).pack()
            
            # Botón cerrar
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill='x')
            
            ttk.Button(button_frame,
                      text="Cerrar",
                      command=self.ventana_reservas_torneo.destroy,
                      style='Primary.TButton').pack(pady=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar reservas del torneo: {str(e)}")
    
    def obtener_texto_estado(self, estado_id):
        """Convertir el ID del estado a texto descriptivo"""
        estados = {
            1: "Pendiente",
            2: "Pagada",
            3: "Activa",
            4: "Finalizada",
            5: "Cancelada"
        }
        return estados.get(estado_id, f"Estado {estado_id}")