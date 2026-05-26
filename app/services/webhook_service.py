from app.schemas.webhook import WebhookPayload
from app.services.message_handler import process_message



async def process_event(payload: WebhookPayload):
    try:
        print(payload.model_dump_json())
        if payload.event == "Message":
            await process_message(payload.data)

    except Exception as e:
        print(f"Erro ao processar webhook: {e}")