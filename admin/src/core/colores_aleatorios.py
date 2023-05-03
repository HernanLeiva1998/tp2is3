import random


def generar_color():
    """Genera un código HEX aleatorio que representa un color aleatorio"""
    color = "#"
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letras = ["A", "B", "C", "D", "E", "F"]
    for i in range(6):
        color += random.choice(nums + letras)
    return color
