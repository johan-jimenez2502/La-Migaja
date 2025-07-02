from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Clases import Restaurante, Pedido

# Configuración de estilo (según tu código original)
FONDO = "#F5E9CC"
COLOR_BOTON = "#8B2F23"
COLOR_TEXTO = "#1D5A75"
FUENTE = ("Times New Roman", 11)
TEXTO_TITULO = ("Times New Roman", 14, "bold")

def ventana_mesero(restaurante, nombre_usuario):
    ventana = tk.Tk()
    ventana.iconbitmap("Logo_migaja.ico")
    ventana.title(f"La Migaja - Mesero ({nombre_usuario})")
    ventana.geometry("500x700")
    ventana.configure(bg=FONDO)
    
    # Frame principal (organización vertical)
    main_frame = tk.Frame(ventana, bg=FONDO)
    main_frame.pack(fill="both", expand=True)
    
    # --- PARTE SUPERIOR: Logo y Bienvenida ---
    top_frame = tk.Frame(main_frame, bg=FONDO)
    top_frame.pack(fill="x", pady=10)
    
    # Logo (manteniendo tu implementación original)
    try:
        logo = Image.open("Logo_migaja.jpg")
        logo = logo.resize((150, 150), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo)
        ventana.logo_tk = logo_tk  # Referencia global
        tk.Label(top_frame, image=logo_tk, bg=FONDO).pack()
    except:
        tk.Label(top_frame, text="La Migaja", font=TEXTO_TITULO, bg=FONDO).pack()

    # Bienvenida
    tk.Label(top_frame, 
             text=f"Bienvenido, {nombre_usuario}",
             font=FUENTE,
             bg=FONDO).pack(pady=5)

    # --- PARTE CENTRAL: Menú con Scroll ---
    center_frame = tk.Frame(main_frame, bg=FONDO)
    center_frame.pack(fill="both", expand=True)
    
    tk.Label(center_frame, 
             text="Menú del Día", 
             font=TEXTO_TITULO, 
             bg=FONDO, 
             fg=COLOR_TEXTO).pack()

    # Canvas y Scrollbar
    canvas = tk.Canvas(center_frame, bg=FONDO, highlightthickness=0)
    scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=FONDO)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Obtener y mostrar productos
    productos = restaurante.obtener_menu()
    spins_producto = {}  # Diccionario para guardar los selectores

    for producto in productos:
        frame = tk.Frame(scroll_frame, bg=FONDO)
        frame.pack(fill="x", pady=2, padx=10)

        # Nombre y precio (formato original)
        tk.Label(frame, 
                 text=f"{producto.nombre} - ${producto.precio}", 
                 font=FUENTE, 
                 bg=FONDO, 
                 width=30, 
                 anchor="w").pack(side="left")
        
        # Selector de cantidad
        spin = tk.Spinbox(frame, from_=0, to=10, width=3)
        spin.pack(side="right")
        spins_producto[producto.codigo] = (spin, producto)

    # --- PARTE INFERIOR: Formulario de Pedido ---
    bottom_frame = tk.Frame(main_frame, bg=FONDO)
    bottom_frame.pack(fill="x", pady=10)

    # Entrada de mesa
    tk.Label(bottom_frame, 
             text="Número de mesa:", 
             font=FUENTE, 
             bg=FONDO).pack()
    
    entrada_mesa = tk.Entry(bottom_frame, font=FUENTE)
    entrada_mesa.pack(pady=5)

    # Función para enviar pedido (original mejorada)
    def enviar():
        mesa = entrada_mesa.get().strip()
        if not mesa:
            messagebox.showwarning("⚠️", "Ingrese el número de mesa")
            return

        pedido = Pedido(mesa=mesa)
        for codigo, (spin, producto) in spins_producto.items():
            cantidad = int(spin.get())
            for _ in range(cantidad):
                pedido.agregar_producto(producto)

        if not pedido.items:
            messagebox.showwarning("⚠️", "Seleccione al menos un producto")
            return

        try:
            restaurante.enviar_pedido(pedido)
            messagebox.showinfo("✅", f"Pedido para Mesa {mesa} enviado")
            # Limpiar selección
            entrada_mesa.delete(0, tk.END)
            for spin, _ in spins_producto.values():
                spin.delete(0, tk.END)
                spin.insert(0, "0")
        except Exception as e:
            messagebox.showerror("❌", f"Error: {str(e)}")

    # Botón enviar (estilo original)
    tk.Button(bottom_frame, 
              text="📤 Enviar pedido", 
              command=enviar,
              bg=COLOR_BOTON,
              fg="white",
              font=TEXTO_TITULO).pack(pady=10)

    # Cerrar sesión
    def volver():
        if messagebox.askyesno("Confirmar", "¿Cerrar sesión?"):
            ventana.destroy()
            from Login import iniciar_app
            iniciar_app()

    tk.Button(bottom_frame, 
              text="🔙 Cerrar Sesión", 
              command=volver,
              bg="#333333",
              fg="white").pack()

    ventana.protocol("WM_DELETE_WINDOW", volver)
    ventana.mainloop()