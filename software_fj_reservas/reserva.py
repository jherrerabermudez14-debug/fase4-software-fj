"""
Módulo de gestión de reservas para Software FJ.
Integra Cliente, Servicio, duración y estado, implementando confirmación,
cancelación y procesamiento con manejo avanzado de excepciones.
"""

from cliente import Cliente
from entidad_base import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
)
from servicios import Servicio


class Reserva(EntidadBase):
    """Representa una reserva que vincula un cliente con un servicio de Software FJ."""

    # Estados válidos del ciclo de vida de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_PROCESADA = "PROCESADA"

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        # Inicializamos la entidad base con el ID de la reserva
        super().__init__(id_reserva)

        # Validamos que el cliente sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")
        # Validamos que el servicio sea una instancia válida de Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")

        # Validamos la duración convertida a entero con encadenamiento de excepción
        try:
            duracion_int = int(duracion)
        except (TypeError, ValueError) as error_duracion:
            raise DatosInvalidosError(
                f"La duración '{duracion}' debe ser un número entero de horas."
            ) from error_duracion

        if duracion_int <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser mayor que cero.")

        # Validamos parámetros específicos del servicio (incluye disponibilidad)
        try:
            servicio.validar_parametros(duracion_int)
        except Exception as error_servicio:
            # Encadenamos el error específico del servicio dentro de ReservaInvalidaError
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva [{id_reserva}]: {error_servicio}"
            ) from error_servicio

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion_int
        self._estado = self.ESTADO_PENDIENTE
        self._total_pagar = 0.0

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio asociado a la reserva."""
        return self._servicio

    @property
    def duracion(self) -> int:
        """Retorna la duración en horas."""
        return self._duracion

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva."""
        return self._estado

    @property
    def total_pagar(self) -> float:
        """Retorna el monto total calculado tras procesar la reserva."""
        return self._total_pagar

    def validar(self) -> bool:
        """Valida que el cliente, el servicio y la duración sigan siendo consistentes."""
        return (
            isinstance(self._cliente, Cliente)
            and isinstance(self._servicio, Servicio)
            and self._duracion > 0
        )

    def confirmar(self) -> None:
        """Confirma una reserva que se encuentre en estado PENDIENTE."""
        if self._estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva [{self.id}] porque ya fue cancelada."
            )
        if self._estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id}] ya fue procesada anteriormente."
            )
        # Revalidamos disponibilidad del servicio al momento de confirmar
        self._servicio.validar_parametros(self._duracion)
        self._estado = self.ESTADO_CONFIRMADA

    def cancelar(self) -> None:
        """Cancela una reserva siempre que no haya sido procesada."""
        if self._estado == self.ESTADO_PROCESADA:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva [{self.id}] porque ya fue procesada."
            )
        if self._estado == self.ESTADO_CANCELADA:
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id}] ya se encuentra en estado CANCELADA."
            )
        self._estado = self.ESTADO_CANCELADA

    def procesar(self, descuento: float = 0.0, impuesto: float = 0.19, recargo: float = 0.0) -> float:
        """
        Procesa el cobro final de la reserva usando el método sobrecargado del servicio.
        Utiliza bloques try/except/else/finally para garantizar consistencia.
        """
        if self._estado != self.ESTADO_CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id}] debe estar CONFIRMADA para procesarse (estado actual: {self._estado})."
            )

        calculo_exitoso = False
        try:
            # Invocamos el método sobrecargado de Servicio para calcular el total
            monto = self._servicio.calcular_costo_total(
                self._duracion,
                descuento=descuento,
                impuesto=impuesto,
                recargo=recargo,
            )
        except CalculoInconsistenteError:
            # Re-lanzamos la excepción de cálculo para que el controlador la registre en logs
            raise
        except Exception as error_inesperado:
            # Encadenamos cualquier error imprevisto
            raise CalculoInconsistenteError(
                f"Fallo inesperado al procesar reserva [{self.id}]: {error_inesperado}"
            ) from error_inesperado
        else:
            # Solo si el bloque try tuvo éxito actualizamos el total y el estado
            self._total_pagar = monto
            self._estado = self.ESTADO_PROCESADA
            calculo_exitoso = True
            return self._total_pagar
        finally:
            # Bloque finally de auditoría interna de cierre de intento de procesamiento
            _ = calculo_exitoso

    def obtener_resumen(self) -> str:
        """Retorna una descripción completa del estado actual de la reserva."""
        return (
            f"Reserva [{self.id}] | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion}h | "
            f"Estado: {self._estado} | Total: ${self._total_pagar:,.2f}"
        )
