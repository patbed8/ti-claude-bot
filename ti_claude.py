import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Tokens via variables d'environnement
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    say("📬 Nouvelles du jour disponibles !")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("Ti-Claude est en ligne ✅")
    handler.start()
