import sqlite3
import os
import random
from app.database.sample_generator import generate_complex_strings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def main():
    delete_db(DB_PATH)
    init_db(DB_PATH)

def init_db(DB_PATH):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_table(cursor, conn)
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

    insert_data(categories, cursor, conn)
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    conn.close()

def delete_db(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE products;")
    conn.commit()

def generate_item(categories):
    category = random.choice(list(categories.keys()))
    subcat_key = random.choice(list(categories[category]["subcategories"].keys()))
    subcat = categories[category]["subcategories"][subcat_key]

    gender  = random.choice(subcat["allowed_genders"])   
    fabric  = random.choice(subcat["allowed_fabrics"])   
    style   = random.choice(subcat["styles"])
    fit     = random.choice(subcat["fit"])
    usage   = random.choice(subcat["usage"])
    brand = random.choice(list(subcat["brands"].keys()))
    price_range = subcat["brands"][brand]
    price = random.randrange(price_range[0], price_range[1])
    age_group = random.choice(categories[category]["age_group"])
    color   = random.choice(categories[category]["colors"])


   
    return {"name":None,
        "category": category,
        "subcategory": subcat_key,
        "age_group": age_group,
        "gender": gender,
            "fabric":fabric,
            "color": color,
            "style": style,
            "fit": fit,
            "usage": usage,
            "description": None,
            "tags": None,
            "brand": brand,
            "price": price}

def create_table(cursor, conn):
    cursor.execute("""CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50), 
    category VARCHAR(50) NOT NULL, 
    subcategory VARCHAR(50) NOT NULL, 
    age_group VARCHAR(50) NOT NULL, 
    gender VARCHAR(50) NOT NULL, 
    fabric VARCHAR(50) NOT NULL, 
    color VARCHAR(50) NOT NULL, 
    style VARCHAR(50) NOT NULL, 
    fit VARCHAR(50) NOT NULL, 
    usage VARCHAR(50) NOT NULL, 
    description VARCHAR(100), 
    tags VARCHAR(100), 
    brand VARCHAR(50), 
    price FLOAT(3))""")

    conn.commit()

def insert_data(categories, cursor, conn):
    for _ in range (0,2):
        item = generate_item(categories)
        complex_str = generate_complex_strings(item)
        name, tags, description = complex_str["name"], str(complex_str["tags"]), complex_str["description"]
        item["name"], item["tags"], item["description"] = name, tags, description
        cursor.execute("""INSERT INTO products(name,category,
        subcategory,
        age_group,
        gender,
        fabric,
        color,
            style,
            fit,
            usage,
            description,
            tags,
                brand,
                price) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
        (item["name"],
        item["category"],
        item["subcategory"],
        item["age_group"],
        item["gender"],
        item["fabric"],
        item["color"],
        item["style"],
        item["fit"],
        item["usage"],
        item["description"],
        item["tags"],
        item["brand"],
        item["price"]))


    conn.commit()

def add_price(item):
    return item

if __name__ == "__main__":
    main()










