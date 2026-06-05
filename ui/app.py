
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

from api.auth import obtener_token
from api.sales import buscar_ventas, preparar_tabla, eliminar_ventas
from config.clientes import obtener_clientes, obtener_cliente
from ui.cliente_manager import VentanaCliente


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


COLUMNAS = {
    "id": "ID Venta",
    "fecha": "Fecha",
    "monto": "Monto Bruto",
    "neto": "Monto Neto",
    "impuesto": "Impuesto",
    "moneda": "Moneda",
    "estado": "Estado",
    "tipoDocumento": "Documento",
    "referenciaInterna": "Referencia",
    "sucursal": "Sucursal",
    "categoria1": "Categoria 1",
    "categoria2": "Categoria 2",
    "categoria3": "Categoria 3",
    "cantidadPagos": "Pagos",
    "procesadora": "Procesadora",
    "fechaPresentacion": "Fecha Presentacion",
    "lote": "Lote",
    "voucher": "Voucher",
    "terminal": "Terminal",
    "autorizacion": "Autorizacion",
    "sucursalPlataforma": "Sucursal Plataforma",
    "montoPago": "Monto Pago",
    "marcaTarjeta": "Marca Tarjeta",
    "numeroTarjeta": "Numero Tarjeta",
    "comprador": "Comprador",
    "cuotas": "Cuotas",
    "promocion": "Promocion",
    "tipoPago": "Tipo Pago",
    "referenciaExterna": "Referencia Externa",
    "idPago": "ID Pago",
    "estadoPago": "Estado Pago",
    "wildcard": "Wildcard",
    "wildcard2": "Wildcard 2",
    "monedaPago": "Moneda Pago",
    "cotizacion": "Cotizacion",
    "montoConvertido": "Monto Convertido",
    "headerBranchId": "Header Branch ID",
    "companyId": "Company ID"
}


class NubceoApp(ctk.CTk):

    def __init__(self, cliente_actual=None):

        super().__init__()

        self.cliente_actual = cliente_actual

        self.title("Nubceo Sales Manager")
        self.geometry("1600x900")

        self.ventas_actuales = []
        self.ventas_filtradas = []
        self.checks_ventas = {}

        self.columnas_visibles = [
            "id",
            "fecha",
            "monto",
            "neto",
            "impuesto",
            "estado"
        ]

        self.crear_ui()


    def crear_ui(self):

        ctk.CTkLabel(
            self,
            text="◉ Nubceo Sales Manager",
            font=("Arial",30)
        ).pack(pady=10)


        if self.cliente_actual:

            ctk.CTkLabel(
                self,
                text=f"Cliente activo: {self.cliente_actual.get('nombre','')}",
                font=("Arial",16)
            ).pack(pady=5)


        frame_fechas = ctk.CTkFrame(self)
        frame_fechas.pack(pady=10)


        self.fecha_desde = DateEntry(
            frame_fechas,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )

        self.fecha_desde.pack(
            side="left",
            padx=10
        )


        self.fecha_hasta = DateEntry(
            frame_fechas,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )

        self.fecha_hasta.pack(
            side="left",
            padx=10
        )


        botones_busqueda = ctk.CTkFrame(self)
        botones_busqueda.pack(pady=5)


        ctk.CTkButton(
            botones_busqueda,
            text="🔍 Buscar ventas",
            command=self.buscar
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            botones_busqueda,
            text="⚙ Columnas",
            command=self.abrir_columnas
        ).pack(side="left", padx=5)


        filtros = ctk.CTkFrame(self)
        filtros.pack(pady=10)


        self.combo_columna_busqueda = ctk.CTkComboBox(
            filtros,
            values=list(COLUMNAS.values()),
            width=220
        )

        self.combo_columna_busqueda.set("ID Venta")

        self.combo_columna_busqueda.grid(
            row=0,
            column=0,
            padx=5
        )


        self.valor_busqueda = ctk.CTkEntry(
            filtros,
            placeholder_text="Ingrese valor a buscar",
            width=260
        )

        self.valor_busqueda.grid(
            row=0,
            column=1,
            padx=5
        )


        ctk.CTkButton(
            filtros,
            text="Aplicar filtro",
            command=self.aplicar_filtros
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        self.filtro_columna = ctk.CTkComboBox(
            filtros,
            values=list(COLUMNAS.values()),
            width=220
        )

        self.filtro_columna.set("ID Venta")

        self.filtro_columna.grid(
            row=0,
            column=0,
            padx=5
        )


        self.buscar_texto = ctk.CTkEntry(
            filtros,
            placeholder_text="Valor a buscar...",
            width=260
        )

        self.buscar_texto.grid(
            row=0,
            column=1,
            padx=5
        )


        self.buscar_texto.bind(
            "<KeyRelease>",
            lambda e:self.aplicar_filtros()
        )


        self.filtro_estado = ctk.CTkComboBox(
            filtros,
            values=[
                "Todos",
                "Conciliadas",
                "Disponibles",
                "Tried"
            ],
            command=lambda e:self.aplicar_filtros()
        )

        self.filtro_estado.set("Todos")

        self.filtro_estado.grid(
            row=0,
            column=2,
            padx=5
        )


        self.filtro_monto_desde = ctk.CTkEntry(
            filtros,
            placeholder_text="Monto desde"
        )

        self.filtro_monto_desde.grid(
            row=0,
            column=3,
            padx=5
        )


        self.filtro_monto_hasta = ctk.CTkEntry(
            filtros,
            placeholder_text="Monto hasta"
        )

        self.filtro_monto_hasta.grid(
            row=0,
            column=4,
            padx=5
        )


        for entrada in [
            self.filtro_monto_desde,
            self.filtro_monto_hasta
        ]:

            entrada.bind(
                "<KeyRelease>",
                lambda e:self.aplicar_filtros()
            )


        self.lbl_total = ctk.CTkLabel(
            self,
            text="Ventas encontradas: 0"
        )

        self.lbl_total.pack()


        acciones = ctk.CTkFrame(self)
        acciones.pack(pady=5)


        ctk.CTkButton(
            acciones,
            text="Seleccionar eliminables",
            command=self.seleccionar_todas
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            acciones,
            text="Limpiar selección",
            command=self.limpiar
        ).pack(side="left", padx=5)


        ctk.CTkButton(
            acciones,
            text="🗑 Eliminar",
            fg_color="darkred",
            command=self.confirmar_eliminar
        ).pack(side="left", padx=5)


        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            show="headings",
            selectmode="extended"
        )

        scroll_y = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        scroll_x = ttk.Scrollbar(
            frame_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self.ids_tree = {}

        self.ventas_seleccionadas = set()

        self.tabla.bind(
            "<ButtonRelease-1>",
            self.toggle_seleccion
        )


    def buscar(self):

        if self.cliente_actual:
            cliente = self.cliente_actual
        else:
            cliente = obtener_cliente(
                self.combo_cliente.get()
            )

        token = obtener_token(
            cliente["apiKey"],
            cliente["apiSecret"]
        )


        datos = buscar_ventas(
            token,
            cliente["tenantId"],
            self.fecha_desde.get(),
            self.fecha_hasta.get()
        )


        self.ventas_actuales = preparar_tabla(
            datos["data"]
        )


        self.aplicar_filtros()


    def aplicar_filtros(self):

        texto = self.buscar_texto.get().lower()

        estado = self.filtro_estado.get()


        resultado=[]


        for venta in self.ventas_actuales:

            if hasattr(self, "valor_busqueda"):

                valor_filtro = self.valor_busqueda.get().lower().strip()

                if valor_filtro:

                    columna = self.combo_columna_busqueda.get()

                    campo = None

                    for key, nombre in COLUMNAS.items():

                        if nombre == columna:

                            campo = key
                            break


                    if campo:

                        dato = str(
                            venta.get(
                                campo,
                                ""
                            )
                        ).lower()

                        if valor_filtro not in dato:

                            continue


            if texto:

                columna_nombre = self.filtro_columna.get()

                campo_real = None

                for key, value in COLUMNAS.items():
                    if value == columna_nombre:
                        campo_real = key
                        break


                if campo_real:

                    valor_campo = str(
                        venta.get(
                            campo_real,
                            ""
                        )
                    ).lower()

                    if texto not in valor_campo:
                        continue


            if estado=="Conciliadas" and venta["estado"]!="reconciled":
                continue


            if estado=="Disponibles" and venta["estado"]!="notReconciled":
                continue


            if estado=="Tried" and venta["estado"]!="tried":
                continue


            resultado.append(venta)


        self.ventas_filtradas=resultado


        self.lbl_total.configure(
            text=f"Ventas encontradas: {len(resultado)}"
        )


        self.dibujar_tabla()


    def dibujar_tabla(self):

        self.tabla.delete(
            *self.tabla.get_children()
        )

        self.ids_tree = {}

        columnas = ["seleccion"] + self.columnas_visibles

        self.tabla["columns"] = columnas


        for campo in columnas:

            titulo = "Sel" if campo == "seleccion" else COLUMNAS.get(campo, campo)

            self.tabla.heading(
                campo,
                text=titulo
            )

            self.tabla.column(
                campo,
                width=70 if campo == "seleccion" else 160,
                stretch=False,
                anchor="center"
            )


        for index, venta in enumerate(self.ventas_filtradas):

            valores = []

            for campo in columnas:

                if campo == "seleccion":

                    if venta.get("estado") == "reconciled":

                        valores.append("🔒")

                    elif venta.get("id") in self.ventas_seleccionadas:

                        valores.append("☑")

                    else:

                        valores.append("☐")

                    continue


                valor = venta.get(campo, "")


                if campo == "estado":

                    if valor == "reconciled":

                        valor = "🔴 Conciliada"

                    elif valor == "tried":

                        valor = "🟡 Tried"

                    else:

                        valor = "🟢 Disponible"


                valores.append(valor)


            self.tabla.insert(
                "",
                "end",
                iid=str(index),
                values=valores
            )


            self.ids_tree[str(index)] = venta



    def toggle_seleccion(self, event=None):

        item = self.tabla.focus()


        if not item:

            return


        venta = self.ids_tree.get(item)


        if not venta:

            return


        if venta.get("estado") == "reconciled":

            return


        venta_id = venta.get("id")


        if venta_id in self.ventas_seleccionadas:

            self.ventas_seleccionadas.remove(
                venta_id
            )

        else:

            self.ventas_seleccionadas.add(
                venta_id
            )


        self.dibujar_tabla()



    def seleccionar_todas(self):

        self.ventas_seleccionadas = {

            venta.get("id")

            for venta in self.ventas_filtradas

            if venta.get("estado") != "reconciled"

        }


        self.dibujar_tabla()



    def limpiar(self):

        self.ventas_seleccionadas.clear()

        self.dibujar_tabla()



    def confirmar_eliminar(self):

        ventas = [

            venta

            for venta in self.ventas_filtradas

            if venta.get("id") in self.ventas_seleccionadas
            and venta.get("estado") != "reconciled"

        ]


        if not ventas:

            messagebox.showwarning(
                "Sin seleccion",
                "No hay ventas seleccionadas para eliminar"
            )

            return


        cliente = self.cliente_actual


        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Cliente: {cliente.get('nombre','')}\n\n"
            f"Ventas a eliminar: {len(ventas)}\n\n"
            "Esta accion no se puede deshacer.\n\n"
            "Desea continuar?"
        )


        if not confirmar:

            return


        token = obtener_token(
            cliente["apiKey"],
            cliente["apiSecret"]
        )


        resultado = eliminar_ventas(
            token,
            cliente["tenantId"],
            cliente["companyId"],
            [x["id"] for x in ventas]
        )


        messagebox.showinfo(
            "Resultado eliminacion",
            str(resultado)
        )


        self.ventas_seleccionadas.clear()

        self.buscar()





    def abrir_columnas(self):

        ventana = ctk.CTkToplevel(self)
        ventana.title("Columnas visibles")
        ventana.geometry("420x650")
        ventana.transient(self)
        ventana.grab_set()
        ventana.focus_force()

        checks = {}

        frame_scroll = ctk.CTkScrollableFrame(
            ventana,
            width=360,
            height=480
        )

        frame_scroll.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        for campo, nombre in COLUMNAS.items():

            var = ctk.BooleanVar(
                value=campo in self.columnas_visibles
            )

            ctk.CTkCheckBox(
                frame_scroll,
                text=nombre,
                variable=var
            ).pack(
                anchor="w",
                padx=20,
                pady=5
            )

            checks[campo] = var


        frame_botones = ctk.CTkFrame(ventana)

        frame_botones.pack(pady=10)


        def seleccionar_todo():

            for var in checks.values():

                var.set(True)


        def limpiar_todo():

            for var in checks.values():

                var.set(False)


        def aplicar():

            self.columnas_visibles = [

                campo
                for campo, var
                in checks.items()
                if var.get()

            ]

            ventana.destroy()

            self.dibujar_tabla()


        ctk.CTkButton(
            frame_botones,
            text="Seleccionar todo",
            command=seleccionar_todo
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            command=limpiar_todo
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            ventana,
            text="✅ Aplicar columnas",
            command=aplicar
        ).pack(
            pady=10
        )



    def actualizar_clientes(self):

        self.combo_cliente.configure(
            values=list(obtener_clientes().keys())
        )


def iniciar_app(cliente_actual=None):

    app=NubceoApp(cliente_actual)
    app.mainloop()
