import customtkinter as ctk

from config.clientes import obtener_clientes, obtener_cliente
from ui.app import iniciar_app
from ui.cliente_manager import VentanaCliente


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginClientes(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Nubceo Sales Manager"
        )

        self.geometry(
            "600x400"
        )

        self.crear_ui()


    def crear_ui(self):

        ctk.CTkLabel(
            self,
            text="◉ Nubceo Sales Manager",
            font=("Arial", 28)
        ).pack(
            pady=30
        )


        clientes = list(
            obtener_clientes().keys()
        )


        self.combo_cliente = ctk.CTkComboBox(
            self,
            width=350,
            values=clientes
        )

        self.combo_cliente.pack(
            pady=10
        )


        if clientes:

            self.combo_cliente.set(
                clientes[0]
            )


        ctk.CTkButton(
            self,
            text="Ingresar",
            width=200,
            command=self.ingresar
        ).pack(
            pady=15
        )


        ctk.CTkButton(
            self,
            text="+ Nuevo Cliente",
            width=200,
            command=lambda:
                VentanaCliente(
                    self,
                    self.actualizar_clientes
                )
        ).pack(
            pady=5
        )


        ctk.CTkButton(
            self,
            text="✏ Editar Cliente",
            width=200,
            command=self.editar_cliente
        ).pack(
            pady=5
        )


    def actualizar_clientes(self):

        clientes = list(
            obtener_clientes().keys()
        )


        self.combo_cliente.configure(
            values=clientes
        )


        if clientes:

            self.combo_cliente.set(
                clientes[0]
            )


    def editar_cliente(self):

        nombre = self.combo_cliente.get()


        cliente = obtener_cliente(
            nombre
        )


        if cliente is None:

            return


        VentanaCliente(
            self,
            self.actualizar_clientes,
            nombre,
            cliente
        )


    def ingresar(self):

        nombre = self.combo_cliente.get()


        cliente = obtener_cliente(
            nombre
        )


        if cliente is None:

            return


        cliente["nombre"] = nombre


        self.destroy()


        iniciar_app(
            cliente
        )



def iniciar_login():

    app = LoginClientes()

    app.mainloop()