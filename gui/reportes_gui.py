import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import date
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

class ReportesGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear la interfaz para gestión de reportes"""
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
                               text="Generación de Reportes",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Crear secciones de reportes
        self.crear_reportes_simples()
        self.crear_reporte_periodo()
        self.crear_reportes_avanzados()
    
    def crear_reportes_simples(self):
        """Crear sección de reportes simples (sin parámetros)"""
        simple_frame = ttk.LabelFrame(self.scrollable_frame,
                                     text="Reportes Generales",
                                     padding=15)
        simple_frame.pack(fill='x', padx=20, pady=10)
        
        # Información
        info_label = ttk.Label(simple_frame,
                              text="Estos reportes se generan automáticamente en formato PDF",
                              font=('Segoe UI', 9, 'italic'))
        info_label.pack(anchor='w', pady=(0, 15))
        
        # Grid para botones
        buttons_frame = ttk.Frame(simple_frame)
        buttons_frame.pack(fill='x')
        
        # Botón 1: Reservas por Cliente
        btn_reservas_cliente = ttk.Button(buttons_frame,
                                         text="Reservas por Cliente",
                                         command=self.generar_reservas_por_cliente,
                                         style='Primary.TButton',
                                         width=25)
        btn_reservas_cliente.grid(row=0, column=0, padx=(0, 10), pady=5, sticky='ew')
        
        # Botón 2: Canchas más utilizadas
        btn_canchas_utilizadas = ttk.Button(buttons_frame,
                                           text="Canchas Más Utilizadas",
                                           command=self.generar_canchas_mas_utilizadas,
                                           style='Primary.TButton',
                                           width=25)
        btn_canchas_utilizadas.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='ew')
        
        # Botón 3: Gráfico de utilización mensual
        btn_grafico_mensual = ttk.Button(buttons_frame,
                                        text="Gráfico Utilización Mensual",
                                        command=self.generar_grafico_utilizacion,
                                        style='Success.TButton',
                                        width=25)
        btn_grafico_mensual.grid(row=1, column=0, padx=(0, 10), pady=5, sticky='ew')
        
        # Botón 4: Facturación mensual
        btn_facturacion = ttk.Button(buttons_frame,
                                    text="Facturación Mensual",
                                    command=self.generar_facturacion_mensual,
                                    style='Success.TButton',
                                    width=25)
        btn_facturacion.grid(row=1, column=1, padx=(0, 10), pady=5, sticky='ew')
        
        # Configurar grid
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
    
    def crear_reporte_periodo(self):
        """Crear sección para reporte por período"""
        periodo_frame = ttk.LabelFrame(self.scrollable_frame,
                                      text="Reporte por Período",
                                      padding=15)
        periodo_frame.pack(fill='x', padx=20, pady=10)
        
        # Información
        info_label = ttk.Label(periodo_frame,
                              text="Generar reporte de reservas por cancha en un período específico",
                              font=('Segoe UI', 9, 'italic'))
        info_label.pack(anchor='w', pady=(0, 15))
        
        # Frame para fechas
        fecha_frame = ttk.Frame(periodo_frame)
        fecha_frame.pack(fill='x', pady=(0, 15))
        
        # Variables para fechas
        self.var_fecha_inicio = tk.StringVar()
        self.var_fecha_fin = tk.StringVar()
        
        # Fecha inicio
        ttk.Label(fecha_frame, text="Fecha Inicio:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.date_inicio = DateEntry(fecha_frame,
                                    textvariable=self.var_fecha_inicio,
                                    date_pattern='yyyy-mm-dd',
                                    width=15)
        self.date_inicio.grid(row=0, column=1, sticky='w', padx=(0, 30), pady=5)
        
        # Fecha fin
        ttk.Label(fecha_frame, text="Fecha Fin:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=5)
        self.date_fin = DateEntry(fecha_frame,
                                 textvariable=self.var_fecha_fin,
                                 date_pattern='yyyy-mm-dd',
                                 width=15)
        self.date_fin.grid(row=0, column=3, sticky='w', padx=(0, 30), pady=5)
        
        # Botón generar
        btn_periodo = ttk.Button(fecha_frame,
                                text="Generar Reporte por Período",
                                command=self.generar_reporte_periodo,
                                style='Primary.TButton')
        btn_periodo.grid(row=0, column=4, padx=(20, 0), pady=5)
    
    def crear_reportes_avanzados(self):
        """Crear sección para reportes avanzados y configuraciones"""
        avanzado_frame = ttk.LabelFrame(self.scrollable_frame,
                                       text="Configuraciones y Estado",
                                       padding=15)
        avanzado_frame.pack(fill='x', padx=20, pady=10)
        
        # Frame para información del sistema
        info_frame = ttk.Frame(avanzado_frame)
        info_frame.pack(fill='x', pady=(0, 15))
        
        # Mostrar información del sistema
        self.label_estado = ttk.Label(info_frame,
                                     text="Sistema listo para generar reportes",
                                     font=('Segoe UI', 9))
        self.label_estado.pack(anchor='w')
        
        # Frame para botones adicionales
        extra_frame = ttk.Frame(avanzado_frame)
        extra_frame.pack(fill='x')
        
        # Botón para abrir carpeta de reportes
        btn_abrir_carpeta = ttk.Button(extra_frame,
                                      text="Abrir Carpeta de Reportes",
                                      command=self.abrir_carpeta_reportes)
        btn_abrir_carpeta.pack(side='left', padx=(0, 10))
        
        # Botón para actualizar estado
        btn_actualizar = ttk.Button(extra_frame,
                                   text="Actualizar Estado",
                                   command=self.actualizar_estado)
        btn_actualizar.pack(side='left')
    
    def generar_reservas_por_cliente(self):
        """Generar reporte de reservas por cliente"""
        try:
            self.actualizar_estado_label("Generando reporte de reservas por cliente...")
            self.controlador.reservas_por_cliente()
            
            self.actualizar_estado_label("Reporte de reservas por cliente generado exitosamente")
            messagebox.showinfo("Éxito", 
                               "Reporte de reservas por cliente generado exitosamente.\n"
                               "El archivo PDF se encuentra en la carpeta del proyecto.")
            
        except Exception as e:
            self.actualizar_estado_label("Error al generar reporte")
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generar_canchas_mas_utilizadas(self):
        """Generar reporte de canchas más utilizadas"""
        try:
            self.actualizar_estado_label("Generando reporte de canchas más utilizadas...")
            self.controlador.canchas_mas_utilizadas()
            
            self.actualizar_estado_label("Reporte de canchas más utilizadas generado exitosamente")
            messagebox.showinfo("Éxito", 
                               "Reporte de canchas más utilizadas generado exitosamente.\n"
                               "El archivo PDF se encuentra en la carpeta del proyecto.")
            
        except Exception as e:
            self.actualizar_estado_label("Error al generar reporte")
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generar_grafico_utilizacion(self):
        """Generar gráfico de utilización mensual"""
        try:
            self.actualizar_estado_label("Generando gráfico de utilización mensual...")
            self.controlador.grafico_utilizacion_mensual_canchas()
            
            self.actualizar_estado_label("Gráfico de utilización mensual generado exitosamente")
            messagebox.showinfo("Éxito", 
                               "Gráfico de utilización mensual generado exitosamente.\n"
                               "El archivo PDF con el gráfico se encuentra en la carpeta del proyecto.")
            
        except Exception as e:
            self.actualizar_estado_label("Error al generar gráfico")
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
    
    def generar_facturacion_mensual(self):
        """Generar reporte de facturación mensual"""
        try:
            self.actualizar_estado_label("Generando reporte de facturación mensual...")
            self.controlador.facturacion_mensual()
            
            self.actualizar_estado_label("Reporte de facturación mensual generado exitosamente")
            messagebox.showinfo("Éxito", 
                               "Reporte de facturación mensual generado exitosamente.\n"
                               "El archivo PDF se encuentra en la carpeta del proyecto.")
            
        except Exception as e:
            self.actualizar_estado_label("Error al generar reporte")
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generar_reporte_periodo(self):
        """Generar reporte por período"""
        try:
            # Validar fechas
            fecha_inicio = self.var_fecha_inicio.get()
            fecha_fin = self.var_fecha_fin.get()
            
            if not fecha_inicio or not fecha_fin:
                messagebox.showerror("Error", "Debe seleccionar ambas fechas")
                return
            
            # Validar que fecha inicio sea menor que fecha fin
            if fecha_inicio > fecha_fin:
                messagebox.showerror("Error", "La fecha de inicio debe ser anterior a la fecha de fin")
                return
            
            self.actualizar_estado_label(f"Generando reporte por período: {fecha_inicio} a {fecha_fin}...")
            self.controlador.reservas_por_cancha_en_periodo(fecha_inicio, fecha_fin)
            
            self.actualizar_estado_label("Reporte por período generado exitosamente")
            messagebox.showinfo("Éxito", 
                               f"Reporte por período ({fecha_inicio} a {fecha_fin}) generado exitosamente.\n"
                               "El archivo PDF se encuentra en la carpeta del proyecto.")
            
        except Exception as e:
            self.actualizar_estado_label("Error al generar reporte")
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def abrir_carpeta_reportes(self):
        """Abrir la carpeta donde se guardan los reportes"""
        try:
            import subprocess
            import platform
            
            # Obtener la carpeta actual del proyecto
            carpeta_proyecto = os.path.dirname(os.path.dirname(__file__))
            
            # Abrir la carpeta según el sistema operativo
            if platform.system() == "Windows":
                subprocess.run(["explorer", carpeta_proyecto])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", carpeta_proyecto])
            else:  # Linux
                subprocess.run(["xdg-open", carpeta_proyecto])
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {str(e)}")
    
    def actualizar_estado(self):
        """Actualizar el estado del sistema"""
        try:
            # Obtener estadísticas del sistema
            clientes = len(self.controlador.listar_clientes())
            canchas = len(self.controlador.listar_canchas())
            reservas = len(self.controlador.listar_reservas())
            
            estado_texto = (f"Sistema activo - Clientes: {clientes}, "
                          f"Canchas: {canchas}, Reservas: {reservas}")
            
            self.actualizar_estado_label(estado_texto)
            
        except Exception as e:
            self.actualizar_estado_label(f"Error al actualizar estado: {str(e)}")
    
    def actualizar_estado_label(self, mensaje):
        """Actualizar el label de estado"""
        self.label_estado.config(text=mensaje)
        self.parent.update_idletasks()