from app.services.text_commands import text_commands as text_command
async def process_message(data: dict):
    type = data.get("Info", {}).get("Type", "Desconecido")

    if type == "text":
        await text_command(data)
    elif type == "media":
        pass
