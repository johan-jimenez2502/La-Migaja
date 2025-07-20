import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox 
from pago_efectivo import abrir_ventana_pago_efectivo

def ventana_caja(restaurante, return_callback):
    ventana = tk.Toplevel() 
    ventana.title("Caja - Punto de Venta")
    ventana.geometry("900x700")
    ventana.configure(bg="#f1ddbf")

    # Logo de La Migaja
    logo_img = Image.open("Logo_migaja.jpg")
    logo_img = logo_img.resize((130, 130))
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(ventana, image=logo_img, bg="#f1ddbf")
    logo_label.image = logo_img
    logo_label.pack(pady=(10, 0))

    # Título
    tk.Label(ventana, text="Caja - Registro de Pago", font=("Helvetica Neue", 22, "bold"),
             bg="#f1d28f", fg="#8B2F23").pack(pady=5)

    # Frame principal
    frame_principal = tk.Frame(ventana, bg="#f1d28f")
    frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

    # Lista de pedidos
    frame_izq = tk.Frame(frame_principal, bg="#f1d28f")
    frame_izq.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_izq, text="Pedidos Servidos", font=("Helvetica Neue", 14, "bold"),
             bg="#f1d28f", fg="#3e3324").pack(anchor="w", pady=5)

    lista_pedidos = tk.Listbox(frame_izq, font=("Courier New", 10),
                               width=50, height=20, bd=2, relief="solid",
                               bg="#fff9f0", fg="#000000")
    lista_pedidos.pack(fill="both", expand=True, padx=5)

    # Separador visual
    tk.Frame(frame_principal, width=2, bg="#8B2F23").pack(side="left", fill="y", padx=5)

    # Panel derecho
    frame_der = tk.Frame(frame_principal, bg="#f1d28f")
    frame_der.pack(side="right", fill="y", padx=10, pady=10)

    tk.Label(frame_der, text="Detalles de Pago", font=("Helvetica Neue", 14, "bold"),
             bg="#f1d28f", fg="#8B2F23").pack(pady=(10, 5))

    label_total = tk.Label(frame_der, text="Total: $0.00", font=("Helvetica Neue", 12),
                           bg="#f1d28f", fg="#000000")
    label_total.pack(pady=5)

    label_cambio = tk.Label(frame_der, text="Cambio: $0.00", font=("Helvetica Neue", 12, "bold"),
                            bg="#f1d28f", fg="#40754C")
    label_cambio.pack(pady=10)

    # Selector método de pago
    metodo = tk.StringVar(value="")

    def seleccionar_metodo(valor):
        metodo.set(valor)
        btn_efectivo.config(relief="raised")
        btn_tarjeta.config(relief="raised")
        if valor == "efectivo":
            btn_efectivo.config(relief="sunken")
        else:
            btn_tarjeta.config(relief="sunken")

    selector_pago = tk.Frame(frame_der, bg="#f1d28f")
    selector_pago.pack(pady=10)

    btn_efectivo = tk.Button(selector_pago, text="💵 Efectivo", bg="#40754C", fg="white",
                             font=("Helvetica Neue", 12, "bold"), width=12, relief="raised",
                             command=lambda: seleccionar_metodo("efectivo"))
    btn_efectivo.grid(row=0, column=0, padx=5, pady=5)

    btn_tarjeta = tk.Button(selector_pago, text="💳 Tarjeta", bg="#8B2F23", fg="white",
                            font=("Helvetica Neue", 12, "bold"), width=12, relief="raised",
                            command=lambda: seleccionar_metodo("tarjeta"))
    btn_tarjeta.grid(row=0, column=1, padx=5, pady=5)

    # Botón pagar
    def procesar_pago():
        idx = lista_pedidos.curselection()
        if not idx:
            messagebox.showwarning("Selecciona un pedido", "Primero selecciona un pedido.")
            return
        if metodo.get() == "":
            messagebox.showwarning("Método de pago", "Por favor, selecciona un método de pago.")
            return

        pedido = pedidos[idx[0]]
        pedido_id = pedido["id"]
        total = pedido.get("total", 0)

        if metodo.get() == "efectivo":
            abrir_ventana_pago_efectivo(total)
        else:
            tarjeta_ventana = tk.Toplevel(ventana)
            tarjeta_ventana.title("Pago con Tarjeta")
            tarjeta_ventana.geometry("350x220")
            tarjeta_ventana.configure(bg="#fff9f0")

            tk.Label(tarjeta_ventana, text="💳 Pago con Tarjeta", font=("Helvetica Neue", 14, "bold"),
                     bg="#fff9f0", fg="#1a1a1a").pack(pady=10)

            campos = {
                "Número de tarjeta": "•••• •••• •••• 1234",
                "Expiración": "08/27",
                "CVC": "***"
            }

            for etiqueta, valor in campos.items():
                tk.Label(tarjeta_ventana, text=etiqueta, bg="#fff9f0", font=("Helvetica Neue", 10, "bold")).pack(anchor="w", padx=20)
                entrada = tk.Entry(tarjeta_ventana, font=("Helvetica Neue", 10), state="disabled", disabledforeground="black")
                entrada.insert(0, valor)
                entrada.pack(padx=20, pady=2, fill="x")

            def finalizar_pago():
                try:
                    restaurante.marcar_pedido_pagado(pedido_id)
                    tarjeta_ventana.destroy()
                    ventana.destroy()
                    ventana_caja(restaurante, return_callback)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo marcar como pagado: {str(e)}")

            tk.Button(tarjeta_ventana, text="Finalizar", command=finalizar_pago,
                      bg="#4caf50", fg="white", font=("Helvetica Neue", 11, "bold"), width=20).pack(pady=10)

    pagar_btn = tk.Button(frame_der, text="✅ Pagar Ahora", command=procesar_pago,
                          bg="#F39C12", fg="white", font=("Helvetica Neue", 13, "bold"),
                          width=25, relief="raised")
    pagar_btn.pack(pady=20)

    # Botón volver
    tk.Button(frame_der,
          text="⬅️ Volver al menú anterior",
          command=lambda: [ventana.destroy(), return_callback()],
          bg="#8B2F23",
          fg="white",
          font=("Helvetica Neue", 12, "bold"),
          width=25,
          relief="raised").pack(pady=10)


    # Obtener pedidos
    pedidos = restaurante.obtener_pedidos_servidos_no_pagados() if restaurante else []

    if not pedidos:
        lista_pedidos.insert(tk.END, "No hay pedidos pendientes de pago.")
    else:
        for pedido in pedidos:
            numero = pedido.get("numero_pedido", "???")
            mesa = pedido.get("mesa", "???")
            total = pedido.get("total", 0)
            hora = pedido.get("hora", "???")
            lista_pedidos.insert(tk.END, f"#{numero} | Mesa {mesa} | ${total:.2f} | {hora}")

    def on_seleccion(event):
        idx = lista_pedidos.curselection()
        if not idx:
            return
        pedido = pedidos[idx[0]]
        total = pedido.get("total", 0)
        label_total.config(text=f"Total: ${total:.2f}")
        label_cambio.config(text="Cambio: $0.00")

    lista_pedidos.bind("<<ListboxSelect>>", on_seleccion)

