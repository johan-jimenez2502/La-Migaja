import tkinter as tk
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
from Login import iniciar_app  # Cambia "login" por el nombre de tu archivo que contiene iniciar_app


def pantalla_bienvenida(root, callback_a_login):
    ventana = tk.Toplevel(root)
    ventana.title("Bienvenido a La Migaja")
    ventana.geometry("500x400")
    ventana.configure(bg="#f1ddbf")
    ventana.resizable(False, False)
    ventana.iconbitmap("Logo_migaja.ico")

    # Cargar imagen del logo
    try:
        logo = Image.open("Logo_migaja.jpg")
        logo = logo.resize((150, 150))
        logo_tk = ImageTk.PhotoImage(logo)
        lbl_logo = tk.Label(ventana, image=logo_tk, bg="#f1ddbf")
        lbl_logo.image = logo_tk
        lbl_logo.pack(pady=30)
    except:
        pass

    # Título
    tk.Label(ventana, text="Bienvenido a La Migaja",
             font=("Times New Roman", 20, "bold"),
             bg="#f1ddbf", fg="#8B2F23").pack()

    # Transición automática tras 3 segundos
    ventana.after(3000, lambda: [ventana.destroy(), callback_a_login()])
