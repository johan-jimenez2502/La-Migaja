import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Clases import Producto, Pedido

# 🎨 Colores corporativos
FONDO = "#F5E9CC"
COLOR_BOTON = "#8B2F23"
COLOR_TEXTO = "#1D5A75"
FUENTE = ("Times New Roman", 11)

def ventana_mesero(restaurante):
    ventana = tk.Tk()
    ventana.iconbitmap("Logo_migaja.ico")
    ventana.title("La Migaja - Mesero")
    ventana.geometry("500x600")
    ventana.configure(bg=FONDO)

    logo = Image.open("Logo_migaja.jpg")
    logo = logo.resize((200, 200))
    logo_tk = ImageTk.PhotoImage(logo)
    tk.Label(ventana, image=logo_tk, bg=FONDO).pack(pady=10)

    tk.Label(ventana, text="Menú del Día", font=("Times New Roman", 16, "bold"), bg=FONDO, fg=COLOR_TEXTO).pack()

    productos = restaurante.obtener_menu()
    spins_producto = {}

    frame_menu = tk.Frame(ventana, bg=FONDO)
    frame_menu.pack(pady=10)

    for producto in productos:
        fila = tk.Frame(frame_menu, bg=FONDO)
        fila.pack(fill="x", pady=2, padx=10)

        tk.Label(fila, text=f"{producto.nombre} - ${producto.precio}", font=FUENTE, bg=FONDO, width=30, anchor="w").pack(side="left")
        spin = tk.Spinbox(fila, from_=0, to=10, width=3)
        spin.pack(side="right")
        spins_producto[producto.codigo] = (spin, producto)

    tk.Label(ventana, text="Número de mesa:", font=FUENTE, bg=FONDO).pack()
    entrada_mesa = tk.Entry(ventana)
    entrada_mesa.pack()

    def enviar():
        mesa = entrada_mesa.get().strip()
        if not mesa:
            messagebox.showwarning("⚠️ Atención", "Debes ingresar el número de mesa.")
            return

        pedido = Pedido(mesa=mesa)
        for codigo, (spin, producto) in spins_producto.items():
            cantidad = int(spin.get())
            for _ in range(cantidad):
                pedido.agregar_producto(producto)

        if not pedido.items:
            messagebox.showinfo("🚫", "No seleccionaste ningún producto.")
            return

        restaurante.enviar_pedido(pedido)
        messagebox.showinfo("✅", f"Pedido enviado correctamente para Mesa {mesa}")
        entrada_mesa.delete(0, tk.END)
        for spin, _ in spins_producto.values():
            spin.delete(0, tk.END)
            spin.insert(0, "0")

    tk.Button(ventana, text="📤 Enviar pedido", command=enviar, bg=COLOR_BOTON, fg="white", font=("Times New Roman", 12, "bold")).pack(pady=20)

    def volver():
        ventana.destroy()
        import Frontend
        Frontend.seleccionar_rol()

    tk.Button(ventana, text="🔙 Volver", command=volver, bg="#40754C", fg="white").pack(pady=5)

    ventana.mainloop()
