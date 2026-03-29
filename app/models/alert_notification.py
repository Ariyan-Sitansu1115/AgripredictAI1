"""
AlertNotification database model.

Stores every notification attempt (SMS + Email) so that the UI can show
accurate "Sent / Failed / Partial" status instead of a hard-coded mock.
"""
from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.models.base import Base


class AlertNotification(Base):
    """Audit record for each notification dispatched (or attempted) for an alert."""

    __tablename__ = "alert_notifications"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, nullable=False, index=True)
    user_id = Column(String(255), nullable=False, index=True)

    # Contact details used at send time
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)

    # Delivery outcomes: "sent" | "failed" | "not_enabled"
    sms_status = Column(String(20), nullable=False, default="not_enabled")
    email_status = Column(String(20), nullable=False, default="not_enabled")

    # Raw provider responses (stored as JSON text for debugging)
    sms_response = Column(Text, nullable=True)
    email_response = Column(Text, nullable=True)

    # Human-readable error summary (nullable – only set on failure)
    error_message = Column(Text, nullable=True)

    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
