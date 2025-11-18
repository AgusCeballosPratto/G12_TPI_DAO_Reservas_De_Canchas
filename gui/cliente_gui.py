import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from models.cliente import Cliente

class ClienteGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.crear_interfaz()
        self.cargar_clientes()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de clientes"""
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
                               text="Gestión de Clientes",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Botón actualizar
        refresh_btn = ttk.Button(title_frame,
                                text="Actualizar",
                                command=self.cargar_clientes,
                                style='Primary.TButton')
        refresh_btn.pack(side='right')
        
        # Frame para formulario de creación
        self.crear_formulario_cliente()
        
        # Frame para lista de clientes
        self.crear_lista_clientes()
    
    def crear_formulario_cliente(self):
        """Crear el formulario para agregar/editar clientes"""
        form_frame = ttk.LabelFrame(self.scrollable_frame, 
                                   text="Agregar Nuevo Cliente",
                                   padding=15)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Variables del formulario
        self.var_dni = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telefono = tk.StringVar()
        
        # Grid para el formulario
        campos = [
            ("DNI:", self.var_dni),
            ("Nombre:", self.var_nombre),
            ("Apellido:", self.var_apellido),
            ("Email:", self.var_email),
            ("Teléfono:", self.var_telefono)
        ]
        
        for i, (label_text, var) in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(form_frame, text=label_text).grid(
                row=row, column=col, sticky='w', padx=(0, 10), pady=5
            )
            
            entry = ttk.Entry(form_frame, textvariable=var, width=25)
            entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 20), pady=5)
        
        # Configurar el grid
        for i in range(4):
            form_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(20, 0))
        
        btn_crear = ttk.Button(button_frame,
                              text="Crear Cliente",
                              command=self.crear_cliente,
                              style='Success.TButton')
        btn_crear.pack(side='left', padx=(0, 10))
        
        btn_limpiar = ttk.Button(button_frame,
                                text="Limpiar",
                                command=self.limpiar_formulario)
        btn_limpiar.pack(side='left')
    
    def crear_lista_clientes(self):
        """Crear la lista/tabla de clientes"""
        list_frame = ttk.LabelFrame(self.scrollable_frame,
                                   text="Lista de Clientes",
                                   padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('dni', 'nombre', 'apellido', 'email', 'telefono')
        self.tree_clientes = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_clientes.heading('dni', text='DNI')
        self.tree_clientes.heading('nombre', text='Nombre')
        self.tree_clientes.heading('apellido', text='Apellido')
        self.tree_clientes.heading('email', text='Email')
        self.tree_clientes.heading('telefono', text='Teléfono')
        
        # Ajustar ancho de columnas
        self.tree_clientes.column('dni', width=100)
        self.tree_clientes.column('nombre', width=120)
        self.tree_clientes.column('apellido', width=120)
        self.tree_clientes.column('email', width=200)
        self.tree_clientes.column('telefono', width=120)
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=tree_scroll.set)
        
        # Layout de la tabla
        self.tree_clientes.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')

        # Frame para botones de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        btn_modificar = ttk.Button(actions_frame,
                                  text="Modificar",
                                  command=self.modificar_cliente,
                                  style='Primary.TButton')
        btn_modificar.pack(side='left', padx=(0, 10))
        
        btn_eliminar = ttk.Button(actions_frame,
                                 text="Eliminar",
                                 command=self.eliminar_cliente,
                                 style='Error.TButton')
        btn_eliminar.pack(side='left')
        
        # Bind para selección
        self.tree_clientes.bind('<<TreeviewSelect>>', self.on_cliente_select)
    
    def crear_cliente(self):
        """Crear un nuevo cliente"""
        try:
            # Validar campos obligatorios
            if not all([self.var_dni.get(), self.var_nombre.get(), 
                       self.var_apellido.get(), self.var_email.get(), 
                       self.var_telefono.get()]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Crear objeto cliente
            cliente = Cliente(
                dni=self.var_dni.get().strip(),
                nombre=self.var_nombre.get().strip(),
                apellido=self.var_apellido.get().strip(),
                email=self.var_email.get().strip(),
                telefono=self.var_telefono.get().strip()
            )
            
            # Usar el servicio para crear el cliente
            self.controlador.crear_cliente(cliente)
            
            messagebox.showinfo("Éxito", "Cliente creado exitosamente")
            self.limpiar_formulario()
            self.cargar_clientes()
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear cliente: {str(e)}")
    
    def cargar_clientes(self):
        """Cargar la lista de clientes en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree_clientes.get_children():
                self.tree_clientes.delete(item)
            
            # Obtener clientes
            clientes = self.controlador.listar_clientes()
            
            # Llenar tabla
            for cliente in clientes:
                self.tree_clientes.insert('', 'end', values=cliente)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")
    
    def on_cliente_select(self, event):
        """Manejar selección de cliente en la tabla"""
        selection = self.tree_clientes.selection()
        if selection:
            item = self.tree_clientes.item(selection[0])
            values = item['values']
            self.cliente_seleccionado = values
    
    def modificar_cliente(self):
        """Modificar el cliente seleccionado"""
        if not hasattr(self, 'cliente_seleccionado'):
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar")
            return
        
        # Crear ventana de modificación
        self.ventana_modificar = tk.Toplevel(self.parent)
        self.ventana_modificar.title("Modificar Cliente")
        self.ventana_modificar.geometry("400x400")
        self.ventana_modificar.resizable(False, False)
        
        # Centrar ventana
        self.ventana_modificar.transient(self.parent.winfo_toplevel())
        self.ventana_modificar.grab_set()
        
        # Variables para modificación (solo email y teléfono)
        self.var_mod_nombre = tk.StringVar(value=self.cliente_seleccionado[1])
        self.var_mod_apellido = tk.StringVar(value=self.cliente_seleccionado[2])
        self.var_mod_email = tk.StringVar(value=self.cliente_seleccionado[3])
        self.var_mod_telefono = tk.StringVar(value=self.cliente_seleccionado[4])
        # Frame principal
        main_frame = ttk.Frame(self.ventana_modificar, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Mostrar DNI y nombre (no editables)
        ttk.Label(main_frame, text=f"DNI: {self.cliente_seleccionado[0]}").pack(anchor='w', pady=5)
        # ttk.Label(main_frame, text=f"Nombre: {self.cliente_seleccionado[1]} {self.cliente_seleccionado[2]}").pack(anchor='w', pady=5)
        ttk.Label(main_frame, text="Nuevo Nombre:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_nombre, width=40).pack(fill='x', pady=5)

        ttk.Label(main_frame, text="Nuevo Apellido:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_apellido, width=40).pack(fill='x', pady=5)
        
        
        # Campos editables
        ttk.Label(main_frame, text="Nuevo Email:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_email, width=40).pack(fill='x', pady=5)
        
        ttk.Label(main_frame, text="Nuevo Teléfono:").pack(anchor='w', pady=(10, 0))
        ttk.Entry(main_frame, textvariable=self.var_mod_telefono, width=40).pack(fill='x', pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame,
                  text="Guardar",
                  command=self.guardar_modificacion,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cancelar",
                  command=self.ventana_modificar.destroy).pack(side='left')
    
    def guardar_modificacion(self):
        """Guardar la modificación del cliente"""
        try:
            from gui_helpers import GUIHelpers
            
            dni = self.cliente_seleccionado[0]
            nuevo_nombre = self.var_mod_nombre.get().strip()
            nuevo_apellido = self.var_mod_apellido.get().strip()
            nuevo_email = self.var_mod_email.get().strip()
            nuevo_telefono = self.var_mod_telefono.get().strip()
            
            if not nuevo_email or not nuevo_telefono or not nuevo_nombre or not nuevo_apellido:
                messagebox.showerror("Error", "Email y teléfono son obligatorios")
                return
            
            GUIHelpers.modificar_cliente_gui(dni, nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_telefono)
            
            messagebox.showinfo("Éxito", "Cliente modificado exitosamente")
            self.ventana_modificar.destroy()
            self.cargar_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar cliente: {str(e)}")
    
    def eliminar_cliente(self):
        """Eliminar el cliente seleccionado"""
        if not hasattr(self, 'cliente_seleccionado'):
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar al cliente {self.cliente_seleccionado[1]} {self.cliente_seleccionado[2]}?\n"
            f"DNI: {self.cliente_seleccionado[0]}"
        )
        
        if respuesta:
            try:
                dni = self.cliente_seleccionado[0]
                self.controlador.eliminar_cliente(dni)
                
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente")
                self.cargar_clientes()
                delattr(self, 'cliente_seleccionado')
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar el formulario de creación"""
        self.var_dni.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_email.set("")
        self.var_telefono.set("")