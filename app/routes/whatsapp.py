from fastapi import APIRouter, Request
import app.services.whatsapp_service 

router = APIRouter()


@router.post('/whatsapp')
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    incoming_message = form_data.get("Body", "")
    sender = form_data.get("From", "")