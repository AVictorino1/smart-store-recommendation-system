from groq import Groq
from dotenv import load_dotenv
import os
import json
from app.services.nlp_service import extract_filters
from app.recommender.pipeline import search_by_text

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_system_prompt(business: dict) -> str:
    return f"""Eres un asistente de ventas amigable y natural para {business['business_name']}, 
una tienda de {business['business_type']}.

Información del negocio:
- Métodos de pago: {business['payment_methods']}
- Envíos: {business['shipping_info']}
- Devoluciones: {business['return_policy']}
- Horarios: {business['schedule']}
- Contacto: {business['contact']}

Tu comportamiento:
- Respondé siempre en español, de forma natural y amigable
- Tus respuestas deben ser breves
- Si el cliente busca un producto, extraé los detalles y buscá en el catálogo
- Si el cliente saluda, saludá de vuelta y preguntá en qué podés ayudar
- Si el cliente pregunta sobre pagos, envíos, devoluciones u horarios, respondé con la información del negocio
- Si la consulta no tiene nada que ver con la tienda, explicá amablemente que solo podés ayudar con productos y servicios de {business['business_name']}
- Nunca inventés información que no esté en los datos del negocio
- Cuando encontrés productos relevantes, presentalos de forma atractiva

Para buscar productos tenés acceso a un catálogo con estas categorías: {business['business_type']}.
Cuando el cliente pida un producto, respondé con EXACTAMENTE este formato JSON y nada más:
{{"action": "search", "query": "texto de búsqueda", "filters": {{"gender": null, "category": null, "color": null, "price_max": null}}}}
Si no están presentes dejá el valor como null.

- gender: solo puede ser "hombre", "mujer", "unisex" o null
- category: solo puede ser "tops", "bottoms" o null
- color: el color mencionado en español o null
- price_max: número entero si menciona precio máximo o null
Para cualquier otra respuesta, respondé con texto natural directamente."""


def process_with_agent(message: str, history: list, business: dict) -> str:
    
    intent_data = detect_intent(message, history, business)
    intent = intent_data.get("intent", "greeting")

    if intent == "search":
        query = intent_data.get("query", message)

        if not query:
            query = message
            
        filters = intent_data.get("filters", {})
        search_results = search_by_text(query, k=3, filters=filters)
        
        images = []
        products_recomm = []
        if search_results is not None and not search_results.empty:
            products_recomm = [product for _, product in search_results.iterrows()]
            images = [
                url for url in search_results["image_url"].tolist()
                if url is not None
            ]
        
        return {
            "text": generate_response(message, history, business, search_results),
            "images": images,
            "products": products_recomm
        }

    elif intent == "irrelevant":
        return {
            "text": f"Solo puedo ayudarte con productos y servicios de {business['business_name']}.",
            "images": [],
            "products": []
        }

    else:
        return {
            "text": generate_response(message, history, business, search_results=None),
            "images": [],
            "products": []
        }


def generate_response(message: str, history: list, business: dict, search_results=None) -> str:
    
    if search_results is not None and search_results.empty:
        context = "No encontré productos que coincidan con esa búsqueda en el catálogo."
    elif search_results is not None:
        productos_texto = ""
        for _, product in search_results.iterrows():
            productos_texto += f"- {product['name']}, ${product['price']}, {product['description'][:60]}\n"
        context = f"Encontré estos productos en el catálogo:\n{productos_texto}"
    else:
        context = None

    system_content = f"""Eres un asistente de ventas amigable para {business['business_name']}, una tienda de {business['business_type']}.

        Información del negocio:
        - Métodos de pago: {business['payment_methods']}
        - Envíos: {business['shipping_info']}
        - Devoluciones: {business['return_policy']}
        - Horarios: {business['schedule']}
        - Contacto: {business['contact']}

        Reglas importantes:
        - Tus respuestas deben ser breves y precisas
        - Respondé SIEMPRE en español natural y amigable
        - NUNCA afirmes tener productos que no están en el catálogo
        - NUNCA devuelvas JSON al cliente, solo texto natural
        - Si no hay productos disponibles, sé honesto y ofrecé alternativas"""

    if context:
        system_content += f"\n\nResultados de búsqueda para responder:\n{context}"

    messages = [{"role": "system", "content": system_content}]
    
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=512,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def detect_intent(message: str, history: list, business: dict) -> dict:

    history_context = ""
    if history:
        recent = history[-4:] if len(history) > 4 else history
        for msg in recent:
            role = "Cliente" if msg["role"] == "user" else "Asistente"
            history_context += f"{role}: {msg['content']}\n"


    messages = [
                    {
                        "role": "system",
                        "content": f"""Eres un clasificador de intenciones para una tienda de {business['business_type']}.

            Historial reciente de la conversación:
            {history_context if history_context else "Sin historial previo"}

            Analizá el mensaje considerando el contexto del historial y respondé ÚNICAMENTE con JSON válido:

            {{
                "intent": "search" | "greeting" | "business_info" | "irrelevant",
                "query": "texto de búsqueda completo incluyendo contexto del historial si es necesario, sino null",
                "filters": {{
                    "gender": null,
                    "category": null,
                    "color": null,
                    "price_max": null
                }}
            }}

            intent debe ser:
                - "search": el cliente busca un producto
                - "greeting": saludo o despedida
                - "business_info": pregunta sobre pagos, envíos, horarios, devoluciones
                - "irrelevant": no tiene que ver con la tienda
                
                Para filters, si no están presentes dejá el valor como null.
                - gender: solo puede ser "hombre", "mujer", "unisex" o null
                - category: solo puede ser "tops", "bottoms" o null
                - color: el color mencionado en español o null
                - price_max: número entero si menciona precio máximo o null

            Si el mensaje es una continuación de una búsqueda anterior como "para mujer?" o "en negro?", 
            construí una query completa combinando el contexto previo con el mensaje actual.
            Si no hay suficiente contexto para una query, devolvé intent "greeting" en vez de search con query null."""
                    },
                    {"role": "user", "content": message}
    ]        
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
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
        return {"intent": "greeting"}