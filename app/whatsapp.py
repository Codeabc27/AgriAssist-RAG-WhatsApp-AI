import os

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value.strip()
    return default


WHATSAPP_ACCESS_TOKEN = _get_env(
    "WHATSAPP_ACCESS_TOKEN",
    "WHATSAPP_TOKEN",
    "META_ACCESS_TOKEN",
    default="",
)
WHATSAPP_PHONE_NUMBER_ID = _get_env(
    "WHATSAPP_PHONE_NUMBER_ID",
    "PHONE_NUMBER_ID",
    "META_PHONE_NUMBER_ID",
    default="",
)
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v20.0")


def send_message(to: str, message: str):
    """Send a text reply via the WhatsApp Cloud API."""

    if not WHATSAPP_ACCESS_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        raise RuntimeError(
            "Missing WhatsApp credentials. Set WHATSAPP_ACCESS_TOKEN/WHATSAPP_TOKEN and "
            "WHATSAPP_PHONE_NUMBER_ID/PHONE_NUMBER_ID in your .env file."
        )

    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
