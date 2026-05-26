import httpx
import mimetypes


async def send_text(number: str, text: str, delay: int = 3, mentionAll: bool = False):
    payload = {
        "delay": delay,
        "mentionAll": mentionAll,
        "mentionedJid": [],
        "number": number,
        "text": text,
    }
    headers = {"Content-Type": "application/json", "apikey": "TokenTeste"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8080/send/text", json=payload, headers=headers
        )
        print("Resposta do envio de texto:", response.status_code, response.text)


async def react_message(chat: str, sender: str, messageId: str, emoji: str):
    payload = {
        "number": chat,
        "reaction": emoji,
        "id": messageId,
        "fromMe": False,
        "participant": sender,
    }
    headers = {"Content-Type": "application/json", "apikey": "TokenTeste"}

    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8080/message/react", json=payload, headers=headers
        )


async def remove_group_participant(chat: str, sender: str):
    payload = {
        "groupJid": chat,
        "action": "remove",
        "participants": [sender],
    }
    headers = {"Content-Type": "application/json", "apikey": "TokenTeste"}

    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8080/group/participant", json=payload, headers=headers
        )


async def send_pix(chat: str):
    payload = {
        "number": chat,
        "title": "PIX",
        "description": "Realize o pagamento via PIX:",
        "footer": "Obrigado",
        "buttons": [
            {
                "type": "pix",
                "currency": "BRL",
                "name": "Robert Alves Ventura dos Santos",
                "keyType": "CPF",
                "key": "06152890535",
            }
        ],
    }
    headers = {"Content-Type": "application/json", "apikey": "TokenTeste"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8080/send/button", json=payload, headers=headers
        )
        print("Resposta do envio do PIX:", response.status_code, response.text)


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

    files = {"file": (filename, file, mimetype)}

    headers = {"apikey": "TokenTeste"}

    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8080/send/media",
            data=data,
            files=files,
            headers=headers,
            timeout=60,
        )
