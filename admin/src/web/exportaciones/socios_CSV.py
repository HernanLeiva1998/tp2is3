import csv
from io import StringIO

from flask import make_response


def generar_CSV(datos_socios):
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
    for dict in datos_socios:
        del dict["password"]
        del dict["photo_path"]
    si = StringIO()
    with open("socios.csv", "w") as f:
        escritor = csv.DictWriter(si, fieldnames = headers)
        escritor.writeheader()
        escritor.writerows(datos_socios)
        salida = make_response(si.getvalue())
        salida.headers.set(
            "Content-Disposition", "attachment", filename = "socios" + ".csv"
         )
        salida.headers.set("Content-Type", "application/csv")
    return salida
