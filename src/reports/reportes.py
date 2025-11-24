from dao.reserva_dao import ReservaDAO
from fpdf import FPDF 
from datetime import date
import matplotlib.pyplot as plt
import os

class ReportesService:
    def __init__(self):
        self.reserva_dao = ReservaDAO()

    # tipo_reporte = 1
    def reservas_por_cliente(self):
        resumen = self.reserva_dao.reservas_por_cliente()
        detalles = self.reserva_dao.detalle_reservas_por_cliente()

        self.generar_reporte_pdf((resumen, detalles), tipo_reporte=1)


    # tipo_reporte = 2
    def reservas_por_cancha_en_periodo(self, fecha_inicio, fecha_fin):
        # Obtener detalle de reservas (cancha, fecha, hora_inicio, hora_fin, monto)
        detalles = self.reserva_dao.reservas_detalle_por_cancha_en_periodo(fecha_inicio, fecha_fin)

        # Agrupar por cancha
        datos_por_cancha = {}
        for fila in detalles:
            cancha = fila[0]
            fecha = fila[1]
            hora_inicio = fila[2]
            hora_fin = fila[3]
            monto = fila[4]
            datos_por_cancha.setdefault(cancha, []).append((fecha, hora_inicio, hora_fin, monto))

        # Generar PDF con detalle en forma de tabla por cancha
        self.generar_reporte_pdf_detalle_por_cancha(datos_por_cancha, fecha_inicio, fecha_fin)

    # tipo_reporte = 3
    def canchas_mas_utilizadas(self):
        resumen = self.reserva_dao.canchas_mas_utilizadas()

        # Obtener detalle por cada cancha
        detalles = {}
        for fila in resumen:
            cancha = fila[0]    # nombre cancha
            detalles[cancha] = self.reserva_dao.reservas_detalle_por_cancha(cancha)

        self.generar_reporte_pdf((resumen, detalles), tipo_reporte=3)


    # tipo_reporte = 4
    def grafico_utilizacion_mensual_canchas(self):
        datos = self.reserva_dao.grafico_utilizacion_mensual_canchas()
        self.generar_imagen_utilizacion_mensual_canchas(datos)
        self.generar_reporte_pdf([], tipo_reporte=4)
        
    # tipo_reporte = 5
    def facturacion_mensual(self):
        resumen = self.reserva_dao.facturacion_mensual()
        detalle = self.reserva_dao.detalle_facturacion_mensual()
        #datos_formateados = self.formatear_datos(datos, tipo_reporte=5)
        self.generar_reporte_pdf((resumen, detalle), tipo_reporte=5)
    
    # Formatear datos para reportes en PDF
    def formatear_datos(self, datos, tipo_reporte):
        if tipo_reporte == 1:
            return [f"DNI: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Total Reservas: {fila[3]}" for fila in datos]
       
        if tipo_reporte == 2:
            return datos
            # return [f"Periodo: {fila[0]} - {fila[1]}, Total Reservas: {fila[3]}, Cancha: {fila[2]}" for fila in datos]
        
        if tipo_reporte == 3:
            return [f"Nombre Cancha: {fila[0]}, Total Reservas: {fila[1]}" for fila in datos]
        
        if tipo_reporte == 5:
            return [f"Mes: {fila[0]}, Facturación Total: ${fila[1]:.2f}" for fila in datos]

    # Generacion de reportes en PDF
    def generar_reporte_pdf(self, datos, tipo_reporte):
        pdf = FPDF()
        pdf.add_page()
        
        # Marca de agua
        try:
            pdf.image("assets/logo/logo_empresa.png", x=30, y=60, w=150, h=0)
        except:
            pass 
            
        pdf.set_font("Arial", size=12)
        
        # Encabezados segun tipo de reporte
        if tipo_reporte == 1:
            pdf.cell(200, 10, txt="REPORTE RESERVAS POR CLIENTE", ln=True, align='C', border=1)
            
        if tipo_reporte == 2:
            pdf.cell(200, 10, txt="REPORTE RESERVAS POR CANCHA EN PERIODO", ln=True, align='C', border=1)
            
        if tipo_reporte == 3:
            pdf.cell(200, 10, txt="REPORTE CANCHAS MAS UTILIZADAS", ln=True, align='C', border=1)
        
        if tipo_reporte == 4:   
            pdf.cell(200, 10, txt="UTILIZACION MENSUAL DE CANCHAS", ln=True, align='C', border=1)
            
        if tipo_reporte == 5:
            pdf.cell(200, 10, txt="REPORTE FACTURACION MENSUAL", ln=True, align='C', border=1)
        
        # Contenido del reporte
        if tipo_reporte in [ 4]:
            for item in datos:
                pdf.cell(200, 10, txt=str(item), ln=True)
        
        
        # Guardar el PDF con un nombre segun el tipo de reporte
        if tipo_reporte == 1:
            resumen, detalle = datos

            pdf.set_font("Arial", "B", 13)
            pdf.ln(5)
            pdf.cell(200, 8, txt="RESUMEN DE RESERVAS POR CLIENTE", ln=True)

            # ============================
            # RESUMEN GENERAL (nombre + total)
            # ============================
            pdf.set_font("Arial", size=11)
            for fila in resumen:
                dni, nombre, apellido, total = fila
                pdf.cell(200, 7, txt=f"{dni} - {nombre} {apellido}  | Total: {total}", ln=True)

            # ============================
            # DETALLE POR CLIENTE
            # ============================
            pdf.ln(10)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(200, 8, txt="DETALLE POR CLIENTE", ln=True)
            pdf.ln(3)

            # Agrupar detalles por cliente
            detalle_por_cliente = {}
            for fila in detalle:
                dni, nombre, apellido, fecha, hi, hf, cancha, deporte = fila
                key = f"{dni} - {nombre} {apellido}"
                detalle_por_cliente.setdefault(key, []).append(
                    (fecha, hi, hf, cancha, deporte)
                )

            # ============================
            # TABLAS DE DETALLE
            # ============================
            for cliente, filas in detalle_por_cliente.items():
                pdf.set_font("Arial", "B", 12)
                pdf.cell(200, 8, txt=f"CLIENTE: {cliente}", ln=True)
                pdf.set_font("Arial", size=11)
                pdf.ln(2)

                # Encabezado tabla
                pdf.set_font("Arial", "B", 10)
                pdf.set_fill_color(200, 200, 200)
                pdf.cell(30, 8, "Fecha", border=1, align="C", fill=True)
                pdf.cell(25, 8, "Inicio", border=1, align="C", fill=True)
                pdf.cell(25, 8, "Fin", border=1, align="C", fill=True)
                pdf.cell(60, 8, "Cancha", border=1, align="C", fill=True)
                pdf.cell(40, 8, "Deporte", border=1, align="C", fill=True)
                pdf.ln()

                pdf.set_font("Arial", size=10)

                for fila in filas:
                    fecha, hi, hf, cancha, deporte = fila
                    pdf.cell(30, 7, fecha, border=1)
                    pdf.cell(25, 7, hi, border=1)
                    pdf.cell(25, 7, hf, border=1)
                    pdf.cell(60, 7, cancha, border=1)
                    pdf.cell(40, 7, deporte, border=1)
                    pdf.ln()

                pdf.ln(5)

                # Salto de página automático
                if pdf.get_y() > 250:
                    pdf.add_page()

            ruta = f"reporte_reservas_por_cliente_{date.today()}.pdf"
            pdf.output(ruta)
            self.abrir_pdf(ruta)
            

        #nuevo nuevo
        if tipo_reporte == 2:
            for fila in datos:
                fecha_inicio = fila[0]
                fecha_fin = fila[1]
                nombre_cancha = fila[2]
                total = fila[3]

                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(200, 8, txt=f"CANCHA: {nombre_cancha}", ln=True)

                pdf.set_font("Arial", size=11)
                pdf.multi_cell(
                    200,
                    7,
                    txt=(
                        f"Período: {fecha_inicio} al {fecha_fin}\n"
                        f"Total de reservas: {total}"
                    ),
                )

                pdf.ln(3)
                pdf.set_draw_color(0, 0, 0)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())

            ruta = f"reporte_reservas_por_cancha_en_periodo_{date.today()}.pdf"
            pdf.output(ruta)
            self.abrir_pdf(ruta)


        if tipo_reporte == 3:
            resumen, detalles = datos

            pdf.set_font("Arial", "B", 14)
            pdf.ln(5)
            pdf.cell(200, 8, txt="REPORTE CANCHAS MAS UTILIZADAS", ln=True, align="C")
            pdf.ln(5)

            # -------------------------
            # RESUMEN GENERAL
            # -------------------------
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 8, txt="RESUMEN", ln=True)
            pdf.set_font("Arial", size=11)

            for fila in resumen:
                cancha, total = fila
                pdf.cell(200, 7, txt=f"{cancha}: {total} reservas", ln=True)

            pdf.ln(8)

            # -------------------------
            # DETALLE POR CANCHA
            # -------------------------
            for cancha, lista in detalles.items():

                pdf.set_font("Arial", "B", 12)
                pdf.cell(200, 8, txt=f"DETALLE - {cancha}", ln=True)
                pdf.cell(200, 8, txt=f"Deporte: {lista[0][4]}", ln=True)

                pdf.ln(3)

                # Encabezados de tabla:
                pdf.set_font("Arial", "B", 10)
                pdf.set_fill_color(200, 200, 200)
                pdf.cell(30, 8, "Fecha", border=1, fill=True)
                pdf.cell(20, 8, "Inicio", border=1, fill=True)
                pdf.cell(20, 8, "Fin", border=1, fill=True)
                pdf.cell(40, 8, "Cliente", border=1, fill=True)
                pdf.cell(30, 8, "Servicio", border=1, fill=True)
                pdf.cell(30, 8, "Estado", border=1, fill=True)
                pdf.ln()

                pdf.set_font("Arial", size=10)

                for fila in lista:
                    fecha, hi, hf, cliente, deporte, estado, servicio, monto = fila

                    pdf.cell(30, 7, fecha, border=1)
                    pdf.cell(20, 7, hi, border=1)
                    pdf.cell(20, 7, hf, border=1)
                    pdf.cell(40, 7, cliente, border=1)
                    pdf.cell(30, 7, servicio, border=1)
                    pdf.cell(30, 7, estado, border=1)
                    pdf.ln()

                # Línea separadora
                pdf.ln(5)
                pdf.set_draw_color(0, 0, 0)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)

                # Salto de página automático
                if pdf.get_y() > 250:
                    pdf.add_page()

            ruta = f"reporte_canchas_mas_utilizadas_{date.today()}.pdf"
            pdf.output(ruta)
            self.abrir_pdf(ruta)

       
        if tipo_reporte == 4:
            pdf.image("img_temporal.png", x=10, y=35, w=180)
            ruta = f"reporte_grafico_utilizacion_mensual_canchas_{date.today()}.pdf"  
            pdf.output(ruta)
            os.remove("img_temporal.png")
            self.abrir_pdf(ruta)
            
        if tipo_reporte == 5:
            resumen, detalle = datos
            #resumen mensual
            pdf.set_font("Arial", "B", 13)
            pdf.ln(5)
            pdf.cell(200, 8, txt="RESUMEN MENSUAL", ln=True)

            pdf.set_font("Arial", size=11)
            for fila in resumen:
                mes = fila[0]
                total = fila[1]
                pdf.cell(200, 7, txt=f"Mes: {mes}  -  Total: ${total:.2f}", ln=True)

            #resumen mensual  detallado
            pdf.ln(10)
            pdf.set_font("Arial", "B", 13)
            pdf.cell(200, 8, txt="DETALLE DE PAGOS", ln=True)
            pdf.ln(3)

            # Encabezados de tabla
            pdf.set_font("Arial", "B", 10)
            pdf.set_fill_color(200, 200, 200)

            pdf.cell(20, 8, "Mes", border=1, align="C", fill=True)
            pdf.cell(25, 8, "Monto", border=1, align="C", fill=True)
            pdf.cell(30, 8, "Fecha Pago", border=1, align="C", fill=True)
            pdf.cell(40, 8, "Reserva", border=1, align="C", fill=True)
            pdf.cell(45, 8, "Cancha", border=1, align="C", fill=True)
            pdf.cell(30, 8, "Deporte", border=1, align="C", fill=True)
            pdf.ln()

            # Filas de tabla
            pdf.set_font("Arial", size=10)

            for fila in detalle:
                mes, monto, fecha_pago, fecha_reserva, hora_inicio, cancha, deporte = fila

                pdf.cell(20, 7, mes, border=1)
                pdf.cell(25, 7, f"${monto:.2f}", border=1)
                pdf.cell(30, 7, fecha_pago, border=1)
                pdf.cell(40, 7, f"{fecha_reserva}, {hora_inicio}", border=1)
                pdf.cell(45, 7, cancha, border=1)
                pdf.cell(30, 7, deporte, border=1)
                pdf.ln()

            ruta = f"reporte_facturacion_mensual_{date.today()}.pdf"
            pdf.output(ruta)
            self.abrir_pdf(ruta)


    def generar_reporte_pdf_detalle_por_cancha(self, datos_por_cancha, fecha_inicio, fecha_fin):
        """Genera un PDF con detalle de reservas por cancha en forma de tabla.

        `datos_por_cancha` es un dict: {cancha_nombre: [(fecha,h_inicio,h_fin,monto), ...], ...}
        """
        pdf = FPDF()
        pdf.add_page()

        try:
            pdf.image("assets/logo/logo_empresa.png", x=30, y=60, w=150, h=0)
        except:
            pass

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="REPORTE RESERVAS POR CANCHA EN PERIODO - DETALLE", ln=True, align='C', border=1)
        pdf.ln(4)

        # Para cada cancha, dibujar un cuadro con encabezado y tabla
        for cancha, filas in datos_por_cancha.items():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 8, txt=f"CANCHA: {cancha}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 7, txt=f"Período: {fecha_inicio} al {fecha_fin}", ln=True)
            pdf.ln(2)

            # Encabezado de tabla
            pdf.set_font("Arial", "B", 11)
            w_fecha = 50
            w_hi = 45
            w_hf = 45
            w_monto = 40
            pdf.cell(w_fecha, 8, txt="Fecha", border=1, align='C')
            pdf.cell(w_hi, 8, txt="Hora inicio", border=1, align='C')
            pdf.cell(w_hf, 8, txt="Hora fin", border=1, align='C')
            pdf.cell(w_monto, 8, txt="Monto", border=1, align='C', ln=True)

            pdf.set_font("Arial", size=11)
            # Filas
            for fila in filas:
                fecha, hi, hf, monto = fila
                pdf.cell(w_fecha, 7, txt=str(fecha), border=1)
                pdf.cell(w_hi, 7, txt=str(hi), border=1)
                pdf.cell(w_hf, 7, txt=str(hf), border=1)
                pdf.cell(w_monto, 7, txt=f"${monto:.2f}", border=1, ln=True)

            # Total reservas para la cancha
            total = len(filas)
            pdf.ln(2)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(200, 7, txt=f"Total reservas: {total}", ln=True)
            pdf.ln(4)

            # Línea separadora
            pdf.set_draw_color(0, 0, 0)
            y = pdf.get_y()
            pdf.line(10, y, 200, y)
            pdf.ln(4)

            # Nueva página si estamos muy al final
            if pdf.get_y() > 250:
                pdf.add_page()

        ruta = f"reporte_reservas_por_cancha_en_periodo_detalle_{date.today()}.pdf"
        pdf.output(ruta)
        self.abrir_pdf(ruta)

    # Generacion de imagen para grafico de utilizacion mensual de canchas 
    def generar_imagen_utilizacion_mensual_canchas(self, datos):
        
        meses = [fila[0] for fila in datos]
        utilizacion = [fila[1] for fila in datos]
    
        plt.figure(figsize=(10,6)) 
        plt.bar(meses, utilizacion, color='blue')
        plt.xlabel('Mes')
        plt.ylabel('Cantidad de Reservas')
        plt.title('Utilización Mensual de Canchas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        ruta_imagen = f"img_temporal.png"
        plt.savefig(ruta_imagen)
        plt.close()
        
        # Abrir PDF automáticamente luego de generarlo (solo Windows)
    def abrir_pdf(self, ruta_pdf):
        try:
            os.startfile(ruta_pdf)
        except Exception as e:
            print(f"No se pudo abrir el PDF automáticamente: {e}")

        