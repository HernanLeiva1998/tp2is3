from fpdf import FPDF
from datetime import datetime
from flask import make_response, render_template


class PDFCarnet(FPDF):
    def header(self):
        self.set_font("Arial", "B", 25)
        self.set_xy(0, 0)
        self.cell(200, 40, "Club Deportivo Villa Elisa", 0, 0, "L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page" + str(self.page_no()) + "/{nb}", 0, 0, "C")


def generar_carnet_PDF(socio, photo, url, estado):
    """Genera el pdf de una cuota paga"""
    pdf = PDFCarnet()
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.set_font("Arial", "B", 16)
    pdf.set_font("Arial", "", 12)
    pdf.image(photo, 5, 30, w=40, h=40)
    pdf.cell(0, ln=1)
    pdf.text(60, 35, str(socio.apellido + " " + socio.nombre))
    pdf.text(60, 40, str(socio.tipo_documento + ": " + socio.dni))
    pdf.text(60, 45, str("Socio: #" + str(socio.id)))
    pdf.text(60, 50, str("Fecha alta: " + str(socio.inserted_at.strftime("%Y-%m-%d"))))
    pdf.text(20, 80, "Estado:")
    if estado:
        pdf.text(20, 85, "Al día")
    else:
        pdf.text(20, 85, "No esta al día")
    pdf.image(
        "http://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=" + url + "&.png",
        55,
        55,
    )
    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set(
        "Content-Disposition", "attachment", filename="Carnet" + ".pdf"
    )
    response.headers.set("Content-Type", "application/pdf")
    return response
