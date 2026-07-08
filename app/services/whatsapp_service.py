import numpy as np
import pandas as pd
from app.recommender.pipeline import search_by_text
from app.services.nlp_service import extract_filters
from app.services.business_service import get_business
from app.services.agent_service import process_with_agent
from app.services.conversation_service import (save_user_message, get_history, save_assistant_message)

async def process_message(message: str, sender: str) -> dict:
    message = message.strip()
    print(f"sender: {sender}")
    if not message:
        return {
            "text": "Hola, escribime qué producto estás buscando.",
            "images": [],
            "products": []
        }

    try:
        save_user_message(sender, message)
        history = get_history(sender, limit=10)
        business = get_business()

        result = process_with_agent(message, history, business)

        save_assistant_message(sender, result["text"])

        return result

    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        return {
            "text": "Hubo un error procesando tu consulta. Intentá de nuevo.",
            "images": [],
            "products": []
        }

