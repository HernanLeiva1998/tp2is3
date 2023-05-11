from fpdf import FPDF
from datetime import datetime

from flask import make_response


class PdfRecibo(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_xy(0, 0)
        self.cell(200, 40, "Recibo de pago", 0, 0, "R")
        self.ln(10)

        
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page" + str(self.page_no()) + "/{nb}", 0, 0, "C")


def generar_recibo_PDF(dato):
    """Genera el pdf de una cuota paga"""
    pdf = PDFRecibo()
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 20, f"{datetime.now().date()}", ln = 1)
    pdf.cell(500, 30, dato["encabezado"], ln = 1)

    pdf.set_font("Arial", "B", 12)
    y_height = 5
    pdf.set_xy(0, 50)
    pdf.cell(15)
    pdf.cell(70, y_height, "Número de recibo: " + str(dato["pago"].id))
    pdf.cell(15)
    pdf.cell(
        70,
        y_height,
        "Cuota numero "
        + str(dato["pago"].nro_cuota)
        + " del año "
        + str(dato["pago"].año_cuota),
        ln = 1,
    )
    pdf.cell(0, y_height, "", ln=1)
    pdf.cell(
        180,
        y_height,
        "Socio: " + dato["pago"].socio.apellido + " " + dato["pago"].socio.nombre,
        ln = 1,
    )

    pdf.cell(0, y_height, "", ln = 1)
    pdf.cell(180, y_height, "Disciplinas:", ln = 1)

    total_disciplinas = dato["cuota_base"]
    pdf.cell(150, y_height, "-Cuota basica ")
    pdf.cell(30, y_height, "$" + str(dato["cuota_base"]), ln = 1)

    for disciplina in dato["pago"].socio.disciplinas:
        total_disciplinas = total_disciplinas + float(disciplina.costo)
        pdf.cell(
            150,
            y_height,
            "-" + disciplina.nombre + " Categoría: " + disciplina.categoria,
        )
        pdf.cell(30, y_height, "$" + str(disciplina.costo), ln = 1)

    pdf.cell(150, y_height, "Costo total de disciplinas:")
    pdf.cell(30, y_height, "$" + str(total_disciplinas))
    pdf.cell(0, 10, "", ln=1)
    pdf.cell(150, y_height, "Porcentaje de recargo para cuotas vencidas: ")
    pdf.cell(30, y_height, "%" + str(dato["recargo"]), ln = 1)
    pdf.cell(150, y_height, "Monto total:")
    pdf.cell(30, y_height, "$" + str(dato["pago"].total), ln = 1)
    pdf.cell(150, y_height, "Fecha de pago:")
    pdf.cell(30, y_height, 
             str(data["pago"].fecha_pago.strftime("%Y-%m-%d")), ln = 1)

    pdf.set_font("Arial", "", 12)
    respuesta = make_response(pdf.output(dest="S").encode("latin-1"))
    respuesta.headers.set("Content-Disposition",
                         "attachment", filename = "Recibo" + ".pdf")
    respuesta.headers.set("Content-Type", "application/pdf")
    return respuesta
