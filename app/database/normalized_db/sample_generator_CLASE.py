from groq import Groq
import json
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# ======================================
# CONFIGURACION
# ======================================
load_dotenv()
api_k = os.getenv("GROQ_API_KEY")
API_KEY = api_k

client = Groq(api_key=API_KEY)

# ======================================
# GROQ
# ======================================

def generar_personas():

    prompt = """
    Genera datos ficticios para una tienda online de ropa.

    Devuelve únicamente JSON válido.

    Formato:

    {
    "clientes": [
        {
        "nombre":"",
        "apellido":"",
        "email":"",
        "telefono":"",
        "fecha_registro":"YYYY-MM-DD"
        }
    ],

    "empleados":[
        {
        "nombre":"",
        "apellido":"",
        "email":"",
        "cargo":"",
        "fecha_contratacion":"YYYY-MM-DD"
        }
    ],

    "proveedores":[
        {
        "nombre":"",
        "telefono":"",
        "email":""
        }
    ]
    }

    Genera exactamente:

    - 100 clientes
    - 20 empleados
    - 10 proveedores

    Cargos posibles:

    - Administrador
    - Atención al cliente
    - Encargado de inventario
    - Empaquetador
    - Analista de marketing
    - Supervisor logístico

    Usa nombres hispanos.
    """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=8000,
            messages=[
                {
                    "role": "system",
                    "content": "Responde solamente JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        contenido = response.choices[0].message.content.strip()

        if contenido.startswith("```"):
            contenido = contenido.split("```")[1]
            if contenido.startswith("json"):
                contenido = contenido[4:]

        return json.loads(contenido)


    # ======================================
    # METODOS DE PAGO
    # ======================================

    def generar_metodos_pago():

        return [
            {
                "metodo_id": 1,
                "metodo": "Tarjeta"
            },
            {
                "metodo_id": 2,
                "metodo": "Transferencia"
            },
            {
                "metodo_id": 3,
                "metodo": "Efectivo"
            }
        ]


    # ======================================
    # DIRECCIONES
    # ======================================

    def generar_direcciones(clientes):

        calles = [
            "Avenida Central",
            "Calle Principal",
            "Los Robles",
            "Las Flores",
            "Villa Fontana",
            "Bolonia",
            "Altamira",
            "San Judas",
            "Bello Horizonte",
            "Linda Vista"
        ]

        direcciones = []

        for cliente_id in range(1, len(clientes) + 1):

            direcciones.append({

                "direccion_id": cliente_id,

                "direccion":
                    f"{random.choice(calles)} #{random.randint(1,999)}",

                "cliente_id": cliente_id
            })

        return direcciones


    # ======================================
    # VENTAS
    # ======================================

    def generar_ventas():

        estados = [
            "Pendiente",
            "Procesando",
            "Enviado",
            "Entregado"
        ]

        ventas = []

        for venta_id in range(1, 201):

            fecha = (
                datetime.now()
                - timedelta(days=random.randint(0, 365))
            )

            ventas.append({

                "venta_id": venta_id,

                "cliente_id": random.randint(1, 100),

                "fecha": fecha.strftime("%Y-%m-%d"),

                "total": round(
                    random.uniform(20, 350),
                    2
                ),

                "estado": random.choice(estados),

                "metodo_pago_id": random.randint(1, 3)
            })

        return ventas


    # ======================================
    # ENVIOS
    # ======================================

    def generar_envios(ventas, direcciones):

        estados = [
            "Preparando",
            "En tránsito",
            "Entregado"
        ]

        envios = []

        for venta in ventas:

            cliente_id = venta["cliente_id"]

            direccion = next(
                d for d in direcciones
                if d["cliente_id"] == cliente_id
            )

            fecha_envio = datetime.strptime(
                venta["fecha"],
                "%Y-%m-%d"
            )

            fecha_entrega = (
                fecha_envio
                + timedelta(days=random.randint(2, 10))
            )

            envios.append({

                "envios_id": venta["venta_id"],

                "venta_id": venta["venta_id"],

                "fecha_envio":
                    fecha_envio.strftime("%Y-%m-%d"),

                "fecha_entrega":
                    fecha_entrega.strftime("%Y-%m-%d"),

                "estado":
                    random.choice(estados),

                "direccion_id":
                    direccion["direccion_id"]
            })

        return envios


    # ======================================
    # DETALLE VENTAS
    # ======================================

    def generar_detalle_ventas(cantidad_productos):

        detalles = []

        detalle_id = 1

        for venta_id in range(1, 201):

            cantidad_items = random.randint(1, 4)

            for _ in range(cantidad_items):

                producto_id = random.randint(
                    1,
                    cantidad_productos
                )

                precio = round(
                    random.uniform(10, 80),
                    2
                )

                cantidad = random.randint(1, 3)

                detalles.append({

                    "detalle_id": detalle_id,

                    "venta_id": venta_id,

                    "producto_id": producto_id,

                    "cantidad": cantidad,

                    "precio_unitario": precio,

                    "subtotal":
                        round(precio * cantidad, 2)
                })

                detalle_id += 1

        return detalles


    # ======================================
    # MAIN
    # ======================================

    if __name__ == "__main__":

        datos = generar_personas()

        clientes = datos["clientes"]

        empleados = datos["empleados"]

        proveedores = datos["proveedores"]

        metodos_pago = generar_metodos_pago()

        direcciones = generar_direcciones(clientes)

        ventas = generar_ventas()

        envios = generar_envios(
            ventas,
            direcciones
        )

        # Ajusta según cuántos productos tengas
        detalle_ventas = generar_detalle_ventas(
            cantidad_productos=100
        )

        dataset = {

            "clientes": clientes,

            "empleados": empleados,

            "proveedores": proveedores,

            "metodos_pago": metodos_pago,

            "direcciones": direcciones,

            "ventas": ventas,

            "envios": envios,

            "detalle_ventas": detalle_ventas
        }

        with open(
            "datos_tienda.json",
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                dataset,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print("Datos generados correctamente.")