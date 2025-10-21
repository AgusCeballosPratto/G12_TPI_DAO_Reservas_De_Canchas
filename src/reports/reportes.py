from dao.reserva_dao import ReservaDAO
from fpdf import FPDF 


class ReportesService:
    def __init__(self):
        self.reserva_dao = ReservaDAO()

    # tipo_reporte = 1
    def reservas_por_cliente(self):
        datos = self.reserva_dao.reservas_por_cliente()
        datos_formateados = self.formatear_datos(datos)
        self.generar_reporte_pdf(datos_formateados, tipo_reporte=1)

    # tipo_reporte = 2
    def reservas_por_cancha_en_periodo(self, cancha_id, fecha_inicio, fecha_fin):
        pass

    # tipo_reporte = 3
    def canchas_mas_utilizadas(self):
        pass

    # tipo_reporte = 4
    def grafico_utilizacion_mensual_canchas(self):
        pass
    
    # Formatear datos para reportes en PDF
    def formatear_datos(self, datos, tipo_reporte=1):
        if tipo_reporte == 1:
            return [f"DNI: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Total Reservas: {fila[3]}" for fila in datos]
    
    # Generacion de reportes en PDF
    def generar_reporte_pdf(self, datos, tipo_reporte):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
    
        if tipo_reporte == 1:
            pdf.cell(200, 10, txt="REPORTE RESERVAS POR CLIENTE", ln=True, align='C', border=1)
            
        for item in datos:
            pdf.cell(200, 10, txt=str(item), ln=True)

        pdf.output("reporte.pdf")
