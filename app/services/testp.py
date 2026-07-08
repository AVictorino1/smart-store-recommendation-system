from app.services.conversation_service import get_history

def main():
    print(get_history("whatsapp:+50557171904", 20))
    return 0

if __name__ == "__main__":
    main()