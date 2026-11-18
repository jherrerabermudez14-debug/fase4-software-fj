"""
Archivo principal de ejecución y simulación del sistema Software FJ.
Ejecuta 12 operaciones completas (válidas e inválidas) para demostrar
estabilidad, manejo avanzado de excepciones, polimorfismo y registro en logs.
"""

from excepciones import ErrorSistemaFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from sistema import SistemaSoftwareFJ


def ejecutar_simulaciones() -> None:
    """Ejecuta la batería de 12 simulaciones sin interrumpir la aplicación."""
    print("=" * 72)
    print("  SOFTWARE FJ - SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 72)

    # Inicializamos el sistema con almacenamiento en memoria y archivo de logs
    sistema = SistemaSoftwareFJ(ruta_log="logs/sistema_reservas.log")

    # ------------------------------------------------------------------
    # OPERACIÓN 1: Registro válido de cliente 1
    # ------------------------------------------------------------------
    print("\n[Operación 1] Registro válido de cliente 1:")
    cliente_1 = sistema.registrar_cliente(
        id_cliente="CLI-001",
        nombre="Ana María Torres",
        documento="1020304050",
        correo="ana.torres@ejemplo.com",
        telefono="3104567890",
    )

    # ------------------------------------------------------------------
    # OPERACIÓN 2: Registro válido de cliente 2
    # ------------------------------------------------------------------
    print("\n[Operación 2] Registro válido de cliente 2:")
    cliente_2 = sistema.registrar_cliente(
        id_cliente="CLI-002",
        nombre="Carlos Andrés Gómez",
        documento="1098765432",
        correo="carlos.gomez@empresa.co",
        telefono="3209876543",
    )

    # ------------------------------------------------------------------
    # OPERACIÓN 3: Registro inválido de cliente (documento corto y correo inválido)
    # ------------------------------------------------------------------
    print("\n[Operación 3] Registro inválido de cliente (datos mal formateados):")
    sistema.registrar_cliente(
        id_cliente="CLI-003",
        nombre="Luisa",
        documento="123",
        correo="correo_sin_arroba",
        telefono="3001112233",
    )

    # ------------------------------------------------------------------
    # OPERACIÓN 4: Registro inválido de cliente por parámetro faltante (None)
    # ------------------------------------------------------------------
    print("\n[Operación 4] Registro inválido de cliente (parámetro faltante):")
    sistema.registrar_cliente(
        id_cliente="CLI-004",
        nombre="",
        documento="1055667788",
        correo="sin.nombre@ejemplo.com",
        telefono="3150001122",
    )

    # ------------------------------------------------------------------
    # OPERACIÓN 5: Creación válida de los 3 servicios especializados
    # ------------------------------------------------------------------
    print("\n[Operación 5] Creación válida de servicios especializados:")
    sala_juntas = ReservaSala(
        id_servicio="SRV-001",
        nombre="Sala Innovación A",
        tarifa_base=80000.0,
        capacidad_maxima=12,
        incluye_proyector=True,
        disponible=True,
    )
    sistema.registrar_servicio(sala_juntas)

    equipo_portatil = AlquilerEquipo(
        id_servicio="SRV-002",
        nombre="Portátil Workstation Pro",
        tarifa_base=35000.0,
        tipo_equipo="Laptop i9 / 32GB RAM",
        stock_disponible=5,
        requiere_soporte=True,
        disponible=True,
    )
    sistema.registrar_servicio(equipo_portatil)

    asesoria_arquitectura = AsesoriaEspecializada(
        id_servicio="SRV-003",
        nombre="Consultoría Arquitectura Python",
        tarifa_base=120000.0,
        area_tematica="Patrones de Diseño y POO",
        modalidad="presencial",
        disponible=True,
    )
    sistema.registrar_servicio(asesoria_arquitectura)

    # ------------------------------------------------------------------
    # OPERACIÓN 6: Creación inválida de servicio (tarifa negativa y tipo inválido)
    # ------------------------------------------------------------------
    print("\n[Operación 6] Creación inválida de servicio (tarifa negativa):")
    try:
        sala_invalida = ReservaSala(
            id_servicio="SRV-ERR",
            nombre="Sala Defectuosa",
            tarifa_base=-50000.0,
            capacidad_maxima=8,
        )
        sistema.registrar_servicio(sala_invalida)
    except ErrorSistemaFJ as error_srv:
        # Capturamos y registramos el error de creación directamente en el log
        sistema._logger.error(f"Error creando servicio inválido: {error_srv}", exc_info=True)
        print(f"  [ERROR CONTROLADO] {error_srv}")

    # ------------------------------------------------------------------
    # OPERACIÓN 7: Creación inválida de servicio con encadenamiento de excepción
    # ------------------------------------------------------------------
    print("\n[Operación 7] Creación inválida de servicio (tarifa no numérica - encadenamiento):")
    try:
        equipo_erroneo = AlquilerEquipo(
            id_servicio="SRV-ERR2",
            nombre="Proyector 4K",
            tarifa_base="no_es_numero",  # type: ignore[arg-type]
            tipo_equipo="Audiovisual",
            stock_disponible=2,
        )
        sistema.registrar_servicio(equipo_erroneo)
    except ErrorSistemaFJ as error_tipo:
        sistema._logger.error(
            f"Error de tipo al crear servicio: {error_tipo} | Causa: {error_tipo.__cause__}",
            exc_info=True,
        )
        print(f"  [ERROR CONTROLADO] {error_tipo} (Causa: {error_tipo.__cause__})")

    # ------------------------------------------------------------------
    # OPERACIÓN 8: Reserva exitosa de sala + confirmación + procesamiento con descuento
    # ------------------------------------------------------------------
    print("\n[Operación 8] Reserva exitosa de Sala Innovación A (3h, 10% desc, IVA 19%):")
    reserva_1 = sistema.crear_reserva("RES-001", cliente_1, sala_juntas, duracion=3)
    sistema.confirmar_y_procesar_reserva(reserva_1, descuento=0.10, impuesto=0.19)

    # Demostración adicional de sobrecarga con singledispatchmethod (float vs dict)
    tarifa_float = sala_juntas.calcular_tarifa_especial(0.15, 3)
    tarifa_dict = sala_juntas.calcular_tarifa_especial(
        {"descuento": 0.15, "impuesto": 0.19, "recargo": 10000.0}, 3
    )
    print(f"  [SOBRECARGA] Tarifa con float (15% desc): ${tarifa_float:,.2f}")
    print(f"  [SOBRECARGA] Tarifa con dict (+recargo):  ${tarifa_dict:,.2f}")

    # ------------------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa de alquiler de equipo y asesoría presencial
    # ------------------------------------------------------------------
    print("\n[Operación 9] Reserva exitosa de Equipo y Asesoría Presencial:")
    reserva_2 = sistema.crear_reserva("RES-002", cliente_2, equipo_portatil, duracion=4)
    sistema.confirmar_y_procesar_reserva(reserva_2, descuento=0.0, impuesto=0.19)

    reserva_3 = sistema.crear_reserva("RES-003", cliente_1, asesoria_arquitectura, duracion=2)
    sistema.confirmar_y_procesar_reserva(reserva_3, descuento=0.05, impuesto=0.19)

    # ------------------------------------------------------------------
    # OPERACIÓN 10: Reserva fallida por servicio no disponible
    # ------------------------------------------------------------------
    print("\n[Operación 10] Reserva fallida por servicio no disponible:")
    sala_mantenimiento = ReservaSala(
        id_servicio="SRV-004",
        nombre="Sala Auditorio",
        tarifa_base=150000.0,
        capacidad_maxima=40,
        disponible=False,
    )
    sistema.registrar_servicio(sala_mantenimiento)
    sistema.crear_reserva("RES-004", cliente_2, sala_mantenimiento, duracion=2)

    # ------------------------------------------------------------------
    # OPERACIÓN 11: Reserva fallida por cálculo inconsistente (descuento > 80%)
    # ------------------------------------------------------------------
    print("\n[Operación 11] Procesamiento fallido por descuento inconsistente (95%):")
    reserva_4 = sistema.crear_reserva("RES-005", cliente_2, equipo_portatil, duracion=2)
    sistema.confirmar_y_procesar_reserva(reserva_4, descuento=0.95, impuesto=0.19)

    # ------------------------------------------------------------------
    # OPERACIÓN 12: Cancelación válida y operación no permitida sobre reserva cancelada
    # ------------------------------------------------------------------
    print("\n[Operación 12] Cancelación de reserva e intento de procesamiento prohibido:")
    sistema.cancelar_reserva(reserva_4)
    sistema.confirmar_y_procesar_reserva(reserva_4)

    # ------------------------------------------------------------------
    # RESUMEN FINAL DEL SISTEMA
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print(
        f"  RESUMEN FINAL: {len(sistema.clientes)} clientes | "
        f"{len(sistema.servicios)} servicios | {len(sistema.reservas)} reservas"
    )
    print("  Logs guardados en: logs/sistema_reservas.log")
    print("=" * 72)


if __name__ == "__main__":
    # Bloque try/except/finally de nivel superior para garantizar cierre limpio
    try:
        ejecutar_simulaciones()
    except Exception as error_fatal:
        print(f"\n[ERROR CRÍTICO NO CONTROLADO] {error_fatal}")
    finally:
        print("\nEjecución finalizada de forma estable.")
