import sqlite3
from app.database.connection import get_connection


def map_product(row):
    return {
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "category": row[3],
        "brand": row[4]
    }

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    conn.close()

    products = []
    for row in rows:
        product = map_product(row)
        products.append(product)
    return products
    
def get_one_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        product = map_product(row)
        return product
    return None

def get_products_id(ids:list):
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join(("?") * len(ids))
    cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})",
                    ids)
    recomm = cursor.fetchall()
    
    conn.close()

    return [
    map_product(row)
    for row in recomm
    ]

def delete_product_r(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()

    conn.close()

    return True

def new_product_r(product):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO products (name, price, category, brand) VALUES (?,?,?,?)",
                    (product.name, product.price, product.category, product.brand))
    conn.commit()

    new_id = cursor.lastrowid
    conn.close()

    
    new_product = {
        "id" : new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "brand": product.brand
    }

    return new_product

def update_product_r(product_id, updated_product):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None
    

    cursor.execute("UPDATE products SET name = ?, price = ?, category = ?, brand = ? WHERE id = ?",
                    (updated_product.name,
                     updated_product.price,
                     updated_product.category,
                     updated_product.brand,
                     product_id))
    
    conn.commit()
    conn.close()

    return {
        "id" : product_id,
        "name" : updated_product.name,
        "price" : updated_product.price,
        "category": updated_product.category,
        "brand": updated_product.brand
    }

