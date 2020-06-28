from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel

# https://developer.github.com/webhooks/event-payloads/#sponsorship
class SponsorAction(str, Enum):
    CREATED = "created"
    CANCELLED = "cancelled"
    EDITED = "edited"
    TIER_CHANGED = "tier_changed"
    PENDING_CANCELLATION = "pending_cancellation"
    PENDING_TIER_CHANGE = "pending_tier_change"


class SponsorActivity(BaseModel):
    action: SponsorAction
    sponsorship: Dict[Any, Any]
    sender: Dict[Any, Any]
    changes: Dict[Any, Any] = None
    effective_date: str = None


# https://developer.github.com/webhooks/event-payloads/#ping
class PingPayload(BaseModel):
    zen: str
    hook_id: int
    hook: Dict[Any, Any]
    sender: Dict[Any, Any]
    repository: Dict[Any, Any] = None
    organization: Dict[Any, Any] = None
