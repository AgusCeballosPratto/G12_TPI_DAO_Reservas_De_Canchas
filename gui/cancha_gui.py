import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from models.cancha import Cancha

class CanchaGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.crear_interfaz()
        self.cargar_canchas()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de canchas"""
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
                               text="Gestión de Canchas",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Botón actualizar
        refresh_btn = ttk.Button(title_frame,
                                text="Actualizar",
                                command=self.cargar_canchas,
                                style='Primary.TButton')
        refresh_btn.pack(side='right')
        
        # Frame para formulario de creación
        self.crear_formulario_cancha()
        
        # Frame para lista de canchas
        self.crear_lista_canchas()
    
    def crear_formulario_cancha(self):
        """Crear el formulario para agregar/editar canchas"""
        form_frame = ttk.LabelFrame(self.scrollable_frame, 
                                   text="Agregar Nueva Cancha",
                                   padding=15)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Variables del formulario
        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar()
        self.var_costo = tk.DoubleVar()
        self.var_iluminacion = tk.BooleanVar()
        
        # Grid para el formulario
        # Fila 1: Nombre y Tipo
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        entry_nombre = ttk.Entry(form_frame, textvariable=self.var_nombre, width=25)
        entry_nombre.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=5)
        combo_tipo = ttk.Combobox(form_frame, 
                                 textvariable=self.var_tipo, 
                                 values=["Futbol", "Tenis", "Padel"],
                                 state="readonly",
                                 width=22)
        combo_tipo.grid(row=0, column=3, sticky='ew', padx=(0, 20), pady=5)
        
        # Fila 2: Costo y Iluminación
        ttk.Label(form_frame, text="Costo por Hora:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        entry_costo = ttk.Entry(form_frame, textvariable=self.var_costo, width=25)
        entry_costo.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        check_iluminacion = ttk.Checkbutton(form_frame, 
                                           text="Tiene Iluminación (Reflectores)",
                                           variable=self.var_iluminacion)
        check_iluminacion.grid(row=1, column=2, columnspan=2, sticky='w', padx=(0, 20), pady=5)
        
        # Configurar el grid
        for i in range(4):
            form_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(20, 0))
        
        btn_crear = ttk.Button(button_frame,
                              text="Crear Cancha",
                              command=self.crear_cancha,
                              style='Success.TButton')
        btn_crear.pack(side='left', padx=(0, 10))
        
        btn_limpiar = ttk.Button(button_frame,
                                text="Limpiar",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(side='left')
    
    def crear_lista_canchas(self):
        """Crear la lista/tabla de canchas"""
        list_frame = ttk.LabelFrame(self.scrollable_frame,
                                   text="Lista de Canchas",
                                   padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('nombre', 'tipo', 'costo', 'iluminacion')
        self.tree_canchas = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        # self.tree_canchas.heading('id', text='ID')
        self.tree_canchas.heading('nombre', text='Nombre')
        self.tree_canchas.heading('tipo', text='Tipo')
        self.tree_canchas.heading('costo', text='Costo/Hora')
        self.tree_canchas.heading('iluminacion', text='Iluminación')
        
        # Ajustar ancho de columnas
        # self.tree_canchas.column('id', width=50)
        self.tree_canchas.column('nombre', width=150)
        self.tree_canchas.column('tipo', width=100)
        self.tree_canchas.column('costo', width=100)
        self.tree_canchas.column('iluminacion', width=100)
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_canchas.yview)
        self.tree_canchas.configure(yscrollcommand=tree_scroll.set)
        
        # Layout de la tabla
        self.tree_canchas.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Frame para botones de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        btn_modificar = ttk.Button(actions_frame,
                                  text="Modificar",
                                  command=self.modificar_cancha,
                                  style='Primary.TButton')
        btn_modificar.pack(side='left', padx=(0, 10))
        
        btn_eliminar = ttk.Button(actions_frame,
                                 text="Eliminar",
                                 command=self.eliminar_cancha,
                                 style='Error.TButton')
        btn_eliminar.pack(side='left')
        
        # Bind para selección
        self.tree_canchas.bind('<<TreeviewSelect>>', self.on_cancha_select)
    
    def crear_cancha(self):
        """Crear una nueva cancha"""
        try:
            # Validar campos obligatorios
            if not all([self.var_nombre.get(), self.var_tipo.get()]):
                messagebox.showerror("Error", "Nombre y tipo son obligatorios")
                return
            
            if self.var_costo.get() <= 0:
                messagebox.showerror("Error", "El costo debe ser mayor a 0")
                return
            
            # Crear objeto cancha
            cancha = Cancha(
                nombre=self.var_nombre.get().strip(),
                tipo=self.var_tipo.get(),
                costo_por_hora=self.var_costo.get(),
                tiene_iluminacion=self.var_iluminacion.get()
            )
            
            # Usar el servicio para crear la cancha
            self.controlador.crear_cancha(cancha)
            
            messagebox.showinfo("Éxito", "Cancha creada exitosamente")
            self.limpiar_formulario()
            self.cargar_canchas()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cancha: {str(e)}")
    
    def cargar_canchas(self):
        """Cargar la lista de canchas en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree_canchas.get_children():
                self.tree_canchas.delete(item)
            
            # Obtener canchas
            canchas = self.controlador.listar_canchas()
            
            # Llenar tabla
            for cancha in canchas:
                # cancha = (id, nombre, tipo, costo_por_hora, estado_id, tiene_iluminacion)
                iluminacion_texto = "Sí" if cancha[5] else "No"
                
                valores = (
                    # cancha[0],  # id
                    cancha[1],  # nombre
                    cancha[2],  # tipo
                    f"${cancha[3]:.2f}",  # costo
                    iluminacion_texto  # iluminación
                )
                
                self.tree_canchas.insert('', 'end', iid=str(cancha[0]), values=valores)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar canchas: {str(e)}")
    
    def on_cancha_select(self, event):
        """Manejar selección de cancha en la tabla"""
        selection = self.tree_canchas.selection()
        if selection:
            iid = selection[0]
            item = self.tree_canchas.item(iid)
            values = item['values']
            self.cancha_seleccionada = (iid, values[0], values[1], values[2], values[3])
    
    def modificar_cancha(self):
        """Modificar la cancha seleccionada"""
        if not hasattr(self, 'cancha_seleccionada'):
            messagebox.showwarning("Advertencia", "Seleccione una cancha para modificar")
            return
        
        # Crear ventana de modificación
        self.ventana_modificar = tk.Toplevel(self.parent)
        self.ventana_modificar.title("Modificar Cancha")
        self.ventana_modificar.geometry("400x300")
        self.ventana_modificar.resizable(False, False)
        
        # Centrar ventana
        self.ventana_modificar.transient(self.parent.winfo_toplevel())
        self.ventana_modificar.grab_set()
        
        # Variables para modificación
        self.var_mod_nombre = tk.StringVar(value=self.cancha_seleccionada[1])
        self.var_mod_tipo = tk.StringVar(value=self.cancha_seleccionada[2])
        # Extraer el valor numérico del costo (quitar $ y convertir)
        costo_limpio = self.cancha_seleccionada[3].replace('$', '')
        self.var_mod_costo = tk.DoubleVar(value=float(costo_limpio))
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana_modificar, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # # Mostrar ID (no editable)
        # ttk.Label(main_frame, text=f"ID: {self.cancha_seleccionada[0]}").pack(anchor='w', pady=5)
        
        # Campos editables
        ttk.Label(main_frame, text="Nombre:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_nombre, width=40).pack(fill='x', pady=5)
        
        ttk.Label(main_frame, text="Tipo:").pack(anchor='w', pady=(10, 0))
        combo_mod_tipo = ttk.Combobox(main_frame, 
                                     textvariable=self.var_mod_tipo,
                                     values=["Futbol", "Tenis", "Padel"],
                                     state="readonly",
                                     width=37)
        combo_mod_tipo.pack(fill='x', pady=5)
        
        ttk.Label(main_frame, text="Costo por Hora:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_costo, width=40).pack(fill='x', pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame,
                  text="Guardar",
                  command=self.guardar_modificacion_cancha,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cancelar",
                  command=self.ventana_modificar.destroy).pack(side='left')
    
    def guardar_modificacion_cancha(self):
        """Guardar la modificación de la cancha"""
        try:
            from gui_helpers import GUIHelpers
            
            id_cancha = self.cancha_seleccionada[0]
            nuevo_nombre = self.var_mod_nombre.get().strip()
            nuevo_tipo = self.var_mod_tipo.get()
            nuevo_costo = self.var_mod_costo.get()
            
            if not nuevo_nombre or not nuevo_tipo:
                messagebox.showerror("Error", "Nombre y tipo son obligatorios")
                return
            
            if nuevo_costo <= 0:
                messagebox.showerror("Error", "El costo debe ser mayor a 0")
                return
            
            GUIHelpers.modificar_cancha_gui(id_cancha, nuevo_nombre, nuevo_tipo, nuevo_costo)
            
            messagebox.showinfo("Éxito", "Cancha modificada exitosamente")
            self.ventana_modificar.destroy()
            self.cargar_canchas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar cancha: {str(e)}")
    
    def eliminar_cancha(self):
        """Eliminar la cancha seleccionada"""
        if not hasattr(self, 'cancha_seleccionada'):
            messagebox.showwarning("Advertencia", "Seleccione una cancha para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar la cancha '{self.cancha_seleccionada[1]}'?"
        )
        
        if respuesta:
            try:
                id_cancha = self.cancha_seleccionada[0]
                self.controlador.eliminar_cancha(id_cancha)
                
                messagebox.showinfo("Éxito", "Cancha eliminada exitosamente")
                self.cargar_canchas()
                delattr(self, 'cancha_seleccionada')
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cancha: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar el formulario de creación"""
        self.var_nombre.set("")
        self.var_tipo.set("")
        self.var_costo.set(0.0)
        self.var_iluminacion.set(False)