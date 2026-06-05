
import json
from pathlib import Path

ARCHIVO = Path("clientes.json")


def obtener_clientes():

    if not ARCHIVO.exists():
        return {}

    with open(ARCHIVO,"r",encoding="utf-8") as f:
        return json.load(f)


def obtener_cliente(nombre):

    return obtener_clientes().get(nombre)


def guardar_cliente(nombre,api_key,api_secret,tenant_id,company_id):

    clientes=obtener_clientes()

    clientes[nombre]={
        "tenantId":tenant_id,
        "companyId":company_id,
        "apiKey":api_key,
        "apiSecret":api_secret
    }

    with open(ARCHIVO,"w",encoding="utf-8") as f:
        json.dump(clientes,f,indent=4)


def editar_cliente(nombre_original,nombre,api_key,api_secret,tenant_id,company_id):

    clientes=obtener_clientes()

    if nombre_original in clientes and nombre_original != nombre:
        del clientes[nombre_original]

    clientes[nombre]={
        "tenantId":tenant_id,
        "companyId":company_id,
        "apiKey":api_key,
        "apiSecret":api_secret
    }

    with open(ARCHIVO,"w",encoding="utf-8") as f:
        json.dump(clientes,f,indent=4)
