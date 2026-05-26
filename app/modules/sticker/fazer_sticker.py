import os
import uuid
import base64
import httpx
from PIL import Image, ImageOps

EVOLUTION_URL = "http://evo:8080"
API_KEY = "FC1AF84C8064-405C-B90F-1D7C9D1FD16A"
INSTANCE_NAME = "Frangro"

async def enviar_texto(phone: str, text: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        await client.post(
            f"{EVOLUTION_URL}/message/sendText/{INSTANCE_NAME}",
            headers={"apikey": API_KEY},
            json={"number": phone, "text": text},
        )

async def enviar_sticker(phone: str, caminho_webp: str):
    with open(caminho_webp, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    payload = {
        "number": phone,
        "sticker": encoded,
    }

    async with httpx.AsyncClient(timeout=300.0) as client:
        r = await client.post(
            f"{EVOLUTION_URL}/message/sendSticker/{INSTANCE_NAME}",
            headers={"apikey": API_KEY},
            json=payload,
        )
        print(f"EVOLUTION (sticker): {r.status_code}")
        return r.status_code

async def enviar_sticker_url(phone: str, url: str):
    payload = {
        "number": phone,
        "sticker": url,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{EVOLUTION_URL}/message/sendSticker/{INSTANCE_NAME}",
            headers={"apikey": API_KEY},
            json=payload,
        )

        print(f"EVOLUTION (sticker-url): {r.status_code} | {r.text}")
        return r.status_code
    
def converter_para_sticker(caminho_original: str) -> str:
    img = Image.open(caminho_original).convert("RGBA")

    # Redimensiona mantendo proporção e preenchendo todo o espaço 512x512
    img = ImageOps.fit(img, (512, 512), Image.Resampling.LANCZOS)

    caminho_webp = caminho_original.replace(os.path.splitext(caminho_original)[1], ".webp")
    img.save(caminho_webp, "WEBP", quality=90)
    img.close()

    return caminho_webp

async def baixar_imagem(message_data: dict) -> str:
    url = f"{EVOLUTION_URL}/chat/getBase64FromMediaMessage/{INSTANCE_NAME}"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            url,
            headers={"apikey": API_KEY},
            json={"message": message_data}
        )

        base64_data = response.json().get("base64")
        image_bytes = base64.b64decode(base64_data)

        os.makedirs("stickers", exist_ok=True)
        caminho = f"stickers/{uuid.uuid4()}.jpg"

        with open(caminho, "wb") as f:
            f.write(image_bytes)

        return caminho

async def criar_sticker(phone: str, message_data: dict):
    try:
        caminho_original = await baixar_imagem(message_data)
        caminho_sticker = converter_para_sticker(caminho_original)

        await enviar_sticker(phone, caminho_sticker)

        os.remove(caminho_original)
        os.remove(caminho_sticker)

    except Exception as e:
        print(f"Erro: {e}")
        await enviar_texto(phone, "❌ Erro ao criar sticker")