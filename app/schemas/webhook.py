from pydantic import BaseModel
from typing import Optional, Dict, Any

class WebhookPayload(BaseModel):
    event: str
    data: Dict[str, Any]
    instanceId: str
    instanceToken: str

class WebhookResponse(BaseModel):
    status: int = 200