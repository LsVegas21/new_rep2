from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import uuid

class LandingPageCreate(BaseModel):
    theme: str
    language: str
    traffic_source: str
    target_action: str

class LandingPageMetadata(BaseModel):
    company_name: str
    email: str
    phone: str
    address: str

class LandingPage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    theme: str
    language: str
    traffic_source: str
    target_action: str
    html: str
    lighthouse: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[LandingPageMetadata] = None