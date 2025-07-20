from Conexion_fb import db

# Diccionario de precios fijos basados en el nombre del producto
precios_actualizados = {
    # Entradas Calientes
    "Arepitas de maíz rellenas de queso ahumado": 22000,
    "Empanadas crujientes con ají de la casa": 19000,
    "Carimañolas rellenas de queso costeño o carne": 20000,

    # Entradas Frías
    "Ceviche de camarón al estilo colombiano": 35000,
    "Ensalada fresca de aguacate con mango y vinagreta de panela": 28000,
    "Tartar de pescado blanco con cítricos y ají dulce": 38000,

    # Delicias Regionales
    "Chicharrón crocante en cubos con limón": 32000,
    "Morcilla caramelizada con reducción de panela": 25000,
    "Tamalitos pequeños de maíz tierno (antojito andino)": 22000,

    # Región Andina
    "Gran Bandeja Antioqueña": 55000,
    "Ajiaco de Santafé con Alcaparras y Nata": 48000,
    "Mondongo Campesino al Estilo Bogotano": 42000,

    # Región Pacífica
    "Sancocho Trifásico del Valle en Fondo de Cilantro": 52000,
    "Arroz Atollado de la Abuela Negra": 47000,
    "Chuleta Valluna Crocante con Ensalada Tropical": 45000,

    # Región Orinoquía
    "Ternera a la Llanera con Yuca Mantequillosa": 65000,
    "Carne a la Perra al Estilo Casanare": 58000,
    "Gallina Criolla Sudada con Papa Colorada": 50000,

    # Región Caribe
    "Pescado Frito Caribeño con Arroz de Coco y Patacón": 60000,
    "Mojarra en Salsa de Coco y Azafrán": 53000,
    "Arroz de Camarón al Estilo Cartagenero": 55000,

    # Jugos
    "Lulo": 10000,
    "Maracuyá": 10000,
    "Guanábana": 10000,
    "Borojó": 10000,
    "Mango": 10000,
    "Mango biche con limón": 10000,
    "Tomate de árbol": 10000,

    # Bebidas Frías
    "Limonada de coco": 13000,
    "Limonada con hierbabuena": 10000,
    "Agua de panela con limón (fría)": 8000,
    "Salpicón de frutas con soda": 15000,
    "Champús valluno (versión fría)": 12000,

    # Bebidas Calientes
    "Café colombiano filtrado (origen regional)": 9000,
    "Espresso / Americano / Capuchino": 8000,
    "Chocolate santafereño con queso": 12000,
    "Té de panela con jengibre": 10000,
    "Canelazo (versión sin alcohol)": 11000,
    "Avena caliente con canela": 10000,

    # Bebidas con Alcohol
    "Aguardiente (seco o dulce)": 12000,
    "Refajo (cerveza + gaseosa roja)": 18000,
    "Chicha fermentada de maíz": 15000,
    "Guarapo fermentado de caña": 13000,
    "Ron añejo (Caldas, Medellín o selección internacional)": 25000
}

# Recorrer toda la colección y actualizar precios por nombre
docs = db.collection("menu").stream()
total_actualizados = 0

for doc in docs:
    data = doc.to_dict()
    nombre = data.get("nombre", "").strip()
    if nombre in precios_actualizados:
        nuevo_precio = precios_actualizados[nombre]
        db.collection("menu").document(doc.id).update({"precio": nuevo_precio})
        print(f"✅ Precio actualizado: {nombre} → ${nuevo_precio:,}")
        total_actualizados += 1
    else:
        print(f"❌ No se encontró precio para: {nombre}")

print(f"\n🎉 Precios actualizados correctamente: {total_actualizados}")
