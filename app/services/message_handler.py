from app.services.text_commands import commands
async def process_message(data: dict):
    name = data.get("Info", {}).get("PushName", "Desconecido")
    chat = data.get("Info", {}).get("Chat", "Desconecido")
    sender = data.get("Info", {}).get("Sender", "Desconecido")
    type = data.get("Info", {}).get("Type", "Desconecido")
    media_type = data.get("Info", {}).get("MediaType", "Desconecido")

    message = data.get("Message", {})

    if type == "text":
        await commands(name, chat, sender, message)
    elif type == "media":
        pass
