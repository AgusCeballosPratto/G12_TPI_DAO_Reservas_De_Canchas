#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

# Configurar paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
config_dir = os.path.join(current_dir, 'config')

sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, config_dir)

# Importar módulos del sistema
from config.database_config import init_database
from controller.controlador_reservas import ControladorReservas

# Importar las pestañas/módulos de la GUI
from gui.cliente_gui import ClienteGUI
from gui.cancha_gui import CanchaGUI
from gui.reserva_gui import ReservaGUI
from gui.pago_gui import PagoGUI
from gui.torneo_gui import TorneoGUI
from gui.reportes_gui import ReportesGUI

class SistemaReservasGUI:
    def __init__(self):
        # Inicializar la base de datos
        init_database()
        
        # Inicializar el controlador
        self.controlador = ControladorReservas()
        
        # Crear la ventana principal
        self.root = tk.Tk()
        self.configurar_ventana_principal()
        self.configurar_estilos()
        self.crear_interfaz()
    
    def configurar_ventana_principal(self):
        """Configurar las propiedades básicas de la ventana principal"""
        self.root.title("Sistema de Reservas de Canchas - G12")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Centrar la ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Configurar el ícono 
        try:
            self.root.iconbitmap("assets/icon/icon.ico")
        except:
            pass
    
    def configurar_estilos(self):
        """Configurar los estilos y colores de la aplicación"""
        # Configurar el estilo ttk
        style = ttk.Style()
        style.theme_use('clam') 
        
        # Paleta de colores - Fondos Modernos Simples
        self.colores = {
            'primario': '#2E86AB',      # Azul principal
            'secundario': '#A23B72',    # Rosa/magenta
            'acento': '#F18F01',        # Naranja
            'fondo': "#DCDAD5",         # Blanco casi puro (moderno)
            'fondo_card': '#DCDAD5',    # Gris ultra claro (tarjetas)
            'texto': '#2C3E50',         # Azul oscuro para texto
            'exito': '#27AE60',         # Verde para éxito
            'error': '#E74C3C',         # Rojo para errores
            'warning': '#F39C12'        # Amarillo para advertencias
        }
        
        # Configurar la ventana principal
        self.root.configure(bg=self.colores['fondo'])
        
        # Estilos para los widgets ttk
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colores['primario'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colores['texto'])
        
        # Estilo para labels normales sin fondo
        style.configure('Normal.TLabel',
                       font=('Segoe UI', 9),
                       foreground=self.colores['texto'])
        
        style.configure('Card.TFrame',
                       background=self.colores['fondo_card'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Primary.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       foreground='white')
        
        style.map('Primary.TButton',
                 background=[('active', self.colores['primario']),
                           ('!active', self.colores['primario'])])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       foreground='white')
        
        style.map('Success.TButton',
                 background=[('active', self.colores['exito']),
                           ('!active', self.colores['exito'])])
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       foreground='white')
        
        style.map('Warning.TButton',
                 background=[('active', self.colores['warning']),
                           ('!active', self.colores['warning'])])
        
        style.configure('Error.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       foreground='white')
        
        style.map('Error.TButton',
                 background=[('active', self.colores['error']),
                           ('!active', self.colores['error'])])
    
    def crear_interfaz(self):
        """Crear la interfaz principal con pestañas"""
        # Marco principal sin fondo específico
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Marco para encabezado con título y logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(10, 20))
        
        # Título principal
        title_label = ttk.Label(header_frame, 
                               text="   SISTEMA DE GESTION CANCHAS MADRID",
                               style='Title.TLabel')
        title_label.pack(side='left') 
        
        # Mostrar logo de la empresa en la esquina derecha
        self.cargar_logo(header_frame)
        
        # Crear el notebook (sistema de pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestanas()
        
        # Barra de estado
        self.crear_barra_estado(main_frame)
    
    def cargar_logo(self, parent):
        """Cargar y mostrar el logo de la empresa"""
        try:
            from PIL import Image, ImageTk
            logo_path = os.path.join(current_dir, "assets", "logo", "logo_empresa.png")
            
            # Cargar y redimensionar la imagen
            img = Image.open(logo_path)
            img = img.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(img)
            
            # Crear el label con la imagen
            logo_label = tk.Label(parent, 
                                image=self.logo_photo,
                                bg=self.colores['fondo'])
            logo_label.pack(side='right', padx=(10, 0))
            
        except Exception as e:
            # Si no funciona PIL, intentar con PhotoImage básico
            try:
                self.logo_photo = tk.PhotoImage(file=os.path.join(current_dir, "assets", "logo", "logo_empresa.png"))
                # Redimensionar con subsample
                self.logo_photo = self.logo_photo.subsample(3, 3)
                logo_label = tk.Label(parent, 
                                    image=self.logo_photo,
                                    bg=self.colores['fondo'])
                logo_label.pack(side='right', padx=(10, 0))
            except:
                # Si todo falla, no mostrar logo
                pass
    
    def crear_pestanas(self):
        """Crear todas las pestañas del sistema"""
        try:
            # Pestaña Clientes
            frame_clientes = ttk.Frame(self.notebook)
            self.notebook.add(frame_clientes, text="CLIENTES")
            self.cliente_gui = ClienteGUI(frame_clientes, self.controlador, self.colores)
            
            # Pestaña Canchas
            frame_canchas = ttk.Frame(self.notebook)
            self.notebook.add(frame_canchas, text="CANCHAS")
            self.cancha_gui = CanchaGUI(frame_canchas, self.controlador, self.colores)
            
            # Pestaña Reservas
            frame_reservas = ttk.Frame(self.notebook)
            self.notebook.add(frame_reservas, text="RESERVAS")
            self.reserva_gui = ReservaGUI(frame_reservas, self.controlador, self.colores)
            
            # Pestaña Pagos
            frame_pagos = ttk.Frame(self.notebook)
            self.notebook.add(frame_pagos, text="PAGOS")
            self.pago_gui = PagoGUI(frame_pagos, self.controlador, self.colores)
            
            # Pestaña Torneos
            frame_torneos = ttk.Frame(self.notebook)
            self.notebook.add(frame_torneos, text="TORNEOS")
            self.torneo_gui = TorneoGUI(frame_torneos, self.controlador, self.colores)
            
            # Pestaña Reportes
            frame_reportes = ttk.Frame(self.notebook)
            self.notebook.add(frame_reportes, text="REPORTES")
            self.reportes_gui = ReportesGUI(frame_reportes, self.controlador, self.colores)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear las pestañas: {str(e)}")
    
    def crear_barra_estado(self, parent):
        """Crear la barra de estado en la parte inferior"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', side='bottom', pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                     text="Sistema iniciado correctamente",
                                     font=('Segoe UI', 9))
        self.status_label.pack(side='left')
        
        # Información del proyecto
        info_label = ttk.Label(status_frame,
                              text="G12 - TPI - Desarrollo de Aplicaciones con Objetos",
                              font=('Segoe UI', 9, 'italic'))
        info_label.pack(side='right')
    
    def actualizar_estado(self, mensaje):
        """Actualizar el mensaje de la barra de estado"""
        self.status_label.config(text=mensaje)
        self.root.update_idletasks()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Error en la aplicación: {str(e)}")


def main():
    """Función principal"""
    try:
        app = SistemaReservasGUI()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error", f"No se pudo iniciar la aplicación: {str(e)}")


if __name__ == "__main__":
    main()