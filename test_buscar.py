from api.auth import obtener_token
from api.sales import buscar_ventas, preparar_tabla
from config.clientes import obtener_cliente


cliente = obtener_cliente(
    "Cliente Test"
)


token = obtener_token(
    cliente["apiKey"],
    cliente["apiSecret"]
)


respuesta = buscar_ventas(
    token,
    cliente["tenantId"],
    "2020-01-01",
    "2026-12-31",
    cantidad=100
)


ventas = preparar_tabla(
    respuesta["data"]
)


contador = 0


for venta in ventas:


    if venta["estado"] != "reconciled":


        contador += 1


        print(
            venta
        )


print(
    "\nVentas posibles:",
    contador
)