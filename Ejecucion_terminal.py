from Clases import Restaurante, Pedido

restaurante = Restaurante()

def mostrar_menu():
    print("\n----- MENÚ LA MIGAJA -----")
    menu = restaurante.obtener_menu()
    for producto in menu:
        print(producto)
    return menu

def agregar_pedido(menu):
    mesa = input("\n🪑 Ingrese el número o nombre de la mesa: ").strip()
    pedido = Pedido(mesa=mesa)
    codigos_disponibles = {p.codigo: p for p in menu}

    while True:
        codigo = input("\nIngrese el código del producto (o 'fin' para terminar): ").upper()
        if codigo == "FIN":
            break
        if codigo in codigos_disponibles:
            producto = codigos_disponibles[codigo]
            pedido.agregar_producto(producto)
            print(f"➕ Añadido: {producto.nombre} - ${producto.precio}")
        else:
            print("❌ Código no encontrado.")

    if pedido.items:
        restaurante.enviar_pedido(pedido)
        print("\n✅ Pedido enviado a cocina.")
        print(f"🪑 Mesa: {pedido.mesa}")
        print(f"💰 Total: ${pedido.total}")

def ver_pedidos_cocinero():
    pedidos = restaurante.obtener_pedidos_pendientes()
    if not pedidos:
        print("🕊 No hay pedidos pendientes.")
        return

    print("\n📦 PEDIDOS PENDIENTES:")
    for idx, pedido in enumerate(pedidos, 1):
        print(f"\n📋 Pedido #{idx}")
        print(f"🆔 ID: {pedido['id']}")
        for item in pedido["items"]:
            print(f" - {item['nombre']} (${item['precio']})")
        print(f"💰 Total: ${pedido['total']}")
        print(f"🆔 ID: {pedido['id']}")

    while True:
        opcion = input("\n¿Deseas marcar algún pedido como servido? (s/n): ").lower()
        if opcion == "s":
            id_elegido = input("🔎 Ingresa el ID exacto del pedido que quieres marcar como servido: ").strip()
            try:
                restaurante.marcar_pedido_servido(id_elegido)
            except Exception as e:
                print(f"❌ Error al actualizar: {e}")
        elif opcion == "n":
            break
        else:
            print("⚠️ Ingresa solo 's' o 'n'.")

    pedidos = restaurante.obtener_pedidos_pendientes()
    if not pedidos:
        print("🕊 No hay pedidos pendientes.")
        return

    print("\n📦 PEDIDOS PENDIENTES:")
    for idx, pedido in enumerate(pedidos, 1):
        print(f"🪑 Mesa: {pedido.get('mesa', 'Sin asignar')}")
        print(f"\n📋 Pedido #{idx}")
        for item in pedido["items"]:
            print(f" - {item['nombre']} (${item['precio']})")
        print(f"💰 Total: ${pedido['total']}")
        print(f"ID: {pedido['id']}")

    # Preguntar si quiere marcar uno como servido
    opcion = input("\n¿Deseas marcar algún pedido como servido? (s/n): ").lower()
    if opcion == "s":
        id_elegido = input("🔎 Ingresa el ID del pedido a marcar como servido: ").strip()
        restaurante.marcar_pedido_servido(id_elegido)




if __name__ == "__main__":
    while True:
        print("\n--- BIENVENIDO A LA MIGAJA ---")
        print("1. Tomar pedido (mesero)")
        print("2. Ver pedidos pendientes (cocinero)")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu = mostrar_menu()
            agregar_pedido(menu)
        elif opcion == "2":
            ver_pedidos_cocinero()
        elif opcion == "3":
            print("Hasta pronto 👋")
            break
        else:
            print("Opción inválida.")
