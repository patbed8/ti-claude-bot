import os
import time
import requests

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
CHANNEL_ID = "C0B5SV0GVC0"  # #actu
LOOKBACK_SECONDS = 40 * 60   # 40 minutes

def join_channel():
    response = requests.post(
        "https://slack.com/api/conversations.join",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={"channel": CHANNEL_ID}
    )
    data = response.json()
    print(f"Join canal : ok={data.get('ok')}, error={data.get('error', 'aucune')}")

def check_recent_actualite():
    oldest = str(time.time() - LOOKBACK_SECONDS)
    print(f"Recherche depuis : {oldest} (maintenant : {time.time()})")

    response = requests.get(
        "https://slack.com/api/conversations.history",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        params={"channel": CHANNEL_ID, "oldest": oldest, "limit": 20}
    )
    data = response.json()
    print(f"Réponse API : ok={data.get('ok')}, error={data.get('error', 'aucune')}")
    print(f"Messages trouvés : {len(data.get('messages', []))}")

    for msg in data.get("messages", []):
        text = msg.get("text", "")
        print(f"  → {text[:80]}")
        if "🗞️ Actualité" in text:
            print("Actualité détectée — envoi notification.")
            return True

    print("Aucune actualité trouvée.")
    return False

def send_notification():
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": "📬 Nouvelles du jour!"}
    )
    if response.status_code == 200:
        print("Notification envoyée avec succès.")
    else:
        print(f"Erreur webhook : {response.status_code} — {response.text}")

if __name__ == "__main__":
    join_channel()
    if check_recent_actualite():
        send_notification()