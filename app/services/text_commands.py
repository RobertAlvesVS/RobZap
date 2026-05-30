from app.modules.roleta.roleta import roleta
from app.modules.yt.baixar_yt import baixar_yt
from app.utils.sender import (
    send_text,
    react_message,
)


async def text_commands(data: dict):
    info = data.get("Info", {})
    message = data.get("Message", {})

    id = info.get("ID", "Desconecido")
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
        await send_text(chat, "Pong!")
        await react_message(chat, sender, id, "🏓")
    elif text.startswith("/roleta"):
        await roleta(name, sender, id, chat)
    elif text.startswith("/baixar"):
        await baixar_yt(name, sender, chat, text)
