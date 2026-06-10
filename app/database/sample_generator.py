from groq import Groq
from dotenv import load_dotenv
import json
import time
import os
#from app.database.product_repository import get_all_products

load_dotenv()
api_k = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_k)

"""
models: llama-3.3-70b-versatile, llama-3.1-8b-instant
def main():
    products = get_all_products()
    complete_item(products)
"""
def main():
    pass


def complete_item(all_items:list):
    complete_items = []
    for i, item in enumerate(all_items):
        if i == 50:
            break
        print(f"Processing {i+1}/{len(all_items)}...")
        complete = generate_complex_strings(item)
        complete_items.append(complete)
        time.sleep(0.2)
        

    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(complete_items, f, ensure_ascii=False, indent=2)


def generate_complex_strings(item: dict) -> dict:
    categories = ", ".join(f"{category}: {item[category]}" for category in item.keys())
    prompt = f""" 
    Tienes este producto de ropa con estos atributos: {categories}
    Tu tarea es asignar valores a las categorias: name, tags y description,
    Estas tres categorias deben tener en común esto:
    - Deben basarse en las demás categorias que te mostré
    - Los valores que tu generes deben ser de lenguaje humano cotidiano, usando sinonimos, variantes y expresiones comunes/naturales
    - Añade/inventa información extra que no aparezca en los datos que te compartí, por ejemplo, puedes inventarte que una camisa tiene rayas, o estampados, etc.
    Luego:
    Para tags especificamente, debe ser una lista de entre 10-15 palabras/frases
    Y para description, deben ser 2-4 oraciones, repito, añade info extra que no aparezca en las demás categorias (con sentido)

    Respondé ÚNICAMENTE con un JSON válido EN ESPAÑOL con estas tres claves: name, tags, description.
    Sin texto antes ni después. Sin backticks. Solo el JSON.

    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
                        "role": "system",
                        "content":"""Eres un redactor creativo especializado en moda urbana y comercial.
                        Usás lenguaje popular, variado y natural. Mezclás términos latinoamericanos
                        e ibéricos cuando aplica. Respondés siempre con JSON válido únicamente."""
                    }, 
                    {
                        "role" : "user",
                        "content": prompt

                    }
                    ], 
                    max_tokens = 1024,
                    temperature=0.8
                    )

    texto = response.choices[0].message.content
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
    
    try:
        campos = json.loads(texto)
    except json.JSONDecodeError:
        print(f"Invalid JSON in the item:", texto)
        campos = {"name": None, "tags": [], "description": None}

    try:
        item["name"] = campos["name"]
        item["tags"] = campos["tags"]
        item["description"] = campos["description"]
    except KeyError:
        pass
       

    return item


if __name__ == "__main__":
    main()
    
