import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


print(DB_PATH)
print(os.getcwd())


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Añadir agegroup, fit, gender, color, style, usage, subcategoria, fabric, tags, description


categories = {
    "tops": {
        "subcategories": {
            "tshirt": {
                "styles": ["casual", "streetwear", "sport", "minimalist"],
                "fit": ["slim", "regular", "oversize"],
                "usage": ["daily", "casual", "gym"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester", "rayon", "spandex"]
            },
            "shirt": {
                "styles": ["formal", "casual", "business casual"],
                "fit": ["slim", "regular"],
                "usage": ["office", "formal events", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "lino", "rayon"]
            },
            "tank_top": {
                "styles": ["casual", "sport", "streetwear"],
                "fit": ["slim", "regular"],
                "usage": ["gym", "summer", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester", "rayon", "spandex"]
            },
            "sweatshirt": {
                "styles": ["casual", "streetwear", "sport"],
                "fit": ["regular", "oversize"],
                "usage": ["casual", "winter", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "fleece", "poliester"]
            },
            "turtleneck": {
                "styles": ["elegant", "minimalist", "formal"],
                "fit": ["slim", "regular"],
                "usage": ["winter", "office", "formal events"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["lana", "algodon", "rayon"]
            },
            "tuxedo": {
                "styles": ["luxury", "formal", "elegant"],
                "fit": ["slim", "tailored"],
                "usage": ["wedding", "gala", "formal events"],
                "allowed_genders": ["hombre", "mujer"],
                "allowed_fabrics": ["poliester", "lana"]
            },
            "sweater": {
                "styles": ["casual", "minimalist", "cozy"],
                "fit": ["regular", "oversize"],
                "usage": ["winter", "daily", "casual"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["lana", "algodon", "fleece"]
            },
            "polo": {
                "styles": ["casual", "smart casual", "sport"],
                "fit": ["slim", "regular"],
                "usage": ["golf", "daily", "office"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester"]
            },
            "henley_shirt": {
                "styles": ["casual", "minimalist"],
                "fit": ["slim", "regular"],
                "usage": ["daily", "casual"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "rayon"]
            },
            "vneck_shirt": {
                "styles": ["casual", "minimalist"],
                "fit": ["slim", "regular"],
                "usage": ["daily", "casual"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "rayon", "poliester"]
            },
            "tube_top": {
                "styles": ["party", "summer", "streetwear"],
                "fit": ["slim"],
                "usage": ["summer", "party", "casual"],
                "allowed_genders": ["mujer"],
                "allowed_fabrics": ["algodon", "spandex", "rayon"]
            },
            "sports_bra": {
                "styles": ["sport", "activewear"],
                "fit": ["compression", "slim"],
                "usage": ["gym", "running", "training"],
                "allowed_genders": ["mujer"],
                "allowed_fabrics": ["spandex", "poliester"]
            }
        },
        "age_group": ["niño", "juvenil", "adulto joven", "adulto mayor"],
        "tags": {
            "formal": ["oficina", "elegante", "boda", "graduacion"],
            "casual": ["diario", "comodo", "relajado"],
            "streetwear": ["urbano", "oversize", "moderno"],
            "sport": ["gym", "running", "training"],
            "minimalist": ["simple", "clean", "neutral"],
            "luxury": ["premium", "sofisticado"],
            "cozy": ["suave", "caliente"],
            "summer": ["fresco", "ligero"],
            "winter": ["abrigado", "termico"]
        },
        "colors": ["blanco", "negro", "gris", "azul", "celeste", "rojo",
                   "verde", "amarillo", "morado", "rosado", "beige", "cafe"]
    },

    "bottoms": {
        "subcategories": {
            "jeans": {
                "styles": ["casual", "streetwear"],
                "fit": ["slim", "regular", "baggy"],
                "usage": ["daily", "casual"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["denim"]  # jeans → solo denim
            },
            "joggers": {
                "styles": ["sport", "streetwear", "casual"],
                "fit": ["slim", "regular", "oversize"],
                "usage": ["gym", "casual", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester", "fleece"]
            },
            "shorts": {
                "styles": ["casual", "sport", "summer"],
                "fit": ["slim", "regular"],
                "usage": ["summer", "daily", "gym"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester", "denim"]
            },
            "cargo_pants": {
                "styles": ["streetwear", "utility", "casual"],
                "fit": ["regular", "baggy"],
                "usage": ["casual", "outdoor"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "poliester"]
            },
            "dress_pants": {
                "styles": ["formal", "business casual"],
                "fit": ["slim", "tailored", "regular"],
                "usage": ["office", "formal events"],
                "allowed_genders": ["hombre", "mujer"],
                "allowed_fabrics": ["lana", "poliester"]
            },
            "leggings": {
                "styles": ["sport", "activewear"],
                "fit": ["compression", "slim"],
                "usage": ["gym", "yoga", "running"],
                "allowed_genders": ["mujer"],
                "allowed_fabrics": ["spandex", "poliester"]
            },
            "skirt": {
                "styles": ["casual", "formal", "streetwear"],
                "fit": ["slim", "regular"],
                "usage": ["daily", "office", "party"],
                "allowed_genders": ["mujer"],
                "allowed_fabrics": ["algodon", "lana", "rayon", "poliester"]  # no denim, no spandex
            },
            "sweatpants": {
                "styles": ["casual", "sport", "cozy"],
                "fit": ["regular", "oversize"],
                "usage": ["home", "gym", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon", "fleece", "poliester"]
            },
            "chinos": {
                "styles": ["smart casual", "business casual"],
                "fit": ["slim", "regular"],
                "usage": ["office", "daily"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["algodon"]  # chinos → solo algodón/gabardina
            },
            "track_pants": {
                "styles": ["sport", "streetwear"],
                "fit": ["regular", "slim"],
                "usage": ["training", "running", "gym"],
                "allowed_genders": ["hombre", "mujer", "unisex"],
                "allowed_fabrics": ["poliester", "spandex"]
            }
        },
        "age_group": ["niño", "juvenil", "adulto joven", "adulto mayor"],
        "tags": {
            "formal": ["oficina", "elegante"],
            "casual": ["diario", "comodo"],
            "streetwear": ["urbano", "baggy"],
            "sport": ["gym", "running", "training"],
            "summer": ["fresco", "ligero"],
            "cozy": ["suave", "relajado"],
            "utility": ["bolsillos", "outdoor"]
        },
        "colors": ["negro", "gris", "azul", "celeste", "beige",
                   "verde", "blanco", "cafe"]
    }
}


def generate_item(categories):
    category = random.choice(list(categories.keys()))
    subcat_key = random.choice(list(categories[category]["subcategories"].keys()))
    subcat = categories[category]["subcategories"][subcat_key]

    gender  = random.choice(subcat["allowed_genders"])   
    fabric  = random.choice(subcat["allowed_fabrics"])   
    style   = random.choice(subcat["styles"])
    fit     = random.choice(subcat["fit"])
    usage   = random.choice(subcat["usage"])
    age_group = random.choice(categories[category]["age_group"])
    color   = random.choice(categories[category]["colors"])

    return [None, category, subcat_key, age_group, gender, fabric, color, style, fit, usage]


items = []
for i in range (0,100):
    item = generate_item(categories)
    items.append(item)

print(items)
def add_price(item):
    return item


"""
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 25, "Ropa", "Adidas"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 55, "Ropa", "Gucci"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 27, "Ropa", "Adidas"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 30, "Ropa", "Puma"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Pantalón", 42, "Ropa", "Adidas"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Pantalón", 45, "Ropa", "Puma"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Pantalón", 60, "Ropa", "Gucci"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Faja", 7, "Accesory", "Adidas"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Faja", 5, "Accesory", "Adidas"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Faja", 10, "Accesory", "Gucci"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 28, "Ropa", "Columbia"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 33, "Ropa", "Columbia"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Faja", 6, "Accesory", "Reebok"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Camisa", 25, "Ropa", "Reebok"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Ropa", 50, "Camisa", "Balenciaga"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Faja", 12, "Accesory", "Balenciaga"))
cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                ("Pantalón", 65, "Ropa", "Balenciaga"))


conn.commit()





cursor.execute("SELECT * FROM products;")
rows = cursor.fetchall()
"""

# Añadir agegroup, gender, color, style, usage, subcategoria, fabric, tags, description
conn.close()




