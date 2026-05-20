from app.utils.sender import sender
async def commands(name, chat, sender, message):
    text = message.get("conversation", "")

    if text.startswith("/ping"):
        await sender(name, chat, sender, message)

        
