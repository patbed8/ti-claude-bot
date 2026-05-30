import os
import time
import requests

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
CHANNEL_ID = "C0B5SV0GVC0"  # #actu
LOOKBACK_SECONDS = 6 * 60 * 60   # 6 heures

def join_channel():
    requests.post(
        "https://slack.com/api/conversations.join",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={"channel": CHANNEL_ID}
    )

def build_notification(text):
    alerts = text.count(":rotating_light:")
    news = text.count(":pushpin:")

    if alerts > 0 and news > 0:
        alerte_str = f"{alerts} alerte{'s' if alerts > 1 else ''}"
        news_str = f"{news} nouvelle{'s' if news > 1 else ''}"
        return f"📬 {alerte_str} et {news_str}!"
    elif alerts > 0:
        return f"📬 {alerts} alerte{'s' if alerts > 1 else ''}!"
    elif news > 0:
        return f"📬 {news} nouvelle{'s' if news > 1 else ''}!"
    else:
        return "📬 Nouvelles du jour!"

def check_recent_actualite():
    oldest = str(time.time() - LOOKBACK_SECONDS)
    response = requests.get(
        "https://slack.com/api/conversations.history",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        params={"channel": CHANNEL_ID, "oldest": oldest, "limit": 20}
    )
    data = response.json()

    if not data.get("ok"):
        print(f"Erreur Slack API : {data.get('error')}")
        return None

    for msg in data.get("messages", []):
        text = msg.get("text", "")
        if "Actualit" in text:
            print(f"Actualité détectée.")
            notification = build_notification(text)
            print(f"Message : {notification}")
            return notification

    print("Aucune actualité trouvée dans les 6 dernières heures.")
    return None

def send_notification(message):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message}
    )
    if response.status_code == 200:
        print("Notification envoyée avec succès.")
    else:
        print(f"Erreur webhook : {response.status_code} — {response.text}")

if __name__ == "__main__":
    join_channel()
    notification = check_recent_actualite()
    if notification:
        send_notification(notification)