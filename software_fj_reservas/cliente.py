"""
Módulo de gestión de clientes para Software FJ.
Implementa encapsulación estricta mediante atributos privados y validaciones robustas.
"""

import re
from entidad_base import EntidadBase
from excepciones import DatosInvalidosError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Representa a un cliente registrado en el sistema Software FJ."""

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str, telefono: str):
        # Inicializamos la clase base con el identificador del cliente
        super().__init__(id_cliente)
        # Asignamos los datos usando las propiedades para activar las validaciones
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        # Ejecutamos la validación integral de la entidad
        self.validar()

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        # Verificamos que el parámetro no sea nulo o vacío
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        nombre_limpio = str(valor).strip()
        # Exigimos una longitud mínima razonable para un nombre real
        if len(nombre_limpio) < 3:
            raise DatosInvalidosError(f"El nombre '{nombre_limpio}' debe tener al menos 3 caracteres.")
        self.__nombre = nombre_limpio

    @property
    def documento(self) -> str:
        """Retorna el número de documento de identidad."""
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Valida que el documento contenga solo dígitos y tenga longitud adecuada."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        doc_limpio = str(valor).strip()
        # Comprobamos que el documento sea numérico y tenga entre 5 y 15 dígitos
        if not doc_limpio.isdigit() or not (5 <= len(doc_limpio) <= 15):
            raise DatosInvalidosError(
                f"El documento '{doc_limpio}' es inválido; debe tener entre 5 y 15 dígitos numéricos."
            )
        self.__documento = doc_limpio

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato básico de correo electrónico mediante expresión regular."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        correo_limpio = str(valor).strip().lower()
        # Patrón estándar para validar usuario@dominio.extension
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, correo_limpio):
            raise DatosInvalidosError(f"El correo electrónico '{correo_limpio}' no tiene un formato válido.")
        self.__correo = correo_limpio

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico de contacto."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga entre 7 y 15 dígitos."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or not (7 <= len(tel_limpio) <= 15):
            raise DatosInvalidosError(
                f"El teléfono '{tel_limpio}' es inválido; debe contener entre 7 y 15 dígitos."
            )
        self.__telefono = tel_limpio

    def validar(self) -> bool:
        """Verifica que todos los atributos encapsulados estén correctamente inicializados."""
        return all([self.__nombre, self.__documento, self.__correo, self.__telefono])

    def obtener_resumen(self) -> str:
        """Retorna una cadena formateada con la información principal del cliente."""
        return (
            f"Cliente [{self.id}] {self.__nombre} | Doc: {self.__documento} | "
            f"Correo: {self.__correo} | Tel: {self.__telefono}"
        )
