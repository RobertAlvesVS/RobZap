from fastapi import APIRouter, BackgroundTasks
from app.schemas.webhook import WebhookPayload, WebhookResponse

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
)


@router.post("/", response_model=WebhookResponse)
async def webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    print(payload)
    return WebhookResponse
