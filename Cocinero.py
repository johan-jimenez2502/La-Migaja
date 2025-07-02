import tkinter as tk
from tkinter import messagebox
from Clases import Restaurante

# 🎨 Colores corporativos
FONDO = "#F5E9CC"
FUENTE = ("Times New Roman", 11)
TEXTO_TITULO = ("Times New Roman", 14, "bold")

def ventana_cocinero(restaurante):
    ventana = tk.Tk()
    ventana.iconbitmap("Logo_migaja.ico")
    ventana.title("👨‍🍳 Cocina - Pedidos Pendientes")
    ventana.geometry("500x600")
    ventana.configure(bg=FONDO)

    tk.Label(ventana, text="📋 Pedidos pendientes:", font=TEXTO_TITULO, bg=FONDO).pack(pady=10)

    # Frame con Scroll
    canvas = tk.Canvas(ventana, bg=FONDO, highlightthickness=0)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=FONDO)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    pedidos = restaurante.obtener_pedidos_pendientes()

    if not pedidos:
        tk.Label(scroll_frame, text="No hay pedidos pendientes", font=FUENTE, bg=FONDO).pack(pady=20)
    else:
        for pedido in pedidos:
            frame = tk.Frame(scroll_frame, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="#FAF3E0")
            frame.pack(padx=30, pady=5, fill="x")

            mesa = pedido.get('mesa', 'Desconocida')
            tk.Label(frame, text=f"Mesa: {mesa}", font=("Times New Roman", 12, "bold"), bg="#FAF3E0").pack(anchor="center")

            for item in pedido.get("items", []):
                nombre = item.get("nombre", "Producto")
                precio = item.get("precio", "???")
                tk.Label(frame, text=f"- {nombre} (${precio})", font=FUENTE, bg="#FAF3E0").pack(anchor="center")

            total = pedido.get("total", 0)
            tk.Label(frame, text=f"Total: ${total}", font=("Times New Roman", 11, "italic"), bg="#FAF3E0").pack(anchor="center")

            def marcar_servido_closure(pedido_id):
                return lambda: marcar_servido(pedido_id, ventana, restaurante)

            tk.Button(frame, text="✅ Marcar como servido", bg="#8B2F23", fg="white", font=FUENTE,
                      command=marcar_servido_closure(pedido["id"])).pack(pady=5)

    # Botón Volver
    def volver():
        ventana.destroy()
        import Frontend
        Frontend.seleccionar_rol()

    tk.Button(ventana, text="🔙 Volver", command=volver, bg="#40754C", fg="white", font=FUENTE).pack(pady=10)

    ventana.mainloop()

def marcar_servido(pedido_id, ventana, restaurante):
    pedido = restaurante.obtener_pedido_por_id(pedido_id)
    restaurante.descontar_inventario(pedido)
    restaurante.marcar_pedido_servido(pedido_id)
    messagebox.showinfo("✅ Pedido servido", f"El pedido {pedido_id} ha sido marcado como servido.")
    ventana.destroy()
    ventana_cocinero(restaurante)  # 🔄 Recarga la ventana

