"""
Notification Service
Sends real SMS and Email notifications.

SMS providers supported:
  • Twilio  (set SMS_PROVIDER=twilio)
  • Fast2SMS (set SMS_PROVIDER=fast2sms  – India-only)

Email provider:
  • Gmail SMTP via smtplib (uses App Password, not the account password)

All credentials are loaded from environment / .env via `app.core.config.settings`.
Every outbound call is logged to logs/notification.log.
"""

import json
import re
import smtplib
import socket
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

import requests

from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger("notification")

# ---------------------------------------------------------------------------
# Phone-number helper
# ---------------------------------------------------------------------------

_PHONE_RE = re.compile(r"^\+?[0-9\s\-().]{7,20}$")


def normalize_phone(phone: str) -> Optional[str]:
    """
    Normalise an Indian mobile number to E.164 format (+91XXXXXXXXXX).

    Accepted prefixes: +91, 91, 0.  The remaining digits must be exactly 10.
    Returns ``None`` when the input is invalid.
    """
    if not phone:
        return None
    digits = re.sub(r"[\s\-().]", "", phone)
    if digits.startswith("+91"):
        core = digits[3:]
    elif digits.startswith("91") and len(digits) == 12:
        core = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        core = digits[1:]
    else:
        core = digits

    if len(core) != 10 or not core.isdigit():
        return None
    return f"+91{core}"


# ---------------------------------------------------------------------------
# Email helper
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(email and _EMAIL_RE.match(email))


# ---------------------------------------------------------------------------
# SMS sending
# ---------------------------------------------------------------------------

def _send_twilio(phone: str, message: str) -> Dict[str, Any]:
    """Send SMS via Twilio REST API. Returns a response dict."""
    url = (
        f"https://api.twilio.com/2010-04-01/Accounts/"
        f"{settings.TWILIO_ACCOUNT_SID}/Messages.json"
    )
    payload = {
        "To": phone,
        "From": settings.TWILIO_PHONE_NUMBER,
        "Body": message,
    }
    try:
        resp = requests.post(
            url,
            data=payload,
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
            timeout=15,
        )
        data = resp.json()
        logger.info("Twilio response [%s]: %s", resp.status_code, data)
        if resp.status_code in (200, 201) and data.get("sid"):
            return {
                "success": True,
                "message_sid": data.get("sid"),
                "sent_at": datetime.now(timezone.utc).isoformat(),
            }
        return {
            "success": False,
            "error": data.get("message", "Unknown Twilio error"),
            "status_code": resp.status_code,
        }
    except requests.Timeout:
        logger.error("Twilio request timed out for phone=%s", phone)
        return {"success": False, "error": "Request timed out"}
    except requests.RequestException as exc:
        logger.error("Twilio request error for phone=%s: %s", phone, exc)
        return {"success": False, "error": str(exc)}


def _send_fast2sms(phone: str, message: str) -> Dict[str, Any]:
    """Send SMS via Fast2SMS DLT/Quick-Send API."""
    # Fast2SMS expects the number without country code
    number = phone.lstrip("+")
    if number.startswith("91"):
        number = number[2:]

    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {"authorization": settings.FAST2SMS_API_KEY, "Content-Type": "application/json"}
    payload = {
        "route": settings.FAST2SMS_ROUTE or "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": number,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        data = resp.json()
        logger.info("Fast2SMS response [%s]: %s", resp.status_code, data)
        if resp.status_code == 200 and data.get("return") is True:
            return {
                "success": True,
                "request_id": data.get("request_id"),
                "sent_at": datetime.now(timezone.utc).isoformat(),
            }
        return {
            "success": False,
            "error": str(data.get("message", "Unknown Fast2SMS error")),
            "status_code": resp.status_code,
        }
    except requests.Timeout:
        logger.error("Fast2SMS request timed out for phone=%s", phone)
        return {"success": False, "error": "Request timed out"}
    except requests.RequestException as exc:
        logger.error("Fast2SMS request error for phone=%s: %s", phone, exc)
        return {"success": False, "error": str(exc)}


def send_sms(phone: str, message: str) -> Dict[str, Any]:
    """
    Validate, normalise and send an SMS via the configured provider.

    Returns a dict with keys:
      ``success`` (bool), and either provider-specific fields or ``error`` (str).
    """
    normalised = normalize_phone(phone)
    if not normalised:
        logger.warning("Invalid phone number supplied: %s", phone)
        return {"success": False, "error": f"Invalid phone number: {phone}"}

    if not message:
        return {"success": False, "error": "Message body is empty"}

    provider = (settings.SMS_PROVIDER or "twilio").lower()

    logger.info("Sending SMS via %s to %s", provider, normalised)

    if provider == "fast2sms":
        if not settings.FAST2SMS_API_KEY:
            return {"success": False, "error": "FAST2SMS_API_KEY is not configured"}
        return _send_fast2sms(normalised, message)

    # default: twilio
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
        return {"success": False, "error": "Twilio credentials are not configured"}
    return _send_twilio(normalised, message)


# ---------------------------------------------------------------------------
# Email sending
# ---------------------------------------------------------------------------

def send_email(recipient: str, subject: str, message: str) -> Dict[str, Any]:
    """
    Send an email via Gmail SMTP.

    Requires ``GMAIL_EMAIL`` and ``GMAIL_APP_PASSWORD`` to be set in the
    environment / .env file (use a Google App Password, not your account
    password).

    Returns a dict with keys:
      ``success`` (bool), and either ``message_id`` / ``sent_at`` or ``error``.
    """
    if not is_valid_email(recipient):
        logger.warning("Invalid email address: %s", recipient)
        return {"success": False, "error": f"Invalid email address: {recipient}"}

    if not settings.GMAIL_EMAIL or not settings.GMAIL_APP_PASSWORD:
        return {"success": False, "error": "Gmail credentials (GMAIL_EMAIL / GMAIL_APP_PASSWORD) are not configured"}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.GMAIL_EMAIL
    msg["To"] = recipient

    # Plain-text part
    msg.attach(MIMEText(message, "plain"))
    # HTML part (simple wrapper)
    html_body = f"<html><body><p>{message}</p></body></html>"
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.login(settings.GMAIL_EMAIL, settings.GMAIL_APP_PASSWORD)
            server.sendmail(settings.GMAIL_EMAIL, recipient, msg.as_string())

        sent_at = datetime.now(timezone.utc).isoformat()
        message_id = msg.get("Message-ID", f"<{sent_at}@agripredict>")
        logger.info("Email sent to %s, message_id=%s", recipient, message_id)
        return {"success": True, "message_id": message_id, "sent_at": sent_at}

    except smtplib.SMTPAuthenticationError as exc:
        logger.error("Gmail SMTP authentication failed: %s", exc)
        return {"success": False, "error": "Gmail authentication failed – check GMAIL_APP_PASSWORD"}
    except smtplib.SMTPException as exc:
        logger.error("Gmail SMTP error sending to %s: %s", recipient, exc)
        return {"success": False, "error": f"SMTP error: {exc}"}
    except socket.timeout:
        logger.error("Gmail SMTP connection timed out for %s", recipient)
        return {"success": False, "error": "SMTP connection timed out"}
    except OSError as exc:
        logger.error("Email send OS error for %s: %s", recipient, exc)
        return {"success": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# Convenience class (kept for backwards-compatibility with any existing imports)
# ---------------------------------------------------------------------------

class NotificationService:
    """Service for sending notifications (thin wrapper around module-level helpers)."""

    def __init__(self) -> None:
        pass

    def send_email(self, recipient: str, subject: str, message: str) -> Dict[str, Any]:
        """Send email notification."""
        return send_email(recipient, subject, message)

    def send_sms(self, phone: str, message: str) -> Dict[str, Any]:
        """Send SMS notification."""
        return send_sms(phone, message)
