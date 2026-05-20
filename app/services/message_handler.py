from app.services.text_commands import text_commands
async def process_message(data: dict):
    type = data.get("Info", {}).get("Type", "Desconecido")

    if type == "text":
        await text_commands(data)
    elif type == "media":
        pass
