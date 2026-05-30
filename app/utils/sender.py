import httpx
import mimetypes
from app.core.config import settings


async def ApiEvo(path: str, payload: dict) -> dict:
    headers = {"apikey": settings.KEYEVO}
    url = f"{settings.URLEVO}/{path}"
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)
        return response.json()


async def send_text(number: str, text: str, delay: int = 3, mentionAll: bool = False):
    payload = {
        "delay": delay,
        "mentionAll": mentionAll,
        "mentionedJid": [],
        "number": number,
        "text": text,
    }
    await ApiEvo("send/text", payload)


async def react_message(chat: str, sender: str, messageId: str, emoji: str):
    payload = {
        "number": chat,
        "reaction": emoji,
        "id": messageId,
        "fromMe": False,
        "participant": sender,
    }
    await ApiEvo("message/react", payload)


async def remove_group_participant(chat: str, sender: str):
    payload = {
        "groupJid": chat,
        "action": "remove",
        "participants": [sender],
    }
    await ApiEvo("group/participant", payload)


async def send_media(
    chat: str,
    tipo: str,
    file: bytes,
    caption: str | None = None,
    filename: str | None = None,
):
    data = {
        "number": chat,
        "type": tipo,
        "caption": caption,
    }

    mimetype, _ = mimetypes.guess_type(filename) if filename else (None, None)
    if not mimetype:
        mimetype = "application/octet-stream"

    async with httpx.AsyncClient(timeout=60) as client:
        files = {"file": (filename, file, mimetype)}
        headers = {"apikey": settings.KEYEVO}
        await client.post(
            f"{settings.URLEVO}/send/media",
            data=data,
            files=files,
            headers=headers,
            timeout=60,
        )


async def send_sticker_url(chat: str, url: str):
    payload = {
        "number": chat,
        "sticker": url,
    }

    await ApiEvo("send/sticker", payload)
