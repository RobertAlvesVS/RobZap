from app.modules.yt.baixar_yt import baixar_yt


async def media_commands(data: dict):
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
    if text.startswith("/baixar"):
        await baixar_yt(name, sender, chat, text)
