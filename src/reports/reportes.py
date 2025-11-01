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
        datos = self.reserva_dao.reservas_por_cliente()
        datos_formateados = self.formatear_datos(datos, tipo_reporte=1)
        self.generar_reporte_pdf(datos_formateados, tipo_reporte=1)

    # tipo_reporte = 2
    def reservas_por_cancha_en_periodo(self, fecha_inicio, fecha_fin):
        datos = self.reserva_dao.reservas_por_cancha_en_periodo(fecha_inicio, fecha_fin)
        datos_formateados = self.formatear_datos(datos, tipo_reporte=2)
        self.generar_reporte_pdf(datos_formateados, tipo_reporte=2)

    # tipo_reporte = 3
    def canchas_mas_utilizadas(self):
        datos = self.reserva_dao.canchas_mas_utilizadas()
        datos_formateados = self.formatear_datos(datos, tipo_reporte=3)
        self.generar_reporte_pdf(datos_formateados, tipo_reporte=3)

    # tipo_reporte = 4
    def grafico_utilizacion_mensual_canchas(self):
        datos = self.reserva_dao.grafico_utilizacion_mensual_canchas()
        self.generar_imagen_utilizacion_mensual_canchas(datos)
        self.generar_reporte_pdf([], tipo_reporte=4)
        
    # tipo_reporte = 5
    def facturacion_mensual(self):
        datos = self.reserva_dao.facturacion_mensual()
        datos_formateados = self.formatear_datos(datos, tipo_reporte=5)
        self.generar_reporte_pdf(datos_formateados, tipo_reporte=5)
    
    # Formatear datos para reportes en PDF
    def formatear_datos(self, datos, tipo_reporte):
        if tipo_reporte == 1:
            return [f"DNI: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Total Reservas: {fila[3]}" for fila in datos]
        
        if tipo_reporte == 2:
            return [f"Periodo: {fila[0]} - {fila[1]}, Total Reservas: {fila[2]}" for fila in datos]
        
        if tipo_reporte == 3:
            return [f"Nombre Cancha: {fila[0]}, Total Reservas: {fila[1]}" for fila in datos]
        
        if tipo_reporte == 5:
            return [f"Mes: {fila[0]}, Facturación Total: ${fila[1]:.2f}" for fila in datos]

    # Generacion de reportes en PDF
    def generar_reporte_pdf(self, datos, tipo_reporte):
        pdf = FPDF()
        pdf.add_page()
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
        for item in datos:
            pdf.cell(200, 10, txt=str(item), ln=True)
        
        # Guardar el PDF con un nombre segun el tipo de reporte
        if tipo_reporte == 1:
            pdf.output(f"reporte_reservas_por_cliente_{date.today()}.pdf")
        
        if tipo_reporte == 2:
            pdf.output(f"reporte_reservas_por_cancha_en_periodo_{date.today()}.pdf")

        if tipo_reporte == 3:
            pdf.output(f"reporte_canchas_mas_utilizadas_{date.today()}.pdf")
       
        if tipo_reporte == 4:
            pdf.image("img_temporal.png", x=10, y=35, w=180)  
            pdf.output(f"reporte_grafico_utilizacion_mensual_canchas_{date.today()}.pdf")
            os.remove("img_temporal.png")
            
        if tipo_reporte == 5:
            pdf.output(f"reporte_facturacion_mensual_{date.today()}.pdf")

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
        
        