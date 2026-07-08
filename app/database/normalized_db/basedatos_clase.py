import sqlite3
import os
import random
import json
import pandas as pd
from app.database.sample_generator import generate_complex_strings
from app.database.init_db import generate_item
from app.database.sample_generator import generate_complex_strings
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

categories= {
                "tops": {
                    "subcategories": {
                        "tshirt": {
                            "styles": ["casual", "streetwear", "sport", "minimalist"],
                            "fit": ["slim", "regular", "oversize"],
                            "usage": ["daily", "casual", "gym"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester", "rayon", "spandex"],
                            "brands": {
                                "Nike":         (18, 55),
                                "Adidas":       (20, 60),
                                "H&M":          (8,  25),
                                "Zara":         (12, 35),
                                "Uniqlo":       (10, 30),
                                "Champion":     (15, 45),
                                "Supreme":      (40, 120),
                                "Ralph Lauren": (35, 90),
                            }
                        },
                        "shirt": {
                            "styles": ["formal", "casual", "business casual"],
                            "fit": ["slim", "regular"],
                            "usage": ["office", "formal events", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "lino", "rayon"],
                            "brands": {
                                "Ralph Lauren":   (60,  180),
                                "Calvin Klein":   (50,  150),
                                "Tommy Hilfiger": (55,  160),
                                "Zara":           (25,  70),
                                "H&M":            (15,  45),
                                "Brooks Brothers":(80,  220),
                                "ASOS":           (20,  60),
                                "Banana Republic":(60,  150),
                            }
                        },
                        "tank_top": {
                            "styles": ["casual", "sport", "streetwear"],
                            "fit": ["slim", "regular"],
                            "usage": ["gym", "summer", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester", "rayon", "spandex"],
                            "brands": {
                                "Nike":      (15, 40),
                                "Adidas":    (18, 45),
                                "Under Armour": (20, 50),
                                "H&M":       (6,  20),
                                "Zara":      (10, 28),
                                "Gymshark":  (22, 55),
                                "Champion":  (12, 35),
                            }
                        },
                        "sweatshirt": {
                            "styles": ["casual", "streetwear", "sport"],
                            "fit": ["regular", "oversize"],
                            "usage": ["casual", "winter", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "fleece", "poliester"],
                            "brands": {
                                "Nike":       (45,  110),
                                "Adidas":     (50,  120),
                                "Champion":   (35,  85),
                                "Supreme":    (90,  220),
                                "Carhartt":   (55,  130),
                                "H&M":        (20,  50),
                                "Zara":       (30,  70),
                                "Stussy":     (70,  150),
                            }
                        },
                        "turtleneck": {
                            "styles": ["elegant", "minimalist", "formal"],
                            "fit": ["slim", "regular"],
                            "usage": ["winter", "office", "formal events"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["lana", "algodon", "rayon"],
                            "brands": {
                                "Uniqlo":        (30,  70),
                                "Ralph Lauren":  (80,  200),
                                "Calvin Klein":  (60,  150),
                                "Zara":          (30,  75),
                                "J.Crew":        (50,  120),
                                "Banana Republic":(70, 160),
                            }
                        },
                        "tuxedo": {
                            "styles": ["luxury", "formal", "elegant"],
                            "fit": ["slim", "tailored"],
                            "usage": ["wedding", "gala", "formal events"],
                            "allowed_genders": ["hombre", "mujer"],
                            "allowed_fabrics": ["poliester", "lana"],
                            "brands": {
                                "Ralph Lauren":   (400, 1200),
                                "Calvin Klein":   (300, 900),
                                "Tommy Hilfiger": (280, 800),
                                "Brooks Brothers":(350, 1000),
                                "Hugo Boss":      (400, 1100),
                                "Armani":         (700, 2000),
                            }
                        },
                        "sweater": {
                            "styles": ["casual", "minimalist", "cozy"],
                            "fit": ["regular", "oversize"],
                            "usage": ["winter", "daily", "casual"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["lana", "algodon", "fleece"],
                            "brands": {
                                "Ralph Lauren":   (80,  220),
                                "Uniqlo":         (30,  80),
                                "J.Crew":         (60,  150),
                                "Zara":           (35,  90),
                                "H&M":            (20,  55),
                                "Banana Republic":(70,  180),
                                "Carhartt":       (60,  140),
                            }
                        },
                        "polo": {
                            "styles": ["casual", "smart casual", "sport"],
                            "fit": ["slim", "regular"],
                            "usage": ["golf", "daily", "office"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester"],
                            "brands": {
                                "Ralph Lauren": (80,  200),
                                "Lacoste":      (90,  180),
                                "Tommy Hilfiger":(60, 150),
                                "Nike":         (40,  90),
                                "Adidas":       (40,  85),
                                "Uniqlo":       (25,  60),
                                "J.Crew":       (50,  110),
                            }
                        },
                        "henley_shirt": {
                            "styles": ["casual", "minimalist"],
                            "fit": ["slim", "regular"],
                            "usage": ["daily", "casual"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "rayon"],
                            "brands": {
                                "H&M":       (10, 30),
                                "Uniqlo":    (15, 40),
                                "Zara":      (18, 45),
                                "J.Crew":    (30, 75),
                                "ASOS":      (12, 35),
                                "Gap":       (20, 55),
                            }
                        },
                        "vneck_shirt": {
                            "styles": ["casual", "minimalist"],
                            "fit": ["slim", "regular"],
                            "usage": ["daily", "casual"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "rayon", "poliester"],
                            "brands": {
                                "H&M":    (8,  25),
                                "Uniqlo": (12, 30),
                                "Zara":   (15, 38),
                                "Gap":    (18, 45),
                                "ASOS":   (10, 28),
                            }
                        },
                        "tube_top": {
                            "styles": ["party", "summer", "streetwear"],
                            "fit": ["slim"],
                            "usage": ["summer", "party", "casual"],
                            "allowed_genders": ["mujer"],
                            "allowed_fabrics": ["algodon", "spandex", "rayon"],
                            "brands": {
                                "Zara":          (15, 45),
                                "H&M":           (8,  25),
                                "ASOS":          (10, 30),
                                "Fashion Nova":  (10, 35),
                                "PrettyLittleThing": (8, 28),
                                "Free People":   (35, 80),
                            }
                        },
                        "sports_bra": {
                            "styles": ["sport", "activewear"],
                            "fit": ["compression", "slim"],
                            "usage": ["gym", "running", "training"],
                            "allowed_genders": ["mujer"],
                            "allowed_fabrics": ["spandex", "poliester"],
                            "brands": {
                                "Nike":         (30, 75),
                                "Adidas":       (28, 70),
                                "Gymshark":     (30, 65),
                                "Under Armour": (25, 65),
                                "Lululemon":    (45, 95),
                                "Alo Yoga":     (50, 100),
                            }
                        },
                    },
                    "age_group": ["niño", "juvenil", "adulto joven", "adulto mayor"],
                    "colors": ["blanco", "negro", "gris", "azul", "celeste", "rojo",
                            "verde", "amarillo", "morado", "rosado", "beige", "cafe"],
                    "tags": {
                        "formal":     ["oficina", "elegante", "boda", "graduacion"],
                        "casual":     ["diario", "comodo", "relajado"],
                        "streetwear": ["urbano", "oversize", "moderno"],
                        "sport":      ["gym", "running", "training"],
                        "minimalist": ["simple", "clean", "neutral"],
                        "luxury":     ["premium", "sofisticado"],
                        "cozy":       ["suave", "caliente"],
                        "summer":     ["fresco", "ligero"],
                        "winter":     ["abrigado", "termico"]
                    }
                },

                "bottoms": {
                    "subcategories": {
                        "jeans": {
                            "styles": ["casual", "streetwear"],
                            "fit": ["slim", "regular", "baggy"],
                            "usage": ["daily", "casual"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["denim"],
                            "brands": {
                                "Levi's":        (40,  120),
                                "Wrangler":      (30,  80),
                                "Lee":           (30,  75),
                                "Calvin Klein":  (60,  140),
                                "Tommy Hilfiger":(55,  130),
                                "Zara":          (30,  80),
                                "H&M":           (20,  55),
                                "Gap":           (35,  90),
                            }
                        },
                        "joggers": {
                            "styles": ["sport", "streetwear", "casual"],
                            "fit": ["slim", "regular", "oversize"],
                            "usage": ["gym", "casual", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester", "fleece"],
                            "brands": {
                                "Nike":          (45, 100),
                                "Adidas":        (45, 95),
                                "Under Armour":  (40, 90),
                                "Champion":      (30, 70),
                                "H&M":           (15, 40),
                                "Gymshark":      (40, 85),
                                "Puma":          (35, 80),
                            }
                        },
                        "shorts": {
                            "styles": ["casual", "sport", "summer"],
                            "fit": ["slim", "regular"],
                            "usage": ["summer", "daily", "gym"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester", "denim"],
                            "brands": {
                                "Nike":      (28, 65),
                                "Adidas":    (28, 60),
                                "Levi's":    (30, 70),
                                "H&M":       (10, 30),
                                "Zara":      (15, 40),
                                "Gymshark":  (30, 65),
                                "Puma":      (25, 55),
                            }
                        },
                        "cargo_pants": {
                            "styles": ["streetwear", "utility", "casual"],
                            "fit": ["regular", "baggy"],
                            "usage": ["casual", "outdoor"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "poliester"],
                            "brands": {
                                "Carhartt":  (55, 130),
                                "Dickies":   (35, 80),
                                "Zara":      (35, 85),
                                "H&M":       (20, 50),
                                "Columbia":  (60, 140),
                                "ASOS":      (25, 60),
                                "Stussy":    (70, 150),
                            }
                        },
                        "dress_pants": {
                            "styles": ["formal", "business casual"],
                            "fit": ["slim", "tailored", "regular"],
                            "usage": ["office", "formal events"],
                            "allowed_genders": ["hombre", "mujer"],
                            "allowed_fabrics": ["lana", "poliester"],
                            "brands": {
                                "Hugo Boss":      (120, 350),
                                "Calvin Klein":   (80,  220),
                                "Ralph Lauren":   (100, 300),
                                "Brooks Brothers":(110, 280),
                                "Banana Republic":(80,  200),
                                "Zara":           (40,  100),
                                "H&M":            (25,  70),
                            }
                        },
                        "leggings": {
                            "styles": ["sport", "activewear"],
                            "fit": ["compression", "slim"],
                            "usage": ["gym", "yoga", "running"],
                            "allowed_genders": ["mujer"],
                            "allowed_fabrics": ["spandex", "poliester"],
                            "brands": {
                                "Lululemon":    (60, 130),
                                "Gymshark":     (40, 85),
                                "Nike":         (40, 90),
                                "Adidas":       (35, 85),
                                "Alo Yoga":     (65, 130),
                                "Under Armour": (35, 80),
                                "Zara":         (20, 50),
                            }
                        },
                        "skirt": {
                            "styles": ["casual", "formal", "streetwear"],
                            "fit": ["slim", "regular"],
                            "usage": ["daily", "office", "party"],
                            "allowed_genders": ["mujer"],
                            "allowed_fabrics": ["algodon", "lana", "rayon", "poliester"],
                            "brands": {
                                "Zara":        (25, 75),
                                "H&M":         (15, 45),
                                "ASOS":        (18, 55),
                                "Free People": (50, 130),
                                "Anthropologie":(60, 160),
                                "Mango":       (30, 80),
                                "Banana Republic":(55, 140),
                            }
                        },
                        "sweatpants": {
                            "styles": ["casual", "sport", "cozy"],
                            "fit": ["regular", "oversize"],
                            "usage": ["home", "gym", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon", "fleece", "poliester"],
                            "brands": {
                                "Nike":      (50, 110),
                                "Adidas":    (45, 100),
                                "Champion":  (30, 75),
                                "H&M":       (18, 45),
                                "Carhartt":  (55, 120),
                                "Puma":      (35, 80),
                                "Gap":       (30, 70),
                            }
                        },
                        "chinos": {
                            "styles": ["smart casual", "business casual"],
                            "fit": ["slim", "regular"],
                            "usage": ["office", "daily"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["algodon"],
                            "brands": {
                                "Ralph Lauren":   (70,  180),
                                "J.Crew":         (60,  150),
                                "Banana Republic":(65,  160),
                                "Gap":            (40,  90),
                                "Zara":           (35,  85),
                                "H&M":            (20,  55),
                                "Dockers":        (40,  90),
                            }
                        },
                        "track_pants": {
                            "styles": ["sport", "streetwear"],
                            "fit": ["regular", "slim"],
                            "usage": ["training", "running", "gym"],
                            "allowed_genders": ["hombre", "mujer", "unisex"],
                            "allowed_fabrics": ["poliester", "spandex"],
                            "brands": {
                                "Nike":         (55, 110),
                                "Adidas":       (55, 105),
                                "Puma":         (45, 95),
                                "Under Armour": (45, 100),
                                "Gymshark":     (45, 90),
                                "Fila":         (35, 75),
                            }
                        },
                    },
                    "age_group": ["niño", "juvenil", "adulto joven", "adulto mayor"],
                    "colors": ["negro", "gris", "azul", "celeste", "beige", "verde", "blanco", "cafe"],
                    "tags": {
                        "formal":     ["oficina", "elegante"],
                        "casual":     ["diario", "comodo"],
                        "streetwear": ["urbano", "baggy"],
                        "sport":      ["gym", "running", "training"],
                        "summer":     ["fresco", "ligero"],
                        "cozy":       ["suave", "relajado"],
                        "utility":    ["bolsillos", "outdoor"]
                    }
                }
            }

def init_db(DB_PATH):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    #PRODUCTOS
    tabla_productos = """CREATE TABLE IF NOT EXISTS productos(
        producto_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50), 
        categoria_id INT, 
        subcategoria_id INT, 
        age_group VARCHAR(50) NOT NULL, 
        genero VARCHAR(50) NOT NULL, 
        tipo_tela VARCHAR(50) NOT NULL, 
        color VARCHAR(50) NOT NULL, 
        estilo VARCHAR(50) NOT NULL, 
        fit VARCHAR(50) NOT NULL, 
        uso VARCHAR(50) NOT NULL, 
        descripcion VARCHAR(100), 
        tags VARCHAR(100), 
        marca_id INT NOT NULL, 
        price FLOAT(3),
        proveedor_id INT,
        FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id),
        FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(subcategoria_id),
        FOREIGN KEY (marca_id) REFERENCES marcas(marca_id),
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(proveedor_id)
        );"""

    #CLIENTES
    tabla_clientes = """
    CREATE TABLE IF NOT EXISTS clientes(
        cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(30) NOT NULL,
        apellido VARCHAR(30) NOT NULL,
        email VARCHAR(30) NOT NULL,
        telefono VARCHAR(40) NOT NULL,
        fecha_registro DATE NOT NULL
    );

    """

    #VENTAS
    tabla_ventas = """
    CREATE TABLE IF NOT EXISTS ventas(
        venta_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INT NOT NULL,
        fecha DATE NOT NULL,
        total FLOAT(4) NOT NULL,
        estado VARCHAR(30) NOT NULL,
        metodo_pago_id INT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
        FOREIGN KEY (metodo_pago_id) REFERENCES metodo_pago(metodo_id)
    );

    """

    #DETALLE VENTA
    tabla_detalle_ventas = """
    CREATE TABLE IF NOT EXISTS detalle_ventas(
        detalle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INT NOT NULL,
        producto_id INT NOT NULL,
        cantidad INT NOT NULL,
        precio_unitario FLOAT(3) NOT NULL,
        subtotal FLOAT(3),
        FOREIGN KEY (venta_id) REFERENCES ventas(venta_id),
        FOREIGN KEY (producto_id) REFERENCES productos(producto_id)

    );


    """

    #METODOS DE PAGO
    tabla_metodo_pago = """
    CREATE TABLE IF NOT EXISTS metodo_pago(
        metodo_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        metodo VARCHAR(30)
    );
    """

    #SUBCATEGORIAS PRODUCTOS
    tabla_categorias = """CREATE TABLE IF NOT EXISTS categorias(
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria VARCHAR(30));"""

    #SUBCATEGORIAS
    tabla_subcategorias = """
    CREATE TABLE IF NOT EXISTS subcategorias(
    subcategoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcategoria VARCHAR(30),
    categoria_id INT NOT NULL,

    FOREIGN KEY (categoria_id)
    REFERENCES categorias(categoria_id));
    """

    #MARCAS
    tabla_marcas = """
    CREATE TABLE IF NOT EXISTS marcas(
        marca_id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca VARCHAR(30));
    """

    #INVENTARIO
    tabla_inventario = """
    CREATE TABLE IF NOT EXISTS inventario(
        inventario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INT,
        cantidad INT,
        FOREIGN KEY (producto_id) REFERENCES productos(producto_id));
    """

    #DIRECCIONES
    tabla_direcciones = """
    CREATE TABLE IF NOT EXISTS direcciones(
        direccion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        direccion VARCHAR(60),
        cliente_id INT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    );
    """

    #ENVIO
    tabla_envios = """
    CREATE TABLE IF NOT EXISTS envios(
        envios_id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INT,
        fecha_envio DATE,
        fecha_entrega DATE,
        estado VARCHAR(30),
        direccion_id INT,
        FOREIGN KEY (venta_id) REFERENCES ventas(venta_id),
        FOREIGN KEY (direccion_id) REFERENCES direcciones(direccion_id));
    """

    #Empleados
    tabla_empleados = """
    CREATE TABLE IF NOT EXISTS empleados(
        empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(30) NOT NULL,
        apellido VARCHAR(30) NOT NULL,
        email VARCHAR(50),
        cargo VARCHAR(30),
        fecha_contratacion DATE
    );
    """

    #Proveedor
    tabla_proveedores = """
    CREATE TABLE IF NOT EXISTS proveedores(
        proveedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(50) NOT NULL,
        telefono VARCHAR(20),
        email VARCHAR(50)
    );
    """

    cursor.execute(tabla_productos)
    cursor.execute(tabla_clientes)
    cursor.execute(tabla_ventas)
    cursor.execute(tabla_detalle_ventas)
    cursor.execute(tabla_metodo_pago)
    cursor.execute(tabla_categorias)
    cursor.execute(tabla_subcategorias)
    cursor.execute(tabla_marcas)
    cursor.execute(tabla_inventario)
    cursor.execute(tabla_direcciones)
    cursor.execute(tabla_envios)
    cursor.execute(tabla_empleados)
    cursor.execute(tabla_proveedores)

def delete_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #cursor.execute("DROP TABLE productos;")
    cursor.execute("DROP TABLE categorias;")
    cursor.execute("DROP TABLE subcategorias;")
    cursor.execute("DROP TABLE marcas;")
    cursor.execute("DROP TABLE proveedores;")
    cursor.execute("DROP TABLE empleados;")
    cursor.execute("DROP TABLE clientes;")
    cursor.execute("DROP TABLE ventas;")
    cursor.execute("DROP TABLE detalle_ventas;")
    cursor.execute("DROP TABLE metodo_pago;")
    cursor.execute("DROP TABLE inventario;")
    cursor.execute("DROP TABLE direcciones;")
    cursor.execute("DROP TABLE envios;")
    conn.commit()

def insert_data(DB_PATH):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(
        "datos_tienda.json",
        "r",
        encoding="utf-8"
        ) as f:

        datos = json.load(f)

    # ==========================
    # METODOS DE PAGO
    # ==========================

    for metodo in datos["metodos_pago"]:

        cursor.execute(
            """
            INSERT INTO metodo_pago(
                metodo_id,
                metodo
            )
            VALUES (?, ?)
            """,
            (
                metodo["metodo_id"],
                metodo["metodo"]
            )
        )

    # ==========================
    # CLIENTES
    # ==========================

    for cliente in datos["clientes"]:

        cursor.execute(
            """
            INSERT INTO clientes(
                nombre,
                apellido,
                email,
                telefono,
                fecha_registro
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                cliente["nombre"],
                cliente["apellido"],
                cliente["email"],
                cliente["telefono"],
                cliente["fecha_registro"]
            )
        )

    # ==========================
    # DIRECCIONES
    # ==========================

    for direccion in datos["direcciones"]:

        cursor.execute(
            """
            INSERT INTO direcciones(
                direccion_id,
                direccion,
                cliente_id
            )
            VALUES (?, ?, ?)
            """,
            (
                direccion["direccion_id"],
                direccion["direccion"],
                direccion["cliente_id"]
            )
        )

    # ==========================
    # EMPLEADOS
    # ==========================

    for empleado in datos["empleados"]:

        cursor.execute(
            """
            INSERT INTO empleados(
                nombre,
                apellido,
                email,
                cargo,
                fecha_contratacion
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                empleado["nombre"],
                empleado["apellido"],
                empleado["email"],
                empleado["cargo"],
                empleado["fecha_contratacion"]
            )
        )

    # ==========================
    # PROVEEDORES
    # ==========================

    for proveedor in datos["proveedores"]:

        cursor.execute(
            """
            INSERT INTO proveedores(
                nombre,
                telefono,
                email
            )
            VALUES (?, ?, ?)
            """,
            (
                proveedor["nombre"],
                proveedor["telefono"],
                proveedor["email"]
            )
        )

    
        # =====================================================
    # INVENTARIO
    # =====================================================

    cursor.execute("""
        SELECT producto_id
        FROM productos
    """)

    productos_ids = cursor.fetchall()

    for producto_id, in productos_ids:

        cursor.execute(
            """
            INSERT INTO inventario(
                producto_id,
                cantidad
            )
            VALUES (?, ?)
            """,
            (
                producto_id,
                random.randint(10, 200)
            )
        )

    # =====================================================
    # OBTENER PRODUCTOS REALES
    # =====================================================

    cursor.execute("""
        SELECT producto_id, price
        FROM productos
    """)

    productos = cursor.fetchall()

    # =====================================================
    # OBTENER CLIENTES
    # =====================================================

    cursor.execute("""
        SELECT cliente_id
        FROM clientes
    """)

    clientes = [row[0] for row in cursor.fetchall()]

    # =====================================================
    # OBTENER DIRECCIONES
    # =====================================================

    cursor.execute("""
        SELECT direccion_id, cliente_id
        FROM direcciones
    """)

    direcciones = cursor.fetchall()

    direcciones_por_cliente = {}

    for direccion_id, cliente_id in direcciones:

        if cliente_id not in direcciones_por_cliente:
            direcciones_por_cliente[cliente_id] = []

        direcciones_por_cliente[cliente_id].append(
            direccion_id
        )

    # =====================================================
    # GENERAR VENTAS + DETALLE_VENTAS + ENVIOS
    # =====================================================

    detalle_id = 1
    envio_id = 1

    for venta_id in range(1, 201):

        cliente_id = random.choice(clientes)

        fecha_compra = (
            datetime.now()
            - timedelta(days=random.randint(0, 365))
        )

        estado_venta = random.choice([
            "Pendiente",
            "Procesando",
            "Enviado",
            "Entregado"
        ])

        metodo_pago_id = random.randint(1, 3)

        total_venta = 0

        detalles = []

        cantidad_items = random.randint(1, 5)

        for _ in range(cantidad_items):

            producto_id, precio = random.choice(
                productos
            )

            cantidad = random.randint(1, 3)

            subtotal = round(
                precio * cantidad,
                2
            )

            total_venta += subtotal

            detalles.append(
                (
                    detalle_id,
                    venta_id,
                    producto_id,
                    cantidad,
                    precio,
                    subtotal
                )
            )

            detalle_id += 1

        # =====================
        # INSERTAR VENTA
        # =====================

        cursor.execute(
            """
            INSERT INTO ventas(
                venta_id,
                cliente_id,
                fecha,
                total,
                estado,
                metodo_pago_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                venta_id,
                cliente_id,
                fecha_compra.strftime("%Y-%m-%d"),
                round(total_venta, 2),
                estado_venta,
                metodo_pago_id
            )
        )

        # =====================
        # INSERTAR DETALLES
        # =====================

        for detalle in detalles:

            cursor.execute(
                """
                INSERT INTO detalle_ventas(
                    detalle_id,
                    venta_id,
                    producto_id,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                detalle
            )

        # =====================
        # GENERAR ENVIO
        # =====================

        direccion_id = random.choice(
            direcciones_por_cliente[cliente_id]
        )

        fecha_envio = fecha_compra + timedelta(
            days=random.randint(1, 3)
        )

        fecha_entrega = fecha_envio + timedelta(
            days=random.randint(2, 7)
        )

        estado_envio = random.choice([
            "Preparando",
            "En tránsito",
            "Entregado"
        ])

        cursor.execute(
            """
            INSERT INTO envios(
                envios_id,
                venta_id,
                fecha_envio,
                fecha_entrega,
                estado,
                direccion_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                envio_id,
                venta_id,
                fecha_envio.strftime("%Y-%m-%d"),
                fecha_entrega.strftime("%Y-%m-%d"),
                estado_envio,
                direccion_id
            )
        )

        envio_id += 1
    

    # ==========================
    # GUARDAR
    # ==========================

    conn.commit()

    print("Datos insertados correctamente.")

    conn.close()

def poblar_catalogo(categories):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # =====================
    # CATEGORIAS
    # =====================

    categoria_ids = {}

    for categoria in categories.keys():

        cursor.execute(
            """
            INSERT INTO categorias(categoria)
            VALUES(?)
            """,
            (categoria,)
        )

        categoria_ids[categoria] = cursor.lastrowid

    # =====================
    # SUBCATEGORIAS
    # =====================

    for categoria, categoria_data in categories.items():

        categoria_id = categoria_ids[categoria]

        for subcategoria in categoria_data["subcategories"].keys():

            cursor.execute(
                """
                INSERT INTO subcategorias(
                    subcategoria,
                    categoria_id
                )
                VALUES (?, ?)
                """,
                (
                    subcategoria,
                    categoria_id
                )
            )

    # =====================
    # MARCAS
    # =====================

    marcas = set()

    for categoria_data in categories.values():

        for subcategoria_data in categoria_data["subcategories"].values():

            for marca in subcategoria_data["brands"].keys():

                marcas.add(marca)

    for marca in sorted(marcas):

        cursor.execute(
            """
            INSERT INTO marcas(marca)
            VALUES(?)
            """,
            (marca,)
        )

    conn.commit()

    print(
        f"Categorías: {len(categoria_ids)} | "
        f"Subcategorías: {sum(len(c['subcategories']) for c in categories.values())} | "
        f"Marcas: {len(marcas)}"
    )

def insert_products(categories, cantidad=100):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # ==========================
    # CARGAR IDS DE CATEGORIAS
    # ==========================

    cursor.execute("""
        SELECT categoria_id, categoria
        FROM categorias
    """)

    categorias_db = {
        nombre: categoria_id
        for categoria_id, nombre in cursor.fetchall()
    }

    # ==========================
    # CARGAR IDS DE SUBCATEGORIAS
    # ==========================

    cursor.execute("""
        SELECT subcategoria_id, subcategoria
        FROM subcategorias
    """)

    subcategorias_db = {
        nombre: subcategoria_id
        for subcategoria_id, nombre in cursor.fetchall()
    }

    # ==========================
    # CARGAR IDS DE MARCAS
    # ==========================

    cursor.execute("""
        SELECT marca_id, marca
        FROM marcas
    """)

    marcas_db = {
        nombre: marca_id
        for marca_id, nombre in cursor.fetchall()
    }

    # ==========================
    # CARGAR PROVEEDORES
    # ==========================

    cursor.execute("""
        SELECT proveedor_id
        FROM proveedores
    """)

    proveedores = [
        row[0]
        for row in cursor.fetchall()
    ]

    if not proveedores:
        raise Exception(
            "No hay proveedores registrados."
        )

    # ==========================
    # GENERAR PRODUCTOS
    # ==========================

    for _ in range(cantidad):

        item = generate_item(categories)

        complex_str = generate_complex_strings(item)

        item["name"] = complex_str["name"]
        item["tags"] = str(complex_str["tags"])
        item["description"] = complex_str["description"]

        categoria_id = categorias_db[item["category"]]

        subcategoria_id = subcategorias_db[
            item["subcategory"]
        ]

        marca_id = marcas_db[
            item["brand"]
        ]

        proveedor_id = random.choice(
            proveedores
        )

        cursor.execute(
            """
            INSERT INTO productos(
                name,
                categoria_id,
                subcategoria_id,
                age_group,
                genero,
                tipo_tela,
                color,
                estilo,
                fit,
                uso,
                descripcion,
                tags,
                marca_id,
                price,
                proveedor_id
            )
            VALUES(
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?,?,?
            )
            """,
            (
                item["name"],
                categoria_id,
                subcategoria_id,
                item["age_group"],
                item["gender"],
                item["fabric"],
                item["color"],
                item["style"],
                item["fit"],
                item["usage"],
                item["description"],
                item["tags"],
                marca_id,
                item["price"],
                proveedor_id
            )
        )

    conn.commit()

    print(
        f"{cantidad} productos insertados correctamente."
    )

def show_data(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos where producto_id = 70;")
    
    
    rows = cursor.fetchall()
    print(rows)
    conn.close()

def export():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tablas = [
        "categorias",
        "subcategorias",
        "marcas",
        "proveedores",
        "clientes",
        "direcciones",
        "empleados",
        "productos",
        "inventario",
        "metodo_pago",
        "ventas",
        "detalle_ventas",
        "envios"
    ]

    for tabla in tablas:
        df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
        df.to_csv(f"{tabla}.csv", index=False)

    conn.close()


show_data(DB_PATH)
export()
#delete_db(DB_PATH)
#init_db(DB_PATH)
#insert_data(DB_PATH)
#poblar_catalogo(categories)

#insert_products(categories, 100)

