"""
Módulo base abstracto para las entidades generales del sistema Software FJ.
Aplica el principio de abstracción y encapsulación común a Clientes, Servicios y Reservas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad identificable del sistema."""

    def __init__(self, identificador: str):
        # Validamos que el identificador no sea None ni una cadena vacía
        if identificador is None or not str(identificador).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        # Atributo protegido con el identificador único de la entidad
        self._id = str(identificador).strip()
        # Atributo protegido que almacena la fecha y hora exacta de creación
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora en que fue instanciada la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que cada subclase debe implementar para validar su estado."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que retorna una descripción legible de la entidad."""
        pass
