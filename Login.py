import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Conexion_fb import db
from Clases import Restaurante

from Mesero import ventana_mesero
from Cocinero import ventana_cocinero
from Registrarse import ventana_registro
from administrador import ventana_administrador

restaurante = Restaurante(db)
main_app_window = None

def iniciar_app():
    global main_app_window
    if main_app_window is None:
        main_app_window = tk.Toplevel()
        main_app_window.title("🔐 Ingreso - La Migaja")
        main_app_window.geometry("600x800")
        main_app_window.configure(bg="#f1ddbf")
        main_app_window.iconbitmap("Logo_migaja.ico")
        main_app_window.resizable(False, False)

        # 📷 Logo
        try:
            imagen_logo = Image.open("Logo_migaja.jpg")
            imagen_logo = imagen_logo.resize((120, 120), Image.Resampling.LANCZOS)

            logo = ImageTk.PhotoImage(imagen_logo)
            label_logo = tk.Label(main_app_window, image=logo, bg="#f1ddbf")
            label_logo.image = logo
            label_logo.pack(pady=(20, 10))
        except Exception as e:
            print("No se pudo cargar el logo:", e)

        # 🧾 Título
        tk.Label(main_app_window, text="Inicio de Sesión", font=("Times New Roman", 16, "bold"),
                 bg="#f1ddbf", fg="#8B2F23").pack(pady=(0, 20))

        # Usuario
        tk.Label(main_app_window, text="Usuario:", bg="#f1ddbf", anchor="w").pack(pady=(5, 0), padx=30, fill="x")
        entrada_usuario = tk.Entry(main_app_window, font=("Times New Roman", 11))
        entrada_usuario.pack(padx=30, pady=5, fill="x")

        # Contraseña
        tk.Label(main_app_window, text="Contraseña:", bg="#f1ddbf", anchor="w").pack(pady=(10, 0), padx=30, fill="x")
        entrada_contrasena = tk.Entry(main_app_window, show="*", font=("Times New Roman", 11))
        entrada_contrasena.pack(padx=30, pady=5, fill="x")

        # Botón ingresar
        tk.Button(main_app_window, text="Ingresar",
                  command=lambda: login(entrada_usuario, entrada_contrasena),
                  bg="#8B2F23", fg="white", font=("Times New Roman", 11),
                  relief="flat", height=2).pack(pady=(25, 10), padx=50, fill="x")

        # Botón registro
        tk.Button(main_app_window, text="Registrar nuevo usuario",
                  command=lambda: abrir_registro(main_app_window),
                  bg="#40754C", fg="white", font=("Times New Roman", 11),
                  relief="flat", height=2).pack(pady=(0, 20), padx=50, fill="x")

        # Cierre seguro
        main_app_window.protocol("WM_DELETE_WINDOW", on_closing_main_window)
    else:
        main_app_window.deiconify()

def on_closing_main_window():
    if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
        main_app_window.destroy()

def return_to_login_callback():
    global main_app_window
    if main_app_window:
        main_app_window.deiconify()

def login(entrada_usuario_widget, entrada_contrasena_widget):
    usuario = entrada_usuario_widget.get().strip()
    contraseña = entrada_contrasena_widget.get().strip()

    if not usuario or not contraseña:
        messagebox.showwarning("⚠️", "Debes completar todos los campos.")
        return

    try:
        user_ref = db.collection("usuarios").document(usuario).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            if user_data["contraseña"] == contraseña:
                main_app_window.withdraw()
                rol = user_data.get("rol")
                nombre = user_data.get("nombre")

                if rol == "Mesero":
                    ventana_mesero(restaurante, nombre, return_to_login_callback)
                elif rol == "Cocinero":
                    ventana_cocinero(restaurante, nombre, return_to_login_callback)
                elif rol == "Administrador":
                    ventana_administrador(restaurante, nombre, return_to_login_callback)
            else:
                messagebox.showerror("❌ Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("❌ Error", "Usuario no registrado")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Error de conexión: {str(e)}")

def abrir_registro(parent_window):
    parent_window.withdraw()
    ventana_registro(parent_window, return_to_login_callback)


