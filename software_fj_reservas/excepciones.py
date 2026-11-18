"""
Módulo de excepciones personalizadas para el sistema Software FJ.
Define una jerarquía clara de errores de negocio y validación para
garantizar que la aplicación capture y gestione fallos sin detenerse.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base del sistema integral de gestión Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL"):
        # Almacenamos un código identificador para facilitar el rastreo en logs
        self.codigo = codigo
        # Llamamos al constructor de la clase padre Exception con el mensaje
        super().__init__(f"[{codigo}] {mensaje}")


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o rango esperado."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para errores de validación de datos
        super().__init__(mensaje, codigo="ERR_DATOS_INVALIDOS")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento obligatorio o es None/vacío."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para parámetros ausentes
        super().__init__(mensaje, codigo="ERR_PARAMETRO_FALTANTE")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza al intentar reservar o procesar un servicio inactivo o sin cupo."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para indisponibilidad de servicios
        super().__init__(mensaje, codigo="ERR_SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva presenta inconsistencias o referencias inválidas."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para errores en reservas
        super().__init__(mensaje, codigo="ERR_RESERVA_INVALIDA")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar ejecutar una acción inválida para el estado actual."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para transiciones de estado prohibidas
        super().__init__(mensaje, codigo="ERR_OPERACION_NO_PERMITIDA")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error aritmético o financiero al calcular costos."""

    def __init__(self, mensaje: str):
        # Asignamos un código específico para errores en cálculos de tarifas
        super().__init__(mensaje, codigo="ERR_CALCULO_INCONSISTENTE")
