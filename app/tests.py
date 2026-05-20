import httpx
import asyncio

payload = {
    "delay": 0,
    "formatJid": False,
    "id": "",
    "mentionAll": False,
    "mentionedJid": [],
    "number": "5511950500196-1632496064@g.us",
    "quoted": {"messageId": "", "participant": ""},
    "text": "Teste",
}
headers = {"Content-Type": "application/json", "apikey": "MinhaGlobalAPIKeyFilho!"}

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8080/send/text", json=payload)
        print(response.status_code)
        print(response.json())

asyncio.run(fetch_data())
