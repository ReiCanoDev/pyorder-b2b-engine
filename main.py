# ==============================================================================
# PROYECTO: PyOrder B2B Engine - Sistema de Validación y Liquidación de Órdenes
# VERSIÓN: 1.0.0 (Single-Transaction CLI)
# ==============================================================================

# 1. DATOS COMPUESTOS (Base de datos en memoria)
# Tupla inmutable: (IVA_GENERAL, COSTO_ENVIO_BASE, TOPE_ENVIO_GRATIS)
CONFIG_FINANCIERA = (0.19, 25.00, 1000.00)

# Diccionario anidado: Catálogo de inventario
catalogo = {
    "LAP-01": {"nombre": "Laptop Pro 16", "precio": 1200.00, "stock": 5},
    "MON-02": {"nombre": "Monitor 4K 27", "precio": 350.00, "stock": 12},
    "SSD-03": {"nombre": "Disco Solido 1TB", "precio": 95.00, "stock": 3}
}

# Diccionario de cupones activos (Código: porcentaje de descuento)
cupones_activos = {
    "B2BWELCOME": 0.10,
    "VIPTECH": 0.15
}

# Listas de operación y auditoría
ciudades_cobertura = ["Bogota", "Medellin", "Cali", "Barranquilla", "Sincelejo"]
productos_disponibles = ["LAP-01", "MON-02", "SSD-03"]
alertas_reabastecimiento = []
historial_transacciones = []

print("=" * 65)
print("📦 SISTEMA CORPORATIVO DE PROCESAMIENTO DE ÓRDENES B2B v1.0")
print(f"SKUs activos en catálogo: {list(catalogo.keys())}")
print("=" * 65)

# ==============================================================================
cliente = input("\nIngrese el nombre completo del cliente: ").strip().title()
id_cliente = (
    input("Ingrese el NIT/ID del cliente: ")
    .strip()
    .replace("-", "")
    .replace(".", "")
    .replace(",", "")
    .replace(" ", "")
)
sku = input("Ingrese el SKU del producto: ").strip().upper()
cantidad_str = input("Ingrese la cantidad a comprar: ").strip()
ciudad = input("Ingrese la ciudad de entrega: ").strip().title()
cupon = input("Ingrese el cupón de descuento (Enter si no aplica): ").strip().upper()

# ==============================================================================
print("\n--- VALIDACIÓN DE DATOS DE ENTRADA ---")

if not cliente:
    print("❌ Error Crítico: El nombre del cliente no puede estar vacío.")
elif not id_cliente.isdigit():
    print("❌ Error Crítico: El ID del cliente debe contener solo números.")
elif not cantidad_str.isdigit():
    print("❌ Error Crítico: La cantidad debe ser un número entero positivo.")
elif sku not in catalogo:
    print(f"❌ Error de Catálogo: El SKU '{sku}' no existe. Activos: {list(catalogo.keys())}")
elif ciudad not in ciudades_cobertura:
    print(f"❌ Error Logístico: Sin cobertura en '{ciudad}'. Ciudades válidas: {ciudades_cobertura}")
else:
    # Si pasa todas las validaciones de formato y pertenencia, extraemos el producto y convertimos cantidad
    cantidad = int(cantidad_str)
    producto = catalogo.get(sku)
    stock_actual = producto.get("stock")
    precio_unitario = producto.get("precio")
    nombre_producto = producto.get("nombre")

    # Validación de regla de stock (Mayor a 0 y menor o igual al stock disponible)
    if cantidad <= 0 or cantidad > stock_actual:
        print(
            f"❌ Error de Inventario: Cantidad inválida ({cantidad}). "
            f"Debe pedir entre 1 y {stock_actual} unidades disponibles de {sku}."
        )
    else:
        print(f"✅ Orden validada exitosamente para '{nombre_producto}' ({sku}).")

        # ======================================================================
        subtotal = precio_unitario * cantidad

        
        if cupon in cupones_activos:
            porcentaje_descuento = cupones_activos.get(cupon)
            motivo_descuento = f"Cupón {cupon} ({porcentaje_descuento * 100:.0f}%)"
        elif cantidad >= 5:
            porcentaje_descuento = 0.05
            motivo_descuento = "Descuento Mayorista Automático (5%)"
        else:
            porcentaje_descuento = 0.0
            motivo_descuento = "Sin descuento (0%)"

        monto_descuento = subtotal * porcentaje_descuento
        subtotal_con_descuento = subtotal - monto_descuento
        iva = subtotal_con_descuento * CONFIG_FINANCIERA[0]

        # Regla de envío (Tope financiero o cupón VIPTECH)
        if subtotal_con_descuento >= CONFIG_FINANCIERA[2] or cupon == "VIPTECH":
            costo_envio = 0.00
        else:
            costo_envio = CONFIG_FINANCIERA[1]

        total_factura = subtotal_con_descuento + iva + costo_envio

        # ======================================================================
        nuevo_stock = stock_actual - cantidad
        producto.update({"stock": nuevo_stock})

        if nuevo_stock == 0:
            productos_disponibles.remove(sku)
            alertas_reabastecimiento.append(sku)
            print(f"⚠️ Alerta de Stock: '{sku}' agotado. Movido a alertas de reabastecimiento.")

        registro_orden = {
            "cliente": cliente,
            "id_cliente": id_cliente,
            "ciudad": ciudad,
            "sku": sku,
            "producto": nombre_producto,
            "cantidad": cantidad,
            "subtotal": subtotal,
            "descuento": monto_descuento,
            "subtotal_neto": subtotal_con_descuento,
            "iva": iva,
            "envio": costo_envio,
            "total_factura": total_factura
        }
        historial_transacciones.append(registro_orden)

        # ======================================================================
        print("\n" + "=" * 65)
        print("🧾 FACTURA DE VENTA CORPORATIVA - PYORDER B2B")
        print("=" * 65)
        print(f"Cliente:                {cliente} (ID: {id_cliente})")
        print(f"Ciudad de Destino:      {ciudad}")
        print(f"Producto:               {nombre_producto} [{sku}]")
        print(f"Cantidad:               {cantidad} unidades x ${precio_unitario:,.2f}")
        print("-" * 65)
        print(f"Subtotal Bruto:         ${subtotal:,.2f}")
        print(f"Beneficio Aplicado:     {motivo_descuento}")
        print(f"Descuento:             -${monto_descuento:,.2f}")
        print(f"Subtotal Neto:          ${subtotal_con_descuento:,.2f}")
        print(f"IVA (19%):              ${iva:,.2f}")
        print(f"Costo Logístico:        ${costo_envio:,.2f}")
        print("=" * 65)
        print(f"TOTAL A PAGAR:          ${total_factura:,.2f}")
        print("=" * 65)

        print("\n--- ESTADO DE AUDITORÍA EN MEMORIA ---")
        print(f"• Stock restante de {sku}:      {producto.get('stock')} unidades")
        print(f"• SKUs disponibles para venta:  {productos_disponibles}")
        print(f"• Alertas de reabastecimiento:  {alertas_reabastecimiento}")
        print(f"• Transacciones registradas:    {len(historial_transacciones)}")
        print(f"• Detalle de auditoría:         {historial_transacciones}\n")