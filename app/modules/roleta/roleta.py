import random

from app.utils.sender import react_message, remove_group_participant, send_text


async def roleta(name: str, sender: str, id: str, chat: str):

    if random.randint(1, 6) == 1:
        await send_text(chat, f"{name} perdeu a roleta russa! 💥")
        await react_message(chat, sender, id, "💥")
        await remove_group_participant(chat, sender)
    else:
        await send_text(chat, f"{name} sobreviveu à roleta russa! 😅")
        await react_message(chat, sender, id, "😅")
