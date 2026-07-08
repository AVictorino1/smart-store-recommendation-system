from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_filters(query: str) -> dict:
    prompt = f"""
Analizá esta consulta de búsqueda de ropa: "{query}"

Extraé los siguientes atributos si están presentes en la consulta.
Si no están presentes dejá el valor como null.

- gender: solo puede ser "hombre", "mujer", "unisex" o null
- category: solo puede ser "tops", "bottoms" o null
- color: el color mencionado en español o null
- price_max: número entero si menciona precio máximo o null
- is_clothing_query: true si la consulta es sobre ropa o accesorios, false si no tiene nada que ver con ropa

Respondé ÚNICAMENTE con JSON válido sin texto antes ni después.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un extractor de entidades para un sistema de búsqueda de ropa. Respondés siempre con JSON válido únicamente."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=256,
        temperature=0.1
    )

    texto = response.choices[0].message.content.strip()
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]

    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"is_clothing_query": True}