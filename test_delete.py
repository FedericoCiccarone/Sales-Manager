from api.auth import obtener_token

from api.sales import eliminar_ventas

from config.clientes import obtener_cliente



cliente = obtener_cliente(
    "Cliente Test"
)



token = obtener_token(
    cliente["apiKey"],
    cliente["apiSecret"]
)



respuesta = eliminar_ventas(
    token,
    cliente["tenantId"],
    cliente["companyId"],
    [
        "21251"
    ]
)



print(
    respuesta
)