from app.database.conversation_repository import (
    get_conversation_history,
    save_message,
    clear_conversation
)

def get_history(phone_number: str, limit: int = 10):
    return get_conversation_history(phone_number, limit)

def save_user_message(phone_number: str, content: str):
    save_message(phone_number, "user", content)

def save_assistant_message(phone_number: str, content: str):
    save_message(phone_number, "assistant", content)

def clear_history(phone_number: str):
    clear_conversation(phone_number)