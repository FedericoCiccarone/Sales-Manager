
import customtkinter as ctk

from config.clientes import guardar_cliente, editar_cliente


class VentanaCliente(ctk.CTkToplevel):

    def __init__(self,parent,callback,nombre=None,datos=None):

        super().__init__(parent)

        self.callback=callback
        self.nombre_original=nombre

        self.title("Cliente Nubceo")
        self.geometry("450x500")

        self.transient(parent)
        self.grab_set()

        self.campos={}

        valores={
            "Nombre": nombre or "",
            "API KEY": (datos or {}).get("apiKey",""),
            "API SECRET": (datos or {}).get("apiSecret",""),
            "Tenant ID": (datos or {}).get("tenantId",""),
            "Company ID": (datos or {}).get("companyId","")
        }

        for campo,valor in valores.items():

            ctk.CTkLabel(self,text=campo).pack(pady=5)

            e=ctk.CTkEntry(self,width=300)
            e.insert(0,valor)
            e.pack()

            self.campos[campo]=e


        ctk.CTkButton(
            self,
            text="Guardar",
            command=self.guardar
        ).pack(pady=25)


    def guardar(self):

        datos=[
            self.campos["Nombre"].get(),
            self.campos["API KEY"].get(),
            self.campos["API SECRET"].get(),
            self.campos["Tenant ID"].get(),
            self.campos["Company ID"].get()
        ]

        if self.nombre_original:
            editar_cliente(self.nombre_original,*datos)
        else:
            guardar_cliente(*datos)

        self.callback()
        self.destroy()
