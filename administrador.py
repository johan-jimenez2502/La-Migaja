import tkinter as tk
from tkinter import messagebox
from ventas_del_dia import ventana_ventas_del_dia
from ventana_caja import ventana_caja
from PIL import Image, ImageTk
from menu import ventana_agregar_producto

# Colores y fuentes según estilo visual
FONDO = "#f1ddbf"
COLOR_BOTON = "#1d5a75"
COLOR_TEXTO = "#4b2b19"
FUENTE_TEXTO = ("Georgia", 14)
FUENTE_TITULO = ("Georgia", 18, "bold")

def ventana_administrador(restaurante_instance, nombre_usuario, return_callback):
    admin_win = tk.Toplevel()
    admin_win.title("Panel del Administrador")
    admin_win.geometry("600x450")
    admin_win.configure(bg=FONDO)
    admin_win.resizable(False, False)

    # Logo y encabezado
    header = tk.Frame(admin_win, bg=FONDO)
    header.pack(pady=10)

    try:
        logo_img = Image.open("Logo_migaja.jpg").resize((80, 80), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        tk.Label(header, image=logo_tk, bg=FONDO).pack(side="left", padx=10)
        admin_win.logo_tk = logo_tk  # Evitar recolección
    except:
        pass

    tk.Label(header, text="La Migaja", font=FUENTE_TITULO, bg=FONDO, fg=COLOR_TEXTO).pack(side="left")

    # Subtítulo
    tk.Label(admin_win, text=f"Bienvenido, {nombre_usuario}\nContinúa con la administración",
             font=FUENTE_TEXTO, bg=FONDO, fg=COLOR_TEXTO).pack(pady=5)

    # Sección central con botones
    button_frame = tk.Frame(admin_win, bg=FONDO)
    button_frame.pack(pady=20)

    def crear_boton(texto, comando, color=COLOR_BOTON):
        return tk.Button(
            button_frame,
            text=texto,
            font=FUENTE_TEXTO,
            bg=color,
            fg="white",
            width=25,
            height=2,
            bd=0,
            relief="flat",
            activebackground="#1e5f76",
            activeforeground="white",
            command=comando
        )

    # Botones principales
    crear_boton(
        "Agregar menú",
        lambda: [
            admin_win.destroy(),
            ventana_agregar_producto(
                restaurante_instance,
                nombre_usuario,
                lambda: ventana_administrador(restaurante_instance, nombre_usuario, return_callback)
            )
        ]
    ).pack(pady=8)



    crear_boton(
        "Ver Ventas del Día",
        lambda: [admin_win.destroy(), ventana_ventas_del_dia(restaurante_instance, lambda: ventana_administrador(restaurante_instance, nombre_usuario, return_callback))]
    ).pack(pady=8)

    crear_boton(
        "Ver Caja",
        lambda: [admin_win.destroy(), ventana_caja(restaurante_instance, lambda: ventana_administrador(restaurante_instance, nombre_usuario, return_callback))]
    ).pack(pady=8)

        # Frame inferior para separar visualmente el botón
    footer_frame = tk.Frame(admin_win, bg=FONDO)
    footer_frame.pack(pady=(10, 20))

    # Línea separadora visual
    tk.Frame(footer_frame, height=2, bg="#D3BFA0", bd=0).pack(fill="x", padx=40, pady=(10, 10))

    # Botón bonito de cerrar sesión
    crear_boton(
        "⏻  Cerrar sesión",
        lambda: [admin_win.destroy(), return_callback()],
        color="#8B2F23"  # Color vino elegante
    ).pack(pady=(30, 8))  # Más espacio arriba para separarlo visualmente



    admin_win.transient()
    admin_win.grab_set()
    admin_win.focus_set()