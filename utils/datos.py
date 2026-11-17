import csv
import json
import os

# Carpeta raiz del proyecto (un nivel arriba de utils)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def leer_csv(ruta_relativa):
    """Lee un CSV y devuelve una lista de diccionarios (uno por fila)."""
    ruta = os.path.join(RAIZ, ruta_relativa)
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def leer_json(ruta_relativa):
    """Lee un archivo JSON y devuelve su contenido."""
    ruta = os.path.join(RAIZ, ruta_relativa)
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)
