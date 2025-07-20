from Conexion_fb import db
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter

class Producto:
    def __init__(self, codigo, nombre, precio, categoria="", subcategoria="", imagen="", unidades=0, ):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.imagen = imagen
        self.unidades = unidades
        

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - ${self.precio} ({self.unidades} unidades)"


class Pedido:
    def __init__(self, mesa=""):
        self.items = []
        self.total = 0
        self.estado = "pendiente"
        self.mesa = mesa

    def agregar_producto(self, producto):
        self.items.append(producto)
        self.total += producto.precio

    def a_dict(self):
        return {
            "items": [vars(p) for p in self.items],
            "total": self.total,
            "estado": self.estado,
            "mesa": self.mesa
        }


class Restaurante:
    def __init__(self, db):
        self.db = db

    def obtener_menu(self):
        productos = []
        docs = self.db.collection("menu").stream()
        for doc in docs:
            data = doc.to_dict()
            producto = Producto(
                codigo=data.get("codigo", ""),
                nombre=data.get("nombre", ""),
                precio=float(data.get("precio", 0)),
                categoria=data.get("categoria", ""),
                subcategoria=data.get("subcategoria", ""),
                imagen=data.get("imagen", "")
            )
            productos.append(producto)
        return productos
    def enviar_pedido(self, pedido):
        try:
            pedido_ref = self.db.collection("pedidos").document()
            pedido_id = pedido_ref.id

            numero_pedido = self.obtener_siguiente_numero_pedido()

            data = pedido.a_dict()
            data["id"] = pedido_id
            data["numero_pedido"] = numero_pedido
            data["hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["pagado"] = False  # ✅ AGREGAR ESTO

            pedido_ref.set(data)
        except Exception as e:
            print(f"Error al enviar pedido: {e}")

    def obtener_pedidos_pendientes(self):
        pedidos = []
        try:
            docs = self.db.collection("pedidos").where("estado", "==", "pendiente").stream()
            for doc in docs:
                pedido = doc.to_dict()
                pedido["id"] = doc.id
                pedidos.append(pedido)
        except Exception as e:
            print(f"Error al obtener pedidos: {e}")
        return pedidos

    def marcar_pedido_servido(self, pedido_id):
        try:
            self.db.collection("pedidos").document(pedido_id).update({"estado": "servido"})
        except Exception as e:
            print(f"Error al actualizar pedido: {e}")

    def obtener_pedido_por_id(self, pedido_id):
        try:
            doc = self.db.collection("pedidos").document(pedido_id).get()
            if doc.exists:
                pedido = doc.to_dict()
                pedido["id"] = pedido_id
                return pedido
        except Exception as e:
            print(f"Error al obtener pedido por ID: {e}")
        return None

    def obtener_pedidos_servidos(self):
        pedidos = []
        try:
            docs = self.db.collection("pedidos") \
                .where("estado", "==", "servido") \
                .order_by("hora", direction="DESCENDING") \
                .stream()
            for doc in docs:
                pedido = doc.to_dict()
                pedido["id"] = doc.id
                pedidos.append(pedido)
        except Exception as e:
            print(f"Error al obtener pedidos servidos: {e}")
        return pedidos

    def obtener_inventario(self):
        productos = []
        try:
            docs = self.db.collection("menu").stream()
            for doc in docs:
                data = doc.to_dict()
                producto = Producto(
                    codigo=data.get("codigo", ""),
                    nombre=data.get("nombre", ""),
                    precio=float(data.get("precio", 0)),
                    categoria=data.get("categoria", ""),
                    subcategoria=data.get("subcategoria", ""),
                    imagen=data.get("imagen", ""),
                    unidades=int(data.get("unidades", 0))
                )
                productos.append(producto)
        except Exception as e:
            print(f"Error al obtener inventario: {e}")
        return productos

    def actualizar_unidades_producto(self, codigo, nuevas_unidades):
        try:
            doc_ref = self.db.collection("menu").document(codigo)
            if doc_ref.get().exists:
                doc_ref.update({"unidades": nuevas_unidades})
                return True
            else:
                print("Producto no encontrado.")
                return False
        except Exception as e:
            print(f"Error al actualizar unidades: {e}")
            return False

    def obtener_siguiente_numero_pedido(self):
        try:
            contador_ref = self.db.collection("utilidades").document("contador")
            doc = contador_ref.get()

            if doc.exists:
                numero_actual = doc.to_dict().get("contador", 0)
            else:
                numero_actual = 0

            nuevo_numero = numero_actual + 1
            if nuevo_numero > 9999:
                nuevo_numero = 1

            contador_ref.set({"contador": nuevo_numero})
            return nuevo_numero
        except Exception as e:
            print(f"Error al obtener contador: {e}")

            return 0
    def marcar_pedido_pagado(self, pedido_id):
        try:
            self.db.collection("pedidos").document(pedido_id).update({"pagado": True})
        except Exception as e:
            print(f"Error al marcar como pagado: {e}")

    def obtener_pedidos_servidos_no_pagados(self):
        pedidos = []
        try:
            docs = self.db.collection("pedidos") \
                .where(filter=FieldFilter("estado", "==", "servido")) \
                .where(filter=FieldFilter("pagado", "==", False)) \
                .stream()
            for doc in docs:
                pedido = doc.to_dict()
                pedido["id"] = doc.id
                pedidos.append(pedido)
        except Exception as e:
            print(f"Error al obtener pedidos servidos no pagados: {e}")
        return pedidos