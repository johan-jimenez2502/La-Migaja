import tkinter as tk
from pantalla_bienvenida import pantalla_bienvenida
from Login import iniciar_app

def main():
    # Crear ventana raíz oculta
    root = tk.Tk()
    root.withdraw()  # Oculta la raíz mientras aparece la pantalla bienvenida

    # Mostrar pantalla de bienvenida y después ir a login
    pantalla_bienvenida(root, iniciar_app)

    # Ejecutar la app
    root.mainloop()

if __name__ == "__main__":
    main()