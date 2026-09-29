# 📦 PyOrder B2B Engine

Un motor de procesamiento, validación y liquidación de órdenes corporativas (B2B) construido 100% en Python.

Este proyecto simula el backend de un sistema de ventas mayorista, enfocado en recibir datos, sanitizarlos, aplicar reglas de negocio complejas y generar un registro de auditoría.

## 🚀 Características Principales (Versión 1.0)

- **Sanitización de Datos:** Limpieza automática de inputs (espacios extra, formatos de texto, validación de números).
- **Validación de Integridad:** Bloqueo de transacciones si el SKU no existe, si la cantidad supera el stock o si la ciudad no tiene cobertura.
- **Motor de Precios:**
  - Cálculo de subtotal e IVA (19%).
  - Descuentos dinámicos por cupones (`VIPTECH`, `B2BWELCOME`) o por compras mayoristas (>= 5 unidades).
  - Lógica de envío gratuito condicionada a topes de compra o cupones especiales.
- **Gestión de Inventario en Memoria:** Actualización del stock en tiempo real y generación de alertas automáticas de reabastecimiento.
- **Auditoría:** Registro de cada transacción exitosa en un historial de operaciones.

## 🛠️ Tecnologías y Conceptos Aplicados

- **Lenguaje:** Python 3.x
- **Estructuras de Datos:** Diccionarios anidados, listas y tuplas.
- **Control de Flujo:** Condicionales (`if/elif/else`) y operadores lógicos, aritméticos y de pertenencia.
- **Manipulación de Strings:** f-strings y métodos nativos (`.strip()`, `.upper()`, `.replace()`, `.isdigit()`).

## 💻 Cómo ejecutarlo

Asegúrate de tener Python instalado en tu computadora. Abre la terminal dentro de la carpeta del proyecto y ejecuta:

```bash
python main.py
```
🗺️ Hoja de Ruta (Roadmap)
Este repositorio evolucionará a medida que avance en el aprendizaje de Python:

[x] v1.0 (Actual): Script transaccional único (estructuras de datos, condicionales).

[ ] v2.0: Implementación de bucles (while/for) para procesar múltiples órdenes continuas.

[ ] v3.0: Refactorización con funciones (def) para código modular y manejo de errores (try/except).

[ ] v4.0: Persistencia de datos (lectura y guardado en JSON/CSV) y Programación Orientada a Objetos (POO).
