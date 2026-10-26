# ==============================================================================
# PROYECTO: PyOrder B2B Engine - Sistema de Validación y Liquidación de Órdenes
# VERSIÓN: 2.0.0 (Continuous Order Processing & Session Auditing)
# ==============================================================================

# 1. DATOS COMPUESTOS (Base de datos en memoria)
CONFIG_FINANCIERA = (0.19, 25.00, 1000.00)

catalogo = {
    "LAP-01": {"nombre": "Laptop Pro 16", "precio": 1200.00, "stock": 5},
    "MON-02": {"nombre": "Monitor 4K 27", "precio": 350.00, "stock": 12},
    "SSD-03": {"nombre": "Disco Solido 1TB", "precio": 95.00, "stock": 3}
}

cupones_activos = {
    "B2BWELCOME": 0.10,
    "VIPTECH": 0.15
}

ciudades_cobertura = ["Bogota", "Medellin", "Cali", "Barranquilla", "Sincelejo"]
productos_disponibles = ["LAP-01", "MON-02", "SSD-03"]
alertas_reabastecimiento = []
historial_transacciones = []

# ==============================================================================
# BUCLE PRINCIPAL DE ATENCIÓN DE PEDIDOS
# ==============================================================================
while True:
    print("\n" + "=" * 65)
    print("📦 SISTEMA CORPORATIVO DE PROCESAMIENTO DE ÓRDENES B2B v2.0")
    print(f"SKUs con disponibilidad de venta: {productos_disponibles}")
    print("=" * 65)

    registro = input("\n¿Desea procesar una orden nueva? (Si/No): ").strip().upper()
    if registro != "SI":
        print("\nSaliendo del registro de órdenes y generando consolidado del día...")
        break

    # Validación de Cliente
    cliente = input("\nIngrese el nombre completo del cliente: ").strip().title()
    while not cliente:
        print("\n❌ Error Crítico: El nombre del cliente no puede estar vacío.")
        cliente = input("Ingrese el nombre correcto del cliente: ").strip().title()

    # Validación de NIT/ID
    id_cliente = (
        input("\nIngrese el NIT/ID del cliente: ")
        .strip()
        .replace("-", "")
        .replace(".", "")
        .replace(",", "")
        .replace(" ", "")
    )
    while not id_cliente.isdigit():
        print("\n❌ Error Crítico: El ID del cliente debe contener solo números.")
        id_cliente = (
            input("Ingrese el NIT/ID del cliente correctamente: ")
            .strip()
            .replace("-", "")
            .replace(".", "")
            .replace(",", "")
            .replace(" ", "")
        )

    # Validación de SKU y verificación de existencia
    sku = input("\nIngrese el SKU del producto: ").strip().upper()
    while sku not in catalogo:
        print(f"\n❌ Error de Catálogo: el SKU '{sku}' no se encuentra en el inventario.")
        print(f"Opciones válidas: {list(catalogo.keys())}")
        sku = input("Ingrese un SKU existente: ").strip().upper()

    producto = catalogo.get(sku)
    stock_actual = producto.get("stock")
    precio_unitario = producto.get("precio")
    nombre_producto = producto.get("nombre")

    # Validación si el SKU seleccionado ya no tiene existencias
    if stock_actual == 0:
        print(f"\n⚠️ El producto '{nombre_producto}' ({sku}) se encuentra agotado actualmente.")
        continue

    # Validación robusta de cantidad (número positivo y dentro del stock)
    while True:
        cantidad_str = input(f"\nIngrese la cantidad a comprar (Disponibles: {stock_actual}): ").strip()
        if not cantidad_str.isdigit():
            print("\n❌ Error Crítico: La cantidad debe ser un número entero positivo.")
            continue
        
        cantidad = int(cantidad_str)
        if cantidad <= 0 or cantidad > stock_actual:
            print(f"\n❌ Error de Inventario: Debe solicitar entre 1 y {stock_actual} unidades.")
            continue
        
        break

    # Validación de Ciudad
    ciudad = input("\nIngrese la ciudad de entrega: ").strip().title()
    while ciudad not in ciudades_cobertura:
        print(f"\n❌ Error Logístico: Sin cobertura en '{ciudad}'. Cobertura: {ciudades_cobertura}")
        ciudad = input("Ingrese una ciudad válida: ").strip().title()

    cupon = input("\nIngrese el cupón de descuento (Enter si no aplica): ").strip().upper()

    # Cálculos Financieros
    subtotal = precio_unitario * cantidad

    if cupon in cupones_activos:
        porcentaje_descuento = cupones_activos.get(cupon)
        motivo_descuento = f"\nCupón {cupon} ({porcentaje_descuento * 100:.0f}%)"
        print(motivo_descuento)
    elif cantidad >= 5:
        porcentaje_descuento = 0.05
        motivo_descuento = "\nDescuento Mayorista Automático (5%)"
        print(motivo_descuento)
    else:
        porcentaje_descuento = 0.0
        motivo_descuento = "\nSin descuento (0%)"
        print(motivo_descuento)

    monto_descuento = subtotal * porcentaje_descuento
    subtotal_con_descuento = subtotal - monto_descuento
    iva = subtotal_con_descuento * CONFIG_FINANCIERA[0]

    if subtotal_con_descuento >= CONFIG_FINANCIERA[2] or cupon == "VIPTECH":
        costo_envio = 0.00
    else:
        costo_envio = CONFIG_FINANCIERA[1]

    total_factura = subtotal_con_descuento + iva + costo_envio

    # Actualización de Inventario en Memoria
    nuevo_stock = stock_actual - cantidad
    producto.update({"stock": nuevo_stock})

    if nuevo_stock == 0 and sku in productos_disponibles:
        productos_disponibles.remove(sku)
        alertas_reabastecimiento.append(sku)
        print(f"\n⚠️ Alerta de Inventario: '{sku}' se ha quedado sin existencias.")

    # Almacenamiento en el Historial de Transacciones
    registro_orden = {
        "cliente": cliente,
        "id_cliente": id_cliente,
        "ciudad": ciudad,
        "sku": sku,
        "producto": nombre_producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
        "descuento": monto_descuento,
        "motivo_descuento": motivo_descuento,
        "subtotal_neto": subtotal_con_descuento,
        "iva": iva,
        "envio": costo_envio,
        "total_factura": total_factura,
        "stock_restante": nuevo_stock
    }
    historial_transacciones.append(registro_orden)
    print(f"\n✅ ¡Orden registrada exitosamente para {cliente}!")


# ==============================================================================
# AUDITORÍA Y EMISIÓN DE FACTURAS (BUCLE FOR)
# ==============================================================================
if historial_transacciones:
    recaudo_total = 0.0

    print("\n" + "#" * 65)
    print("📋 RELACIÓN DE FACTURAS PROCESADAS EN LA SESIÓN")
    print("#" * 65)

    for i, orden in enumerate(historial_transacciones, 1):
        # Sumamos al acumulador global usando la información de cada orden específica
        recaudo_total += orden.get("total_factura")

        print("\n" + "=" * 65)
        print(f"🧾 FACTURA N° {i} - PYORDER B2B")
        print("=" * 65)
        print(f"Cliente:                {orden.get('cliente')} (ID: {orden.get('id_cliente')})")
        print(f"Ciudad de Destino:      {orden.get('ciudad')}")
        print(f"Producto:               {orden.get('producto')} [{orden.get('sku')}]")
        print(f"Cantidad:               {orden.get('cantidad')} x ${orden.get('precio_unitario'):,.2f}")
        print("-" * 65)
        print(f"Subtotal Bruto:         ${orden.get('subtotal'):,.2f}")
        print(f"Beneficio Aplicado:     {orden.get('motivo_descuento')}")
        print(f"Descuento:             -${orden.get('descuento'):,.2f}")
        print(f"Subtotal Neto:          ${orden.get('subtotal_neto'):,.2f}")
        print(f"IVA (19%):              ${orden.get('iva'):,.2f}")
        print(f"Costo Logístico:        ${orden.get('envio'):,.2f}")
        print("=" * 65)
        print(f"TOTAL A PAGAR:          ${orden.get('total_factura'):,.2f}")
        print("=" * 65)

    print("\n" + "#" * 65)
    print(f"💰 RECAUDO TOTAL DE LA JORNADA ({len(historial_transacciones)} órdenes): ${recaudo_total:,.2f}")
    print("#" * 65)

    # Estado de auditoría final (se imprime una sola vez)
    print("\n--- ESTADO FINAL DE AUDITORÍA EN MEMORIA ---")
    print(f"• Catálogo actualizado:        {catalogo}")
    print(f"• SKUs disponibles para venta: {productos_disponibles}")
    print(f"• Alertas de reabastecimiento: {alertas_reabastecimiento}\n")
else:
    print("\nNo se registraron transacciones durante esta sesión.\n")