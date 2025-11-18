import os
import requests

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

def send_whatsapp(to_number: str, message: str):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print("Faltan variables de entorno para WhatsApp. No se envía mensaje.")
        return

    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print("WhatsApp API response:", r.status_code, r.text)
    except Exception as e:
        print("Error enviando mensaje WhatsApp:", e)
