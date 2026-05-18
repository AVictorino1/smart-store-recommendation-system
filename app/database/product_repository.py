import sqlite3
from app.database.connection import get_connection
from app.database.init_db import generate_item
from app.models import Product, ProductUpdate

def map_product(row):
    return dict(row)

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

def new_product_r(product: Product):
    conn = get_connection()
    cursor = conn.cursor()

    product_dict = product.model_dump()

    columns = ", ".join(product_dict.keys())
    placeholders = ", ".join("?" * len(product_dict)) 

    values = tuple(product_dict.values())
    cursor.execute(f"""INSERT INTO products ({columns}) VALUES ({placeholders})""",
                    (values))
    conn.commit()

    new_id = cursor.lastrowid
    new_product = get_one_product(new_id)
    conn.close()

    

    return new_product

def update_product_r(product_id, updated_product: ProductUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None
    
    product_dict = updated_product.model_dump()

    columns = ", ".join([f"{column} = ? "for column in product_dict.keys()])
    values = tuple(product_dict.values())
    
    query = f"""UPDATE products SET {columns} WHERE id = ?"""
    cursor.execute(query, (values + (product_id, )))
    

    conn.commit()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    updated = cursor.fetchone()

    conn.close()

    return map_product(updated)

def update_product_partial(product_id, updated_product: ProductUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None
    
    product_dict = updated_product.model_dump(exclude_unset=True)

    columns = ", ".join([f"{column} = ? "for column in product_dict.keys()])
    values = tuple(product_dict.values())
    
    query = f"""UPDATE products SET {columns} WHERE id = ?"""
    cursor.execute(query, (values + (product_id, )))
    

    conn.commit()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    updated = cursor.fetchone()

    conn.close()

    return map_product(updated)

    

