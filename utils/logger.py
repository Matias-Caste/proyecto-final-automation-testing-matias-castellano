import logging
import os
from datetime import datetime

CARPETA_REPORTES = "reports"

# Un archivo de log por cada ejecucion, con fecha y hora en el nombre
os.makedirs(CARPETA_REPORTES, exist_ok=True)
NOMBRE_LOG = datetime.now().strftime("log_%Y%m%d_%H%M%S.log")
RUTA_LOG = os.path.join(CARPETA_REPORTES, NOMBRE_LOG)


def crear_logger(nombre):
    """Devuelve un logger que escribe en consola y en el archivo de log."""
    logger = logging.getLogger(nombre)

    # Si ya tiene handlers no los agrego de nuevo (para no duplicar mensajes)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    handler_archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    handler_archivo.setFormatter(formato)
    logger.addHandler(handler_archivo)

    handler_consola = logging.StreamHandler()
    handler_consola.setFormatter(formato)
    logger.addHandler(handler_consola)

    return logger
