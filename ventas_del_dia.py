# VentasDelDia.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageTk

FONDO = "#f1ddbf"
COLOR_TEXTO = "#1a1a1a"
FUENTE = ("Helvetica", 11)

def ventana_ventas_del_dia(restaurante, return_callback):
    ventana = tk.Toplevel()
    ventana.title("📊 Ventas del Día")
    ventana.geometry("600x500")
    ventana.configure(bg=FONDO)
    # Logo de La Migaja
    logo_img = Image.open("Logo_migaja.jpg")
    logo_img = logo_img.resize((130, 130))
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(ventana, image=logo_img, bg="#f1ddbf")
    logo_label.image = logo_img
    logo_label.pack(pady=(10, 0))

    tk.Label(ventana,
             text="Productos vendidos hoy",
             font=("Helvetica", 16, "bold"),
             bg=FONDO,
             fg=COLOR_TEXTO).pack(pady=(10, 5))

    separator = tk.Frame(ventana, bg=COLOR_TEXTO, height=2)
    separator.pack(fill="x", padx=20, pady=(0, 10))

    contenedor_scroll = tk.Frame(ventana, bg=FONDO)
    contenedor_scroll.pack(fill="both", expand=True, padx=10)

    canvas = tk.Canvas(contenedor_scroll, bg=FONDO, highlightthickness=0)
    scrollbar = ttk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas.yview)
    frame_scrollable = tk.Frame(canvas, bg=FONDO)

    frame_scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    hoy = datetime.now().strftime("%Y-%m-%d")
    ventas = defaultdict(lambda: {"cantidad": 0, "subtotal": 0})

    pedidos = restaurante.obtener_pedidos_servidos()
    total_dia = 0

    for pedido in pedidos:
        if pedido.get("hora", "").startswith(hoy):
            for item in pedido.get("items", []):
                nombre = item["nombre"]
                precio = float(item.get("precio", 0))
                ventas[nombre]["cantidad"] += 1
                ventas[nombre]["subtotal"] += precio
                total_dia += precio

    if not ventas:
        tk.Label(frame_scrollable,
                 text="🔕 No hay ventas registradas hoy.",
                 bg=FONDO,
                 font=FUENTE,
                 fg=COLOR_TEXTO).pack(pady=20)
    else:
        for nombre, info in ventas.items():
            texto = f"• {nombre} x {info['cantidad']}  -  ${info['subtotal']:.2f}"
            tk.Label(frame_scrollable,
                     text=texto,
                     bg=FONDO,
                     font=FUENTE,
                     anchor="w",
                     justify="left").pack(anchor="w", padx=10, pady=2)

    separator2 = tk.Frame(ventana, bg="#999", height=1)
    separator2.pack(fill="x", padx=20, pady=(10, 5))

    tk.Label(ventana,
             text=f"💰 Total del día: ${total_dia:.2f}",
             font=("Helvetica", 13, "bold"),
             bg=FONDO,
             fg="#2e7d32").pack(pady=(5, 20))
    # Botón para volver a la pantalla anterior (Administrador)
    def volver():
        ventana.destroy()
        if return_callback:
            return_callback()

    tk.Button(
        ventana,
        text="⬅️ Volver al menú anterior",
        command=volver,
        font=("Helvetica", 11, "bold"),
        bg="#8B2F23",
        fg="white",
        activebackground="#a0422f",
        activeforeground="white",
        relief="raised",
        padx=10,
        pady=5
    ).pack(pady=10)
