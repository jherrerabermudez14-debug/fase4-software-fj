"""
Módulo de servicios para Software FJ.
Define la clase abstracta Servicio y tres subclases especializadas:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
Aplica herencia, polimorfismo, encapsulación y métodos sobrecargados.
"""

from abc import abstractmethod
from functools import singledispatchmethod
from entidad_base import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase):
    """Clase abstracta base para todos los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Inicializamos la entidad base con el ID del servicio
        super().__init__(id_servicio)
        # Validamos y asignamos los atributos encapsulados
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida que el nombre del servicio no sea nulo o vacío."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = str(valor).strip()

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por hora o unidad de tiempo."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida que la tarifa base sea un número positivo."""
        if valor is None:
            raise ParametroFaltanteError("La tarifa base del servicio es obligatoria.")
        try:
            # Convertimos explícitamente a flotante para detectar tipos no numéricos
            tarifa = float(valor)
        except (TypeError, ValueError) as error_tipo:
            # Encadenamos el error original de conversión a DatosInvalidosError
            raise DatosInvalidosError(
                f"La tarifa base '{valor}' debe ser un valor numérico."
            ) from error_tipo

        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor que cero.")
        self._tarifa_base = tarifa

    @property
    def disponible(self) -> bool:
        """Indica si el servicio se encuentra disponible para reservas."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Actualiza la disponibilidad del servicio."""
        self._disponible = bool(estado)

    def validar(self) -> bool:
        """Verifica la validez general de la configuración del servicio."""
        return bool(self._nombre) and self._tarifa_base > 0

    def obtener_resumen(self) -> str:
        """Retorna la descripción polimórfica del servicio."""
        return self.describir_servicio()

    @abstractmethod
    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo base del servicio según la duración solicitada."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción detallada específica de cada tipo de servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion: int, **kwargs) -> bool:
        """Valida parámetros de operación específicos de cada subclase."""
        pass

    def calcular_costo_total(
        self,
        duracion: int,
        descuento: float = 0.0,
        impuesto: float = 0.19,
        recargo: float = 0.0,
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular el costo total.
        Permite invocarse solo con duración, o agregando descuento, impuesto (IVA) y recargo.
        """
        try:
            # Validamos rangos financieros para evitar cálculos inconsistentes
            if not (0.0 <= float(descuento) <= 0.80):
                raise ValueError("El descuento debe estar entre 0.0 (0%) y 0.80 (80%).")
            if float(impuesto) < 0.0 or float(recargo) < 0.0:
                raise ValueError("El impuesto y el recargo no pueden ser negativos.")

            # Obtenemos el subtotal polimórfico de la subclase correspondiente
            subtotal = self.calcular_costo(duracion)
            # Aplicamos descuento, luego recargo y finalmente el impuesto
            monto_descontado = subtotal * (1.0 - float(descuento))
            base_imponible = monto_descontado + float(recargo)
            total = base_imponible * (1.0 + float(impuesto))
            return round(total, 2)
        except (TypeError, ValueError) as error_aritmetico:
            # Encadenamos excepciones aritméticas o de tipo a CalculoInconsistenteError
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo total para '{self._nombre}': {error_aritmetico}"
            ) from error_aritmetico

    @singledispatchmethod
    def calcular_tarifa_especial(self, ajuste, duracion: int) -> float:
        """
        Sobrecarga por tipo usando singledispatchmethod.
        Soporta ajuste como float (porcentaje de descuento) o dict (reglas completas).
        """
        raise DatosInvalidosError(
            f"Tipo de ajuste no soportado ({type(ajuste).__name__}); use float o dict."
        )

    @calcular_tarifa_especial.register
    def _(self, ajuste: float, duracion: int) -> float:
        """Variante 1: recibe un porcentaje de descuento directo como flotante."""
        return self.calcular_costo_total(duracion, descuento=ajuste)

    @calcular_tarifa_especial.register
    def _(self, ajuste: dict, duracion: int) -> float:
        """Variante 2: recibe un diccionario con claves opcionales descuento, impuesto y recargo."""
        return self.calcular_costo_total(
            duracion,
            descuento=ajuste.get("descuento", 0.0),
            impuesto=ajuste.get("impuesto", 0.19),
            recargo=ajuste.get("recargo", 0.0),
        )


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        capacidad_maxima: int,
        incluye_proyector: bool = False,
        disponible: bool = True,
    ):
        # Inicializamos la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if capacidad_maxima is None or int(capacidad_maxima) <= 0:
            raise DatosInvalidosError("La capacidad máxima de la sala debe ser mayor que cero.")
        self._capacidad_maxima = int(capacidad_maxima)
        self._incluye_proyector = bool(incluye_proyector)

    def validar_parametros(self, duracion: int, **kwargs) -> bool:
        """Valida disponibilidad, duración en horas y asistentes si se especifican."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre}' no está disponible actualmente.")
        if duracion is None or int(duracion) <= 0:
            raise DatosInvalidosError("La duración de la reserva de sala debe ser al menos 1 hora.")
        asistentes = kwargs.get("asistentes")
        if asistentes is not None and int(asistentes) > self._capacidad_maxima:
            raise DatosInvalidosError(
                f"Los asistentes ({asistentes}) superan la capacidad máxima ({self._capacidad_maxima})."
            )
        return True

    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo por hora sumando un cargo fijo si incluye proyector."""
        self.validar_parametros(duracion)
        cargo_proyector = 25000.0 if self._incluye_proyector else 0.0
        return round((self._tarifa_base * int(duracion)) + cargo_proyector, 2)

    def describir_servicio(self) -> str:
        """Retorna la descripción detallada de la sala."""
        proyector_txt = "con proyector" if self._incluye_proyector else "sin proyector"
        estado_txt = "Disponible" if self._disponible else "No disponible"
        return (
            f"Sala [{self.id}] {self._nombre} | Capacidad: {self._capacidad_maxima} pers. | "
            f"{proyector_txt} | Tarifa/h: ${self._tarifa_base:,.2f} | Estado: {estado_txt}"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        stock_disponible: int,
        requiere_soporte: bool = False,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        if int(stock_disponible) < 0:
            raise DatosInvalidosError("El stock disponible no puede ser negativo.")
        self._tipo_equipo = str(tipo_equipo).strip()
        self._stock_disponible = int(stock_disponible)
        self._requiere_soporte = bool(requiere_soporte)

    def validar_parametros(self, duracion: int, **kwargs) -> bool:
        """Valida disponibilidad, stock suficiente y duración mínima."""
        if not self._disponible or self._stock_disponible <= 0:
            raise ServicioNoDisponibleError(
                f"El equipo '{self._nombre}' ({self._tipo_equipo}) no tiene unidades disponibles."
            )
        if duracion is None or int(duracion) <= 0:
            raise DatosInvalidosError("La duración del alquiler debe ser mayor a 0 horas.")
        cantidad = kwargs.get("cantidad", 1)
        if int(cantidad) <= 0 or int(cantidad) > self._stock_disponible:
            raise DatosInvalidosError(
                f"Cantidad solicitada ({cantidad}) inválida; stock actual: {self._stock_disponible}."
            )
        return True

    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo del alquiler agregando soporte técnico si aplica."""
        self.validar_parametros(duracion)
        recargo_soporte = 15000.0 * int(duracion) if self._requiere_soporte else 0.0
        return round((self._tarifa_base * int(duracion)) + recargo_soporte, 2)

    def describir_servicio(self) -> str:
        """Retorna la descripción detallada del equipo en alquiler."""
        soporte_txt = "con soporte técnico" if self._requiere_soporte else "sin soporte"
        return (
            f"Equipo [{self.id}] {self._nombre} ({self._tipo_equipo}) | Stock: {self._stock_disponible} | "
            f"{soporte_txt} | Tarifa/h: ${self._tarifa_base:,.2f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica profesional."""

    MODALIDADES_VALIDAS = ("virtual", "presencial")

    def __init__(
        self,
        id_servicio: str,
        nombre: str,
        tarifa_base: float,
        area_tematica: str,
        modalidad: str = "virtual",
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not area_tematica or not str(area_tematica).strip():
            raise ParametroFaltanteError("El área temática de la asesoría es obligatoria.")
        mod_limpia = str(modalidad).strip().lower()
        if mod_limpia not in self.MODALIDADES_VALIDAS:
            raise DatosInvalidosError(
                f"Modalidad '{modalidad}' inválida. Opciones permitidas: {self.MODALIDADES_VALIDAS}."
            )
        self._area_tematica = str(area_tematica).strip()
        self._modalidad = mod_limpia

    def validar_parametros(self, duracion: int, **kwargs) -> bool:
        """Valida disponibilidad y duración de la sesión de asesoría."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"La asesoría '{self._nombre}' no se encuentra habilitada."
            )
        if duracion is None or int(duracion) <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser de al menos 1 hora.")
        return True

    def calcular_costo(self, duracion: int) -> float:
        """Aplica un factor adicional del 15% cuando la asesoría es presencial."""
        self.validar_parametros(duracion)
        factor_modalidad = 1.15 if self._modalidad == "presencial" else 1.0
        return round(self._tarifa_base * int(duracion) * factor_modalidad, 2)

    def describir_servicio(self) -> str:
        """Retorna la descripción detallada de la asesoría."""
        return (
            f"Asesoría [{self.id}] {self._nombre} | Área: {self._area_tematica} | "
            f"Modalidad: {self._modalidad} | Tarifa/h: ${self._tarifa_base:,.2f}"
        )
