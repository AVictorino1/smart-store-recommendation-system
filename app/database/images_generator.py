import requests
import sqlite3
import os
import time
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
PEXELS_KEY = os.getenv("PEXELS_API_KEY")

def build_search_query(product: dict) -> str:
    parts = []
    
    if product["brand"]:
        parts.append(product["brand"])
    if product["subcategory"]:
        parts.append(product["subcategory"].replace("_", " "))
    if product["color"]:
        parts.append(product["color"])
    
    return " ".join(parts)

def get_image_url(query: str) -> str:
    url = "https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "portrait"
    }
    headers = {
        "Authorization": PEXELS_KEY  
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        print(f"Error {response.status_code} para query: {query}")
        return None
    
    data = response.json()
    photos = data.get("photos", [])
    
    if not photos:
       
        return get_image_url_fallback(query.split()[-2] if len(query.split()) > 1 else query)
    
    
    return photos[0]["src"]["medium"]

def get_image_url_fallback(query: str) -> str:
    url = "https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "portrait"
    }
    headers = {
        "Authorization": PEXELS_KEY
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    photos = data.get("photos", [])
    
    if not photos:
        return None
    
    return photos[0]["src"]["medium"]

def update_product_image(product_id: int, image_url: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE products SET image_url = ? WHERE id = ?",
        (image_url, product_id)
    )
    conn.commit()
    conn.close()

def add_images_to_catalog():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, brand, subcategory, color 
        FROM products 
        WHERE image_url IS NULL
    """)
    products = cursor.fetchall()
    conn.close()
    
    print(f"Productos sin imagen: {len(products)}")
    
    for i, product in enumerate(products):
        query = build_search_query(dict(product))
        print(f"Buscando imagen {i+1}/{len(products)}: {query}")
        
        image_url = get_image_url(query)
        
        if image_url:
            update_product_image(product["id"], image_url)
            print(f"✓ imagen asignada: {image_url}")
        else:
            print(f"✗ sin imagen para producto {product['id']}")
        
        time.sleep(0.5)  # Pexels permite 200 requests/hora, podés ser más rápido

if __name__ == "__main__":
    add_images_to_catalog()