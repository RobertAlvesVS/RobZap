from fastapi import APIRouter, BackgroundTasks
from app.schemas.webhook import WebhookPayload, WebhookResponse
from app.services.webhook_service import process_event

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
)


@router.post("", response_model=WebhookResponse)
async def webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_event, payload)
    return WebhookResponse
