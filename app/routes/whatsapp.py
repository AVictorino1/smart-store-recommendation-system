from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.services.whatsapp_service import process_message
import os
from app.services.product_service import get_product_id
from twilio.rest import Client

router = APIRouter()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    incoming_message = form_data.get("Body", "")
    sender = form_data.get("From", "")

    result = await process_message(incoming_message, sender)
    print(result)
    text = result["text"]
    images = result["images"]
    products = result["products"]


    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>{text}</Message>
        </Response>"""

   
    if images:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for products_ in products:
            twilio_client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=sender,
                body=f"*{products_['name']}*\nPrecio: ${products_['price']}\n{products_['description'][:80]}...",
                media_url=[products_["image_url"]]
            )

    return Response(content=xml_response, media_type="application/xml")