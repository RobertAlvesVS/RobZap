from app.utils.sender import (
    remove_group_participant,
    send_pix,
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
        import random

        print(f"Comando roleta russa recebido de {name} ({sender}) no chat {chat}")

        if random.randint(1, 6) == 1:
            await send_text(chat, f"{name} perdeu a roleta russa! 💥")
            await react_message(chat, sender, id, "💥")
            await remove_group_participant(chat, sender)
        else:
            await send_text(chat, f"{name} sobreviveu à roleta russa! 😅")
            await react_message(chat, sender, id, "😅")
    elif text.startswith("/pix"):
        print(f"Comando pix recebido de {name} ({sender}) no chat {chat}")
        await send_text(
            chat,
            f"Opa {name}, Obrigado por usar o comando /pix! Enviando as informações de pagamento...",
        )
        await send_pix(chat)
