from fastapi import APIRouter, BackgroundTasks
from app.schemas.webhook import WebhookPayload, WebhookResponse
from services.webhook_service import WebhookService

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
)


@router.post("/", response_model=WebhookResponse)
async def webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(WebhookService.process_event, payload)
    return WebhookResponse
