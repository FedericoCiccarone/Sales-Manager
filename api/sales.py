import requests

from datetime import datetime


BASE_URL = "https://connectapi.nubceo.com/v1"



def buscar_ventas(
        token,
        tenant_id,
        fecha_desde=None,
        fecha_hasta=None,
        id_venta=None,
        pagina=1,
        cantidad=100
):


    url = (
        f"{BASE_URL}/tenants/"
        f"{tenant_id}/reconciler/sales"
    )


    headers = {

        "Authorization":
            f"Bearer {token}",

        "Content-Type":
            "application/json"
    }



    params = {

        "page":
            pagina,

        "pageSize":
            cantidad
    }



    if fecha_desde and fecha_hasta:


        params[
            "filter[date][between]"
        ] = (
            f"{fecha_desde},{fecha_hasta}"
        )



    if id_venta:


        params[
            "filter[externalCode][eq]"
        ] = id_venta



    response = requests.get(
        url,
        headers=headers,
        params=params
    )



    if response.status_code == 401:

        raise Exception(
            "TOKEN_EXPIRED"
        )



    if response.status_code != 200:

        raise Exception(
            response.text
        )



    return response.json()





def formatear_fecha(
        fecha_api
):


    if not fecha_api:

        return ""


    try:

        return (

            datetime
            .fromisoformat(
                fecha_api.replace(
                    "Z",
                    "+00:00"
                )
            )
            .strftime(
                "%d/%m/%Y"
            )

        )


    except:


        return fecha_api





def formatear_monto(
        valor
):


    if valor is None:

        return "$ 0.00"


    return f"$ {valor:,.2f}"





def preparar_tabla(
        ventas
):

    filas = []

    for venta in ventas:

        pagos = venta.get("relatedPayments", [])
        pago = pagos[0] if pagos else {}

        filas.append({
            "seleccion": False,

            "id": venta.get("id"),
            "fecha": formatear_fecha(venta.get("date")),
            "monto": formatear_monto(venta.get("grossAmount")),
            "neto": formatear_monto(venta.get("netAmount")),
            "impuesto": formatear_monto(venta.get("taxAmount")),
            "moneda": venta.get("currencyCode"),
            "estado": venta.get("reconciliationStatus"),
            "tipoDocumento": venta.get("documentType"),
            "referenciaInterna": venta.get("internalReference"),
            "sucursal": venta.get("customerBranchReference"),
            "categoria1": venta.get("saleCategory1"),
            "categoria2": venta.get("saleCategory2"),
            "categoria3": venta.get("saleCategory3"),
            "cantidadPagos": len(pagos),

            "procesadora": pago.get("platformExternalCode"),
            "fechaPresentacion": formatear_fecha(pago.get("presentedDate")),
            "lote": pago.get("batch"),
            "voucher": pago.get("voucher"),
            "terminal": pago.get("terminal"),
            "autorizacion": pago.get("authorizationCode"),
            "sucursalPlataforma": pago.get("platformBranchReference"),
            "montoPago": formatear_monto(pago.get("grossAmount")),
            "marcaTarjeta": pago.get("cardBrand"),
            "numeroTarjeta": pago.get("cardNumber"),
            "comprador": pago.get("buyerIdentification"),
            "cuotas": pago.get("installments"),
            "promocion": pago.get("promotionCode"),
            "tipoPago": pago.get("paymentType"),
            "referenciaExterna": pago.get("externalReference"),
            "idPago": pago.get("id"),
            "estadoPago": pago.get("reconciliationStatus"),
            "wildcard": pago.get("wildCard"),
            "wildcard2": pago.get("wildCardTwo"),
            "monedaPago": pago.get("currencyCode"),
            "cotizacion": pago.get("exchangeRate"),
            "montoConvertido": formatear_monto(pago.get("convertedAmount")),
            "companyId": pago.get("companyId"),
            "headerBranchId": pago.get("headerBranchId")
        })

    return filas

def eliminar_ventas(
        token,
        tenant_id,
        company_id,
        ids
):


    url = (

        f"{BASE_URL}/tenants/"
        f"{tenant_id}/"
        f"{company_id}/"
        "reconciler/sales/delete"

    )


    headers = {

        "Authorization":
            f"Bearer {token}",

        "Content-Type":
            "application/json"

    }



    body = {

        "ids":
            ids

    }



    response = requests.post(

        url,

        headers=headers,

        json=body

    )



    if response.status_code == 401:

        raise Exception(
            "TOKEN_EXPIRED"
        )



    if response.status_code not in [
        200,
        201
    ]:

        raise Exception(
            response.text
        )



    return response.json()