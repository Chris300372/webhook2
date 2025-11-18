from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from ai_agent import ai_answer
from whatsapp import send_whatsapp

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mi_token_secreto")

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return JSONResponse(content=int(challenge), status_code=200)
    else:
        return JSONResponse(content={"error": "Token inválido"}, status_code=403)

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        print("Webhook recibido:", data)

        # Extract message (safe access)
        entry = data.get("entry", [])
        if not entry:
            return {"status": "no_entry"}

        changes = entry[0].get("changes", [])
        if not changes:
            return {"status": "no_changes"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return {"status": "no_messages"}

        message = messages[0]
        from_number = message.get("from")
        text = message.get("text", {}).get("body", "")

        if not from_number or not text:
            return {"status": "missing_fields"}

        # Generate answer using ai_agent
        reply = ai_answer(text)

        # Send via WhatsApp
        send_whatsapp(from_number, reply)

    except Exception as e:
        print("Error procesando webhook:", e)

    return {"status": "ok"}
