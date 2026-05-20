from app.utils.sender import send_text

async def text_commands(data: dict):
    info = data.get("Info", {})
    message = data.get("Message", {})

    name = info.get("PushName", "Desconhecido")
    chat = info.get("Chat", "Desconhecido")
    sender = info.get("Sender", "Desconhecido")

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
        or "Desconhecido"
    )

    if text.startswith("/ping"):
        print(f"Comando ping recebido de {name} ({sender}) no chat {chat}")