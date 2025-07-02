import tkinter as tk
from Conexion_fb import db
from Clases import Restaurante

restaurante = Restaurante(db)

def seleccionar_rol():
    root = tk.Tk()
    root.iconbitmap("Logo_migaja.ico")
    root.title("👥 Seleccionar Rol")
    root.geometry("300x200")
    root.configure(bg="#F5E9CC")

    tk.Label(root, text="¿Quién eres?", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Button(root, text="🧑‍🍳 Cocinero", font=("Arial", 12), width=20, command=lambda: abrir_cocinero(root)).pack(pady=5)
    tk.Button(root, text="🧑‍💼 Mesero", font=("Arial", 12), width=20, command=lambda: abrir_mesero(root)).pack(pady=5)

    root.mainloop()

def abrir_mesero(root):
    root.destroy()
    from Mesero import ventana_mesero
    ventana_mesero(restaurante)

def abrir_cocinero(root):
    root.destroy()
    from Cocinero import ventana_cocinero
    ventana_cocinero(restaurante)

seleccionar_rol()
