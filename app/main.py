import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

load_dotenv()

try:
    from app.rag_pipeline import rag_answer
    from app.whatsapp import send_message
except ImportError:
    from rag_pipeline import rag_answer
    from whatsapp import send_message

app = FastAPI()

logger = logging.getLogger(__name__)

# Hardcoded to match your Working token directly
VERIFY_TOKEN = "WORKING"


# Meta uses GET to verify the webhook callback URL.
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print(f"DEBUG GET -> Received Token: {token} | Expected Token: {VERIFY_TOKEN}")

    if (
        mode == "subscribe"
        and VERIFY_TOKEN
        and token == VERIFY_TOKEN
        and challenge is not None
    ):
        return PlainTextResponse(challenge, status_code=200)

    raise HTTPException(
        status_code=403,
        detail="Webhook verification failed",
    )


# Meta sends incoming WhatsApp messages using POST.
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        print(
            "DEBUG POST PAYLOAD RECEIVED:", data
        )  # This will print the raw message payload in your terminal

        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})

                # Delivery receipts and other events may have no messages.
                for message in value.get("messages", []):
                    sender = message.get("from")
                    message_type = message.get("type")

                    if not sender:
                        continue

                    if message_type != "text":
                        send_message(
                            sender,
                            "Please send your agricultural question as a text message.",
                        )
                        continue

                    text = message.get("text", {}).get("body", "").strip()
                    if not text:
                        continue

                    print(f"Processing message from {sender}: {text}")
                    reply = rag_answer(text)
                    send_message(sender, reply)

        return {"status": "ok"}

    except Exception:
        logger.exception("Failed to process WhatsApp webhook payload")
        raise HTTPException(
            status_code=500,
            detail="Failed to process webhook",
        )
