# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto desarrollado para el componente práctico **Fase 4 – Prácticas simuladas** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Descripción

Aplicación orientada a objetos en **Python** (sin uso de bases de datos) que gestiona clientes, servicios especializados y reservas para la empresa **Software FJ**, garantizando estabilidad y robustez mediante manejo avanzado de excepciones y registro persistente en archivos de log.

## Arquitectura del proyecto

| Archivo | Responsabilidad |
| :--- | :--- |
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSistemaFJ` y 6 subclases). |
| `logger.py` | Configuración del archivo de logs (`logs/sistema_reservas.log`) en UTF-8. |
| `entidad_base.py` | Clase abstracta `EntidadBase` con atributos encapsulados y métodos abstractos. |
| `cliente.py` | Clase `Cliente` con encapsulación (`__nombre`, `__documento`, `__correo`, `__telefono`) y validaciones estrictas. |
| `servicios.py` | Clase abstracta `Servicio` y subclases polimórficas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con métodos sobrecargados (`calcular_costo_total` y `@singledispatchmethod`). |
| `reserva.py` | Clase `Reserva` con estados (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`, `PROCESADA`), confirmación, cancelación y procesamiento. |
| `sistema.py` | Controlador `SistemaSoftwareFJ` con listas en memoria y manejo `try/except/else/finally`. |
| `main.py` | Ejecución secuencial de 12 simulaciones completas (casos válidos e inválidos). |

## Requisitos y ejecución

- Python 3.10 o superior (sin dependencias externas; usa únicamente la biblioteca estándar).

```bash
python3 main.py
```

Al finalizar la ejecución, el sistema genera automáticamente el archivo `logs/sistema_reservas.log` con la trazabilidad completa de eventos y errores controlados.
