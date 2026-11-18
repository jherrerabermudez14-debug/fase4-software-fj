"""
Módulo de registro de eventos y errores (logging) para Software FJ.
Configura la escritura persistente en un archivo de logs sin usar bases de datos.
"""

import logging
import os


def configurar_logger(ruta_archivo: str = "logs/sistema_reservas.log") -> logging.Logger:
    """
    Configura y retorna un logger que escribe eventos y errores en un archivo.
    Crea la carpeta destino automáticamente si no existe.
    """
    # Obtenemos el directorio padre de la ruta del archivo de logs
    directorio = os.path.dirname(ruta_archivo)
    # Si se especificó una carpeta y aún no existe en disco, la creamos
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    # Obtenemos o creamos una instancia única del logger del sistema
    logger = logging.getLogger("SoftwareFJ")
    # Definimos el nivel mínimo de registro en INFO para capturar eventos y errores
    logger.setLevel(logging.INFO)

    # Evitamos duplicar manejadores (handlers) si la función se llama más de una vez
    if not logger.handlers:
        # Definimos el formato con fecha/hora, nivel de severidad y mensaje
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Creamos un FileHandler con codificación UTF-8 para tildes y caracteres en español
        manejador_archivo = logging.FileHandler(ruta_archivo, mode="a", encoding="utf-8")
        # Asignamos el nivel INFO al manejador de archivo
        manejador_archivo.setLevel(logging.INFO)
        # Aplicamos el formato definido al manejador
        manejador_archivo.setFormatter(formato)
        # Agregamos el manejador al logger principal
        logger.addHandler(manejador_archivo)

    # Retornamos el logger listo para usarse en cualquier módulo
    return logger
