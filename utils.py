import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration WhatsApp API depuis les variables d'environnement
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v19.0")


def send_whatsapp_message(message):
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_PHONE_NUMBER,
        "type": "text",
        "text": {"preview_url": False, "body": message[:4096]}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(
            f"\nErreur lors de l'envoi du message WhatsApp: {response.status_code}, {response.text}")


def send_interactive_message(body_text, button_id, button_title):
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
    }
    interactive_message_payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_PHONE_NUMBER,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": body_text[:1024]  # Max 1024 characters - Whatsapp API
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": button_id,
                            # Max 20 characters - Whatsapp API
                            "title": button_title[:20]
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(interactive_message_payload))

    if response.status_code == 200:
        print("\nReminder message envoyé avec succès.")
    else:
        print(
            f"\nErreur lors de l'envoi du reminder message WhatsApp: {response.status_code}, {response.text}")


def send_daily_message():
    message = "Ceci est un message de rappel."
    send_interactive_message(message, "ok", "C'est noté")


def format_datetime(datetime_str):
    date_time_obj = datetime.fromisoformat(datetime_str[:-6])
    return date_time_obj.strftime("%d %B %Y à %Hh%M")
