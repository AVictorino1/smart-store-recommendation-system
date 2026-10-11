from groq import Groq
from dotenv import load_dotenv
import os
import json
from app.models import Product

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def regenerate_product(product: Product, field: str, value: str, columns: list) -> dict:
    prompt = f"""
Tienes este producto,"{product}"
El cual ha sido actualizado por el usuario, pero la actualización afecta a las siguientes columnas: "{columns}"
Tu tarea es actualizar esas columnas con el dato que ha sido cambiado el cual es la columna: "{field}" con el NUEVO dato: "{value}", para que el cambio concuerde con las demás columnas.
Solo debes actualizar esas columnas que te compartí y NADA MÁS.
Por último vas a devolver un producto con las MISMAS COLUMNAS que el original pero con los datos cambiados como te dije.
Respondé ÚNICAMENTE con JSON válido sin texto antes ni después.
IMPORTANTE: los tags deben ir envueltos en "" así: "['tag1', 'tag2'...]"
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente que actualiza automáticamente las propiedades de un producto en una base de datos. Respondés siempre con JSON válido únicamente."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1024,
        temperature=0.1,
        reasoning_effort="low"
    )
    print("REASONING:", getattr(response.choices[0].message, "reasoning", None))
    texto = response.choices[0].message.content.strip()
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]

    try:
        print(f"EL PRODUCTO REGENERADO:{texto}")
        return json.loads(texto)
    except json.JSONDecodeError:
        print("VACIO")
        return []