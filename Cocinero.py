import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Clases import Restaurante
from Conexion_fb import db
from datetime import datetime

# 🎨 Estilos visuales modernos
FONDO = "#f1ddbf"
COLOR_ENCABEZADO = "#8B2F23"
COLOR_CARD = "#fff9f0"
COLOR_BOTON = "#1fd465"
COLOR_CERRAR = "#6c757d"
COLOR_TEXTO = "#1a1a1a"
FUENTE_TITULO = ("Helvetica", 17, "bold")
FUENTE_NORMAL = ("Helvetica", 11)
FUENTE_PRODUCTOS = ("Helvetica", 10)

def ventana_cocinero(restaurante, nombre_usuario, return_callback):
    ventana = tk.Toplevel()
    ventana.title(f"Cocinero - {nombre_usuario}")
    ventana.geometry("1000x700")
    ventana.configure(bg=FONDO)
    ventana.iconbitmap("Logo_migaja.ico")

    # 🧾 Encabezado
    encabezado = tk.Frame(ventana, bg=FONDO)
    encabezado.pack(fill="x", pady=10)

    tk.Label(encabezado,
             text=f"🍳 Pedidos en cocina - {nombre_usuario}",
             font=FUENTE_TITULO,
             fg=COLOR_ENCABEZADO,
             bg=FONDO).pack(pady=(5, 10))

    separator = tk.Frame(ventana, bg=COLOR_ENCABEZADO, height=2)
    separator.pack(fill="x", padx=20, pady=(0, 10))

    # 🖼️ Contenedor principal dividido 70/30
    contenedor = tk.Frame(ventana, bg=FONDO)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # 🧾 Área de pedidos (70%)
    pedidos_area = tk.Frame(contenedor, bg=FONDO, width=700)
    pedidos_area.pack(side="left", fill="both", expand=True)

    canvas = tk.Canvas(pedidos_area, bg=FONDO, highlightthickness=0)
    scrollbar = ttk.Scrollbar(pedidos_area, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=FONDO)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    pedidos_frame = tk.Frame(scrollable_frame, bg=FONDO)
    pedidos_frame.pack(fill="both")

    # 📷 Área lateral con imagen (30%)
    imagen_frame = tk.Frame(contenedor, bg=FONDO, width=300)
    imagen_frame.pack(side="right", fill="y", padx=20)

    try:
        imagen_logo = Image.open("Logo_migaja.jpg")
        imagen_logo = imagen_logo.resize((260, 260))
        imagen_tk = ImageTk.PhotoImage(imagen_logo)
        tk.Label(imagen_frame, image=imagen_tk, bg=FONDO).pack(pady=30)
        imagen_frame.image = imagen_tk
    except Exception as e:
        tk.Label(imagen_frame, text="Logo no encontrado", bg=FONDO, fg="red").pack()

    def mostrar_pedidos():
        for widget in pedidos_frame.winfo_children():
            widget.destroy()

        pedidos = restaurante.obtener_pedidos_pendientes()
        pedidos.sort(key=lambda x: x.get("numero_pedido", 0))

        if not pedidos:
            tk.Label(pedidos_frame,
                     text="🎉 No hay pedidos pendientes",
                     font=FUENTE_NORMAL,
                     bg=FONDO,
                     fg=COLOR_TEXTO).pack(pady=20)
            return

        for i, pedido in enumerate(pedidos):
            crear_tarjeta_pedido(pedido, True, i)

    def mostrar_pedidos_anteriores():
        for widget in pedidos_frame.winfo_children():
            widget.destroy()

        pedidos = restaurante.obtener_pedidos_servidos()
        pedidos.sort(key=lambda x: x.get("numero_pedido", 0))  # ✅ SOLO ordenar por número

        if not pedidos:
            tk.Label(pedidos_frame,
                     text="📜 No hay pedidos anteriores",
                     font=FUENTE_NORMAL,
                     bg=FONDO,
                     fg=COLOR_TEXTO).pack(pady=20)
            return

        for i, pedido in enumerate(pedidos):
            crear_tarjeta_pedido(pedido, False, i)

    def crear_tarjeta_pedido(pedido, mostrar_boton, index):
        fila = index // 2
        columna = index % 2

        card = tk.Frame(pedidos_frame, bg=COLOR_CARD, bd=1, relief="solid")
        card.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")

        numero = pedido.get("numero_pedido", "???")
        mesa = pedido.get("mesa", "Sin número")

        tk.Label(card,
                 text=f"🧾 Pedido #{numero}  |  Mesa: {mesa}",
                 font=("Helvetica", 13, "bold"),
                 bg=COLOR_CARD,
                 fg=COLOR_TEXTO).pack(anchor="w", pady=(2, 0))

        if 'hora' in pedido:
            tk.Label(card,
                     text=f"🕒 Hora: {pedido['hora']}",
                     font=("Helvetica", 9),
                     bg=COLOR_CARD,
                     fg="#6c757d").pack(anchor="w", pady=(0, 4))

        if not mostrar_boton:
            tk.Label(card,
                     text="✅ Servido",
                     font=("Helvetica", 9, "italic"),
                     bg=COLOR_CARD,
                     fg="#198754").pack(anchor="w", pady=(0, 4))

        productos_frame = tk.Frame(card, bg=COLOR_CARD)
        productos_frame.pack(anchor="w", padx=10)

        for item in pedido.get("items", []):
            tk.Label(productos_frame,
                     text=f"• {item['nombre']}",
                     font=FUENTE_PRODUCTOS,
                     bg=COLOR_CARD,
                     fg=COLOR_TEXTO).pack(anchor="w", pady=1)

        if mostrar_boton:
            tk.Button(card,
                      text="✅ Marcar como Servido",
                      bg=COLOR_BOTON,
                      fg="white",
                      relief="flat",
                      font=FUENTE_NORMAL,
                      command=lambda p=pedido['id']: marcar_servido(p)).pack(anchor="e", pady=10)

    def marcar_servido(pedido_id):
        if messagebox.askyesno("Confirmar", "¿Marcar este pedido como servido?"):
            try:
                restaurante.marcar_pedido_servido(pedido_id)
                messagebox.showinfo("Éxito", "Pedido marcado como servido")
                mostrar_pedidos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

    # 🔘 Controles inferiores
    control_frame = tk.Frame(scrollable_frame, bg=FONDO)
    control_frame.pack(fill="x", pady=(10, 20))

    tk.Button(control_frame,
              text="🔄 Actualizar",
              command=mostrar_pedidos,
              bg=COLOR_ENCABEZADO,
              fg="white",
              font=FUENTE_NORMAL,
              relief="flat").pack(side="left", padx=5)

    tk.Button(control_frame,
              text="📜 Pedidos Anteriores",
              command=mostrar_pedidos_anteriores,
              bg="#1a73e8",
              fg="white",
              font=FUENTE_NORMAL,
              relief="flat").pack(side="left", padx=5)

    tk.Button(control_frame,
              text="🔙 Cerrar Sesión",
              command=lambda: [ventana.destroy(), return_callback()],
              bg=COLOR_CERRAR,
              fg="white",
              font=FUENTE_NORMAL,
              relief="flat").pack(side="right", padx=5)

    mostrar_pedidos()
    ventana.mainloop()
