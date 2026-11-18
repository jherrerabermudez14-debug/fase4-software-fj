"""
Módulo controlador principal del sistema Software FJ.
Gestiona las listas internas de clientes, servicios y reservas sin bases de datos,
coordinando las operaciones y el registro en el archivo de logs.
"""

from typing import Optional
from cliente import Cliente
from excepciones import ErrorSistemaFJ, ReservaInvalidaError
from logger import configurar_logger
from reserva import Reserva
from servicios import Servicio


class SistemaSoftwareFJ:
    """Controlador central que administra clientes, servicios y reservas en memoria."""

    def __init__(self, ruta_log: str = "logs/sistema_reservas.log"):
        # Listas internas en memoria (sin motor de base de datos)
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        # Logger persistente en archivo de texto
        self._logger = configurar_logger(ruta_log)
        self._logger.info("Sistema Software FJ inicializado correctamente.")

    @property
    def clientes(self) -> list[Cliente]:
        """Retorna una copia de la lista de clientes registrados."""
        return list(self._clientes)

    @property
    def servicios(self) -> list[Servicio]:
        """Retorna una copia de la lista de servicios registrados."""
        return list(self._servicios)

    @property
    def reservas(self) -> list[Reserva]:
        """Retorna una copia de la lista de reservas registradas."""
        return list(self._reservas)

    def registrar_cliente(
        self, id_cliente: str, nombre: str, documento: str, correo: str, telefono: str
    ) -> Optional[Cliente]:
        """
        Intenta registrar un nuevo cliente capturando y registrando cualquier error en el log.
        Usa try/except/else/finally para mantener la estabilidad del programa.
        """
        cliente_creado = None
        try:
            # Verificamos que no exista otro cliente con el mismo ID o documento
            for existente in self._clientes:
                if existente.id == id_cliente or existente.documento == str(documento).strip():
                    raise ReservaInvalidaError(
                        f"Ya existe un cliente registrado con ID '{id_cliente}' o documento '{documento}'."
                    )
            cliente_creado = Cliente(id_cliente, nombre, documento, correo, telefono)
        except ErrorSistemaFJ as error_negocio:
            # Registramos el error de validación con su causa encadenada si existe
            self._logger.error(f"Error al registrar cliente '{id_cliente}': {error_negocio}", exc_info=True)
            print(f"  [ERROR CONTROLADO] {error_negocio}")
        else:
            # Si no hubo excepciones, agregamos el cliente a la lista interna
            self._clientes.append(cliente_creado)
            self._logger.info(f"Cliente registrado: {cliente_creado.obtener_resumen()}")
            print(f"  [OK] {cliente_creado.obtener_resumen()}")
        finally:
            # Confirmamos en consola el cierre limpio de la transacción
            self._logger.info(f"Fin de intento de registro de cliente '{id_cliente}'.")
        return cliente_creado

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra un objeto Servicio ya instanciado en la lista interna."""
        try:
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El objeto proporcionado no hereda de Servicio.")
            self._servicios.append(servicio)
        except ErrorSistemaFJ as error_srv:
            self._logger.error(f"Error al registrar servicio: {error_srv}", exc_info=True)
            print(f"  [ERROR CONTROLADO] {error_srv}")
            return False
        else:
            self._logger.info(f"Servicio registrado: {servicio.describir_servicio()}")
            print(f"  [OK] {servicio.describir_servicio()}")
            return True

    def crear_reserva(
        self, id_reserva: str, cliente: Optional[Cliente], servicio: Optional[Servicio], duracion: int
    ) -> Optional[Reserva]:
        """Crea una reserva integrando cliente, servicio y duración con manejo de errores."""
        reserva = None
        try:
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
        except ErrorSistemaFJ as error_res:
            self._logger.error(
                f"Fallo al crear reserva '{id_reserva}': {error_res} | Causa: {error_res.__cause__}",
                exc_info=True,
            )
            print(f"  [ERROR CONTROLADO] {error_res}")
        else:
            self._reservas.append(reserva)
            self._logger.info(f"Reserva creada: {reserva.obtener_resumen()}")
            print(f"  [OK] {reserva.obtener_resumen()}")
        return reserva

    def confirmar_y_procesar_reserva(
        self, reserva: Optional[Reserva], descuento: float = 0.0, impuesto: float = 0.19, recargo: float = 0.0
    ) -> Optional[float]:
        """Confirma y procesa una reserva existente de forma segura."""
        try:
            if reserva is None:
                raise ReservaInvalidaError("No se puede procesar una reserva inexistente (None).")
            reserva.confirmar()
            total = reserva.procesar(descuento=descuento, impuesto=impuesto, recargo=recargo)
        except ErrorSistemaFJ as error_proc:
            self._logger.error(
                f"Error procesando reserva: {error_proc} | Causa: {error_proc.__cause__}",
                exc_info=True,
            )
            print(f"  [ERROR CONTROLADO] {error_proc}")
            return None
        else:
            self._logger.info(f"Reserva procesada con éxito: {reserva.obtener_resumen()}")
            print(f"  [OK] {reserva.obtener_resumen()}")
            return total

    def cancelar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """Cancela una reserva de forma controlada registrando el evento."""
        try:
            if reserva is None:
                raise ReservaInvalidaError("No se puede cancelar una reserva nula.")
            reserva.cancelar()
        except ErrorSistemaFJ as error_canc:
            self._logger.error(f"Error al cancelar reserva: {error_canc}", exc_info=True)
            print(f"  [ERROR CONTROLADO] {error_canc}")
            return False
        else:
            self._logger.info(f"Reserva cancelada: {reserva.obtener_resumen()}")
            print(f"  [OK] {reserva.obtener_resumen()}")
            return True
