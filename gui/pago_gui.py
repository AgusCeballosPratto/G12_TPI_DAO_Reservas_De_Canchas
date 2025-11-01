import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

class PagoGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.metodos_pago = ["Tarjeta de credito", "Tarjeta de debito", "Efectivo", "Transferencia"]
        self.crear_interfaz()
        self.cargar_pagos()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de pagos"""
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
                               text="Gestión de Pagos",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Botón actualizar
        refresh_btn = ttk.Button(title_frame,
                                text="Actualizar",
                                command=self.cargar_pagos,
                                style='Primary.TButton')
        refresh_btn.pack(side='right')
        
        # Frame para botones de filtro
        self.crear_filtros()
        
        # Frame para lista de pagos
        self.crear_lista_pagos()
    
    def crear_filtros(self):
        """Crear botones de filtro para ver diferentes tipos de pagos"""
        filter_frame = ttk.LabelFrame(self.scrollable_frame,
                                     text="Filtros de Visualización",
                                     padding=10)
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        btn_todos = ttk.Button(filter_frame,
                              text="Todos los Pagos",
                              command=self.cargar_pagos,
                              style='Primary.TButton')
        btn_todos.pack(side='left', padx=(0, 10))
        
        btn_pendientes = ttk.Button(filter_frame,
                                   text="Pagos Pendientes",
                                   command=self.cargar_pagos_pendientes,
                                   style='Warning.TButton')
        btn_pendientes.pack(side='left', padx=(0, 10))
        
        btn_pagados = ttk.Button(filter_frame,
                                text="Pagos Realizados",
                                command=self.cargar_pagos_realizados,
                                style='Success.TButton')
        btn_pagados.pack(side='left')
    
    def crear_lista_pagos(self):
        """Crear la lista/tabla de pagos"""
        list_frame = ttk.LabelFrame(self.scrollable_frame,
                                   text="Lista de Pagos",
                                   padding=15)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('id', 'reserva_id', 'monto', 'fecha_pago', 'metodo_pago', 'estado', 'cliente_id')
        self.tree_pagos = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_pagos.heading('id', text='ID')
        self.tree_pagos.heading('reserva_id', text='Reserva ID')
        self.tree_pagos.heading('monto', text='Monto')
        self.tree_pagos.heading('fecha_pago', text='Fecha Pago')
        self.tree_pagos.heading('metodo_pago', text='Método Pago')
        self.tree_pagos.heading('estado', text='Estado')
        self.tree_pagos.heading('cliente_id', text='Cliente DNI')
        
        # Ajustar ancho de columnas
        self.tree_pagos.column('id', width=50)
        self.tree_pagos.column('reserva_id', width=80)
        self.tree_pagos.column('monto', width=100)
        self.tree_pagos.column('fecha_pago', width=100)
        self.tree_pagos.column('metodo_pago', width=120)
        self.tree_pagos.column('estado', width=120)
        self.tree_pagos.column('cliente_id', width=100)
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_pagos.yview)
        self.tree_pagos.configure(yscrollcommand=tree_scroll.set)
        
        # Layout de la tabla
        self.tree_pagos.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Frame para botones de acciones
        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        btn_abonar = ttk.Button(actions_frame,
                               text="Abonar Pago",
                               command=self.abonar_pago,
                               style='Success.TButton')
        btn_abonar.pack(side='left')
        
        # Bind para selección
        self.tree_pagos.bind('<<TreeviewSelect>>', self.on_pago_select)
    
    def cargar_pagos(self):
        """Cargar todos los pagos en el Treeview"""
        try:
            # Limpiar tabla
            for item in self.tree_pagos.get_children():
                self.tree_pagos.delete(item)
            
            # Obtener pagos
            pagos = self.controlador.mostrar_pagos()
            
            # Estados
            estados = {5: "Pendiente", 6: "Pagado"}
            
            # Llenar tabla
            for pago in pagos:
                # pago = (id, reserva_id, monto, fecha_pago, estado_id, cliente_id, metodo_pago)
                estado_texto = estados.get(pago[4], "Desconocido")
                
                valores = (
                    pago[0],  # id
                    pago[1],  # reserva_id
                    f"${pago[2]:.2f}",  # monto
                    pago[3],  # fecha_pago
                    pago[6] if pago[6] != "Sin definir" else "-",  # metodo_pago
                    estado_texto,  # estado
                    pago[5]   # cliente_id
                )
                
                self.tree_pagos.insert('', 'end', values=valores)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pagos: {str(e)}")
    
    def cargar_pagos_pendientes(self):
        """Cargar solo los pagos pendientes"""
        try:
            # Limpiar tabla
            for item in self.tree_pagos.get_children():
                self.tree_pagos.delete(item)
            
            # Obtener pagos pendientes
            reservas_pendientes = self.controlador.mostrar_reservas_pendientes_pagos()
            
            # Los pagos pendientes se muestran a través de las reservas
            for reserva in reservas_pendientes:
                # Necesitamos obtener el pago asociado a esta reserva
                pagos = self.controlador.mostrar_pagos()
                for pago in pagos:
                    if pago[1] == reserva[0] and pago[4] == 5:  # reserva_id y estado pendiente
                        valores = (
                            pago[0],  # id
                            pago[1],  # reserva_id
                            f"${pago[2]:.2f}",  # monto
                            pago[3],  # fecha_pago
                            pago[6] if pago[6] != "Sin definir" else "-",  # metodo_pago
                            "Pendiente",  # estado
                            pago[5]   # cliente_id
                        )
                        self.tree_pagos.insert('', 'end', values=valores)
                        break
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pagos pendientes: {str(e)}")
    
    def cargar_pagos_realizados(self):
        """Cargar solo los pagos realizados"""
        try:
            # Limpiar tabla
            for item in self.tree_pagos.get_children():
                self.tree_pagos.delete(item)
            
            # Obtener pagos realizados
            reservas_pagadas = self.controlador.mostrar_reservas_pagadas()
            
            # Los pagos realizados se muestran a través de las reservas
            for reserva in reservas_pagadas:
                # Necesitamos obtener el pago asociado a esta reserva
                pagos = self.controlador.mostrar_pagos()
                for pago in pagos:
                    if pago[1] == reserva[0] and pago[4] == 6:  # reserva_id y estado pagado
                        valores = (
                            pago[0],  # id
                            pago[1],  # reserva_id
                            f"${pago[2]:.2f}",  # monto
                            pago[3],  # fecha_pago
                            pago[6] if pago[6] != "Sin definir" else "-",  # metodo_pago
                            "Pagado",  # estado
                            pago[5]   # cliente_id
                        )
                        self.tree_pagos.insert('', 'end', values=valores)
                        break
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pagos realizados: {str(e)}")
    
    def on_pago_select(self, event):
        """Manejar selección de pago en la tabla"""
        selection = self.tree_pagos.selection()
        if selection:
            item = self.tree_pagos.item(selection[0])
            values = item['values']
            self.pago_seleccionado = values
    
    def abonar_pago(self):
        """Abonar el pago seleccionado"""
        if not hasattr(self, 'pago_seleccionado'):
            messagebox.showwarning("Advertencia", "Seleccione un pago para abonar")
            return
        
        if self.pago_seleccionado[5] == "Pagado":
            messagebox.showwarning("Advertencia", "Este pago ya está abonado")
            return
        
        # Crear ventana para abonar pago
        self.ventana_abonar = tk.Toplevel(self.parent)
        self.ventana_abonar.title("Abonar Pago")
        self.ventana_abonar.geometry("400x400") 
        self.ventana_abonar.resizable(False, False)
        
        # Centrar ventana
        self.ventana_abonar.transient(self.parent.winfo_toplevel())
        self.ventana_abonar.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana_abonar, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Información del pago
        info_frame = ttk.LabelFrame(main_frame, text="Información del Pago", padding=10)
        info_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(info_frame, text=f"ID Pago: {self.pago_seleccionado[0]}").pack(anchor='w', pady=2)
        ttk.Label(info_frame, text=f"ID Reserva: {self.pago_seleccionado[1]}").pack(anchor='w', pady=2)
        ttk.Label(info_frame, text=f"Monto: {self.pago_seleccionado[2]}").pack(anchor='w', pady=2)
        ttk.Label(info_frame, text=f"Cliente DNI: {self.pago_seleccionado[6]}").pack(anchor='w', pady=2)
        
        # Selección de método de pago
        method_frame = ttk.LabelFrame(main_frame, text="Método de Pago", padding=10)
        method_frame.pack(fill='x', pady=(0, 20))
        
        self.var_metodo_pago = tk.StringVar()
        
        for i, metodo in enumerate(self.metodos_pago):
            ttk.Radiobutton(method_frame,
                           text=metodo,
                           variable=self.var_metodo_pago,
                           value=metodo).pack(anchor='w', pady=2)
        
        # Establecer método por defecto
        self.var_metodo_pago.set(self.metodos_pago[0])
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame,
                  text="Confirmar Pago",
                  command=self.confirmar_pago,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cancelar",
                  command=self.ventana_abonar.destroy).pack(side='left')
    
    def confirmar_pago(self):
        """Confirmar el pago con el método seleccionado"""
        try:
            if not self.var_metodo_pago.get():
                messagebox.showerror("Error", "Seleccione un método de pago")
                return
            
            # Usar el controlador para abonar el pago
            self.controlador.abonar_pago(
                int(self.pago_seleccionado[0]),  # ID del pago
                self.var_metodo_pago.get()       # Método de pago
            )
            
            messagebox.showinfo("Éxito", "Pago abonado exitosamente")
            self.ventana_abonar.destroy()
            self.cargar_pagos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abonar pago: {str(e)}")
