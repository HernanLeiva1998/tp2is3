import csv
from io import StringIO

from flask import make_response


def generar_CSV(data_socios):
    """Esta funcion retorna un CSV con todos los datos de los socios"""
    headers = [
        "nro_socio",
        "apellido",
        "nombre",
        "tipo_documento",
        "dni",
        "email",
        "telefono",
        "direccion",
        "genero",
        "activo",
    ]
    for dict in data_socios:
        del dict["password"]
        del dict["photo_path"]
    si = StringIO()
    with open("socios.csv", "w") as f:
        writer = csv.DictWriter(si, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_socios)
        output = make_response(si.getvalue())
        output.headers.set(
            "Content-Disposition", "attachment", filename="socios" + ".csv"
        )
        output.headers.set("Content-Type", "application/csv")
    return output
