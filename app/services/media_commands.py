from app.modules.sticker.criar_sticker import criar_sticker
from app.modules.yt.baixar_yt import baixar_yt


async def media_commands(data: dict):
    info = data.get("Info", {})
    message = data.get("Message", {})
    image_message = message.get("imageMessage", {})
    video_message = message.get("videoMessage", {})

    id = info.get("ID", "Desconecido")
    name = info.get("PushName", "Desconhecido")
    chat = info.get("Chat", "Desconhecido")
    sender = info.get("Sender", "Desconhecido")

    media_type = info.get("MediaType", "Desconhecido")

    text = (
        image_message.get("caption")
        or video_message.get("caption")
        or message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
        or "Desconhecido"
    )
    if text.startswith("/baixar"):
        await baixar_yt(name, sender, chat, text)
    elif text.strip() in ["/s", "/sticker"] and media_type == "image":
        print(f"📸 Comando /sticker recebido de {name} no chat {chat}")
        await criar_sticker(chat, id, data)
