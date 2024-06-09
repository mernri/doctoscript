import requests
import schedule
import time
import random
from datetime import datetime
import config
import sys
import utils


def check_availabilities(practitioner):
    url = "https://www.doctolib.fr/availabilities.json"
    start_date = datetime.now().strftime("%Y-%m-%d")
    params = practitioner["params"].copy()
    params["start_date"] = start_date

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "next_slot" in data or "total" in data and data["total"] > 0:
            next_slot = utils.format_datetime(
                data["next_slot"]) if "next_slot" in data else "Inconnu"
            message = (
                f"Il y a au moins un rendez-vous libre pour *{practitioner['name']}*.\n\n"
                f"Prochain créneau disponible : \n{next_slot}.\n\n"
                f"Réservez ici : {practitioner['booking_url']}"
            )

            utils.send_whatsapp_message(message)
            print(
                f"\n                                          \033[92mRDV AVEC {practitioner['name']} DISPO le : . Message envoyé..\033[0m")

        else:
            print(
                f"\n                                          Pas de rendez-vous libre pour le moment pour {practitioner['name']}.")
    else:
        print(
            f"\n                                          \033[91mErreur lors de la récupération des disponibilités[0m")

    # Planifier la prochaine vérification après l'intervalle aléatoire
    schedule_random_interval(practitioner)


def schedule_random_interval(practitioner):
    min_interval = 7*60  # 7min
    max_interval = 12*60  # 12min
    random_interval = random.randint(min_interval, max_interval)
    current_time = datetime.now().strftime("%d.%m.%Y - %Hh%Mm%Ss")

    bold = "\033[1m"
    reset = "\033[0m"
    highlight_magenta = "\033[45m\033[97m"
    highlight_violet = "\033[48;5;93m\033[97m"

    print(
        f"\n{highlight_magenta} {practitioner['name']} {reset}{highlight_violet} {current_time} {reset}{bold} Next check scheduled in {random_interval // 60} minutes and {random_interval % 60} seconds.{reset}")
    schedule.clear()
    schedule.every(random_interval).seconds.do(
        check_availabilities,
        practitioner
    )


def generate_daily_schedule():
    # Between 7:25 and 7:35
    start_time = random.randint(7 * 60 + 25, 7 * 60 + 35)
    # Between 21:25 and 23:25
    end_time = random.randint(21 * 60 + 25, 23 * 60 + 25)
    start_hour, start_minute = divmod(start_time, 60)
    end_hour, end_minute = divmod(end_time, 60)
    return (start_hour, start_minute), (end_hour, end_minute)


def run_scheduler(practitioner):
    schedule_random_interval(practitioner)

    # Planifier l'envoi du message quotidien à midi
    schedule.every().day.at("12:00").do(utils.send_daily_message)

    while True:
        current_time = datetime.now()
        (start_hour, start_minute), (end_hour,
                                     end_minute) = generate_daily_schedule()
        start_time = current_time.replace(
            hour=start_hour, minute=start_minute, second=0, microsecond=0)
        end_time = current_time.replace(
            hour=end_hour, minute=end_minute, second=0, microsecond=0)

        if start_time <= current_time <= end_time:
            schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing practitioner name: python doctoscript.py <practitioner_name>")
        sys.exit(1)

    practitioner_name = sys.argv[1]
    if not hasattr(config, practitioner_name):
        print(f"praticien '{practitioner_name}' non trouvé dans config.py")
        sys.exit(1)

    practitioner = getattr(config, practitioner_name)
    run_scheduler(practitioner)
