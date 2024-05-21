import requests
import schedule
import time
import random
from datetime import datetime
from dotenv import load_dotenv
import os
import config
import json

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
    
    if response.status_code == 200:
        print("\nMessage WhatsApp envoyé avec succès.")
    else:
        print(f"\nErreur lors de l'envoi du message WhatsApp: {response.status_code}, {response.text}")


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

    response = requests.post(url, headers=headers, data=json.dumps(interactive_message_payload))
    
    if response.status_code == 200:
        print("\nReminder message envoyé avec succès.")
    else:
        print(f"\nErreur lors de l'envoi du reminder message WhatsApp: {response.status_code}, {response.text}")


def send_daily_message():
    message = "Ceci est un message de rappel."
    send_interactive_message(message, "ok", "C'est noté")


def format_datetime(datetime_str):
    date_time_obj = datetime.fromisoformat(datetime_str[:-6])
    return date_time_obj.strftime("%d %B %Y à %Hh%M")

def check_availabilities(practicien):
    url = "https://www.doctolib.fr/availabilities.json"
    start_date = datetime.now().strftime("%Y-%m-%d")
    params = practicien["params"].copy()
    params["start_date"] = start_date

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    response = requests.get(url, params=params, headers=headers)
        
    if response.status_code == 200:
        data = response.json()
        if "next_slot" in data:
            next_slot = format_datetime(data["next_slot"])
            message = (
                f"Il y a au moins un rendez-vous libre pour *{practicien['name']}*.\n\n"
                f"Prochain créneau disponible : \n{next_slot}.\n\n"
                f"Réservez ici : {practicien['booking_url']}"
            )
            
            send_whatsapp_message(message)
            print("\nMessage envoyé : {message}")
        else:
            print("\nPas de rendez-vous libre pour le moment.")
    else:
        print(f"\nErreur lors de la récupération des disponibilités : {response.status_code} - {response.text}")
    
    # Planifier la prochaine vérification après l'intervalle aléatoire
    schedule_random_interval()

def schedule_random_interval():
    min_interval = 8*60 # 8 minutes in seconds
    max_interval = 12*60 # 12 minutes in seconds
    random_interval = random.randint(min_interval, max_interval)
    current_time = datetime.now().strftime("[%d.%m.%Y - %Hh%M]")
    print(f"\n{current_time} - Next check scheduled in {random_interval // 60} minutes and {random_interval % 60} seconds.")
    schedule.clear()  # Clear the current schedule
    schedule.every(random_interval).seconds.do(
        check_availabilities,
        config.tenon_fertilite
    )

def run_scheduler():
    schedule_random_interval()  # Schedule the first check
    
      # Planifier l'envoi du message quotidien à midi
    schedule.every().day.at("12:10").do(send_daily_message)
    
    while True:
        current_time = time.localtime()
        if 8 <= current_time.tm_hour < 21:
            schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
