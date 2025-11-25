import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sys
import os

# Configuración de paths
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from models.torneo import Torneo


class TorneoGUI:
    def __init__(self, parent, controlador, colores):
        self.parent = parent
        self.controlador = controlador
        self.colores = colores
        self.tipos_torneo = ["Futbol", "Tenis", "Padel"]

        self.var_fecha = tk.StringVar()
        self.var_hora_inicio = tk.StringVar()
        self.var_hora_fin = tk.StringVar()

        self.crear_interfaz()
        self.cargar_torneos()

    # ---------------------------
    # Generar horas
    # ---------------------------
    def generar_horas(self):
        horas = []
        for h in range(8, 24):
            horas.append(f"{h:02d}:00")
            horas.append(f"{h:02d}:30")
        return horas

    # ---------------------------
    # INTERFAZ
    # ---------------------------
    def crear_interfaz(self):
        main_canvas = tk.Canvas(self.parent, bg=self.colores["fondo"])
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Titulo
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(title_frame, text="Gestión de Torneos", style="Title.TLabel").pack(side="left")

        ttk.Button(title_frame, text="Actualizar", command=self.cargar_torneos, style="Primary.TButton").pack(side="right")

        self.crear_formulario()
        self.crear_lista_torneos()

    # ---------------------------
    # FORMULARIO DE CREACIÓN
    # ---------------------------
    def crear_formulario(self):
        form_frame = ttk.LabelFrame(self.scrollable_frame, text="Crear Nuevo Torneo", padding=15)
        form_frame.pack(fill="x", padx=20, pady=10)

        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar()

        # Nombre
        ttk.Label(form_frame, text="Nombre del Torneo:").grid(row=0, column=0, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew", padx=10)

        # Tipo
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=2, sticky="w")
        self.combo_tipo = ttk.Combobox(
            form_frame, textvariable=self.var_tipo, values=self.tipos_torneo, state="readonly"
        )
        self.combo_tipo.grid(row=0, column=3, sticky="ew", padx=10)

        # Fecha
        ttk.Label(form_frame, text="Fecha:").grid(row=1, column=0, sticky="w")
        DateEntry(form_frame, textvariable=self.var_fecha, date_pattern="yyyy-mm-dd").grid(
            row=1, column=1, sticky="ew", padx=10
        )

        # Horarios
        ttk.Label(form_frame, text="Hora inicio:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(
            form_frame, textvariable=self.var_hora_inicio, values=self.generar_horas(), state="readonly"
        ).grid(row=2, column=1, sticky="ew", padx=10)

        ttk.Label(form_frame, text="Hora fin:").grid(row=2, column=2, sticky="w")
        ttk.Combobox(
            form_frame, textvariable=self.var_hora_fin, values=self.generar_horas(), state="readonly"
        ).grid(row=2, column=3, sticky="ew", padx=10)

        # CANCHAS (listbox múltiple)
        ttk.Label(form_frame, text="Canchas disponibles:").grid(row=3, column=0, sticky="nw")

        self.listbox_canchas = tk.Listbox(form_frame, selectmode="multiple", height=6)
        self.listbox_canchas.grid(row=3, column=1, columnspan=3, sticky="ew")

        # Cargar canchas filtradas
        self.canchas_tipo_map = {}  # index → cancha_id

        def cargar_canchas(_=None):
            """Cargar canchas filtradas por tipo. Soporta dict, tupla/list u objeto."""
            self.listbox_canchas.delete(0, tk.END)
            self.canchas_tipo_map.clear()
            tipo = self.var_tipo.get().strip()
            if not tipo:
                return

            try:
                canchas = self.controlador.listar_canchas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al listar canchas: {e}")
                return

            idx = 0
            for cancha in canchas:
                # Normalizar campos según tipo de dato retornado
                if isinstance(cancha, dict):
                    cancha_tipo = cancha.get('tipo') or cancha.get('deporte') or cancha.get('tipo_deporte')
                    cancha_id = cancha.get('id') or cancha.get('cancha_id')
                    cancha_nombre = cancha.get('nombre') or cancha.get('name') or str(cancha_id)
                elif isinstance(cancha, (list, tuple)):
                    cancha_id = cancha[0] if len(cancha) > 0 else None
                    cancha_nombre = cancha[1] if len(cancha) > 1 else str(cancha_id)
                    cancha_tipo = cancha[2] if len(cancha) > 2 else None
                else:
                    cancha_id = getattr(cancha, 'id', None)
                    cancha_nombre = getattr(cancha, 'nombre', getattr(cancha, 'name', str(cancha_id)))
                    cancha_tipo = getattr(cancha, 'tipo', getattr(cancha, 'deporte', None))

                # Comparación case-insensitive y protección frente a None
                if cancha_tipo and cancha_tipo.lower() == tipo.lower():
                    self.listbox_canchas.insert(tk.END, cancha_nombre)
                    self.canchas_tipo_map[idx] = cancha_id
                    idx += 1

        # bind existente -> se mantiene pero llamamos también al cargar por defecto
        self.combo_tipo.bind("<<ComboboxSelected>>", cargar_canchas)

        # Establecer un valor por defecto y cargar canchas al abrir el formulario
        if self.tipos_torneo:
            self.combo_tipo.set(self.tipos_torneo[0])
            cargar_canchas()

        # Botones
        ttk.Button(form_frame, text="Crear Torneo", style="Success.TButton", command=self.crear_torneo).grid(
            row=4, column=1, pady=20
        )
        ttk.Button(form_frame, text="Limpiar", command=self.limpiar_formulario).grid(row=4, column=2, pady=20)

    # ---------------------------
    # Crear torneo
    # ---------------------------
    def crear_torneo(self):
        if not all(
            [
                self.var_nombre.get(),
                self.var_tipo.get(),
                self.var_fecha.get(),
                self.var_hora_inicio.get(),
                self.var_hora_fin.get(),
            ]
        ):
            messagebox.showerror("Error", "Complete todos los campos.")
            return

        indices = self.listbox_canchas.curselection()
        if not indices:
            messagebox.showerror("Error", "Seleccione al menos una cancha.")
            return

        canchas_ids = [self.canchas_tipo_map[i] for i in indices]

        torneo = Torneo(self.var_nombre.get(), self.var_tipo.get())

        try:
            self.controlador.crear_torneo(
                torneo,
                canchas_ids,
                self.var_fecha.get(),
                self.var_hora_inicio.get(),
                self.var_hora_fin.get(),
            )
            messagebox.showinfo("Éxito", "Torneo creado correctamente.")
            self.limpiar_formulario()
            self.cargar_torneos()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------
    # Lista de torneos
    # ---------------------------
    def crear_lista_torneos(self):
        frame = ttk.LabelFrame(self.scrollable_frame, text="Torneos", padding=15)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("id", "nombre", "fecha_inicio", "fecha_fin", "tipo")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=140)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        ttk.Button(frame, text="Eliminar", style="Error.TButton", command=self.eliminar_torneo).pack(
            side="left", pady=10
        )
        ttk.Button(frame, text="Ver Reservas", style="Primary.TButton", command=self.ver_reservas).pack(
            side="left", padx=10, pady=10
        )

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            self.sel_torneo = self.tree.item(sel[0])["values"]

    def cargar_torneos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for torneo in self.controlador.mostrar_torneos():
            self.tree.insert("", "end", values=torneo)

    def eliminar_torneo(self):
        if not hasattr(self, "sel_torneo"):
            messagebox.showwarning("Advertencia", "Seleccione un torneo.")
            return

        torneo_id = self.sel_torneo[0]
        self.controlador.eliminar_torneo_id(torneo_id)
        self.cargar_torneos()
        messagebox.showinfo("Éxito", "Torneo eliminado.")

    # ---------------------------
    # Mostrar reservas del torneo
    # ---------------------------
    def ver_reservas(self):
        if not hasattr(self, "sel_torneo"):
            messagebox.showwarning("Advertencia", "Seleccione un torneo.")
            return

        torneo_id = self.sel_torneo[0]
        reservas = self.controlador.listar_reservas_por_torneo(torneo_id)

        win = tk.Toplevel(self.parent)
        win.title("Reservas del Torneo")
        win.geometry("900x600")

        cols = ("id", "cliente", "cancha", "fecha", "inicio", "fin", "estado")
        tree = ttk.Treeview(win, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120)

        tree.pack(fill="both", expand=True)

        for r in reservas:
            estado = self.obtener_texto_estado(r[6])
            tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], r[5], estado))

    def obtener_texto_estado(self, estado_id):
        estados = {1: "Pendiente", 2: "Pagada", 3: "Activa", 4: "Finalizada", 5: "Cancelada"}
        return estados.get(estado_id, f"Estado {estado_id}")
    def limpiar_formulario(self):
        """Limpiar el formulario de creación de torneos."""
        # Limpiar campos de texto / combos
        self.var_nombre.set("")
        self.var_tipo.set("")
        self.var_fecha.set("")
        self.var_hora_inicio.set("")
        self.var_hora_fin.set("")

        # Limpiar selección de canchas
        if hasattr(self, "listbox_canchas"):
            self.listbox_canchas.selection_clear(0, tk.END)
