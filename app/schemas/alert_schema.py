"""Alert Pydantic schemas"""
from pydantic import BaseModel
from typing import Any, Dict, Optional

class Alert(BaseModel):
    id: int
    alert_type: str
    crop: Optional[str]
    message: str
    severity: str
    created_at: str
    is_active: bool

class AlertSettingsRequest(BaseModel):
    price_drop: bool = True
    demand_spike: bool = True
    weather: bool = True
    email: bool = False

class AlertSettingsResponse(BaseModel):
    message: str
    settings: AlertSettingsRequest


# ---------------------------------------------------------------------------
# Notification send request / response
# ---------------------------------------------------------------------------

class SendNotificationRequest(BaseModel):
    alert_id: int
    user_id: str
    phone: Optional[str] = None
    email: Optional[str] = None
    message: str
    notify_sms: bool = False
    notify_email: bool = False


class SendNotificationResponse(BaseModel):
    # Overall outcome: "SUCCESS" | "FAILED" | "PARTIAL"
    status: str
    sms_status: str     # "sent" | "failed" | "not_enabled"
    email_status: str   # "sent" | "failed" | "not_enabled"
    sms_response: Optional[Dict[str, Any]] = None
    email_response: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
    timestamp: str


class TestNotificationRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    message: str = "This is a test notification from AgriPredictAI."
    notify_sms: bool = True
    notify_email: bool = True
