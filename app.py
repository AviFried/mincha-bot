from flask import Flask, request
import requests
import os

app = Flask(__name__)

ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

poll_totals = {}


def send_message(text):
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": CHAT_ID, "message": text}
    requests.post(url, json=payload)


def send_mincha_poll():
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendPoll/{API_TOKEN}"
    payload = {
        "chatId": CHAT_ID,
        "message": "Mincha Minyan — who can come today?",
        "options": ["Out", "+1", "+2", "+3"],
        "multipleAnswers": False
    }
    r = requests.post(url, json=payload)
    return r.json()


@app.route("/", methods=["GET"])
def health():
    return "Mincha bot running."


@app.route("/send_poll", methods=["GET"])
def manual_trigger():
    result = send_mincha_poll()
    return {"status": "poll_sent", "response": result}


@app.route("/poll", methods=["GET"])
def poll_webhook():
    data = request.json

    if not data or data.get("typeWebhook") != "incomingPollUpdateMessageReceived":
        return "ignored"

    poll = data["messageData"]["pollUpdateMessage"]
    poll_id = poll["pollId"]

    total = 0

    for option in poll["options"]:
        name = option["name"]
        voters = option.get("voters", [])

        if name == "Out":
            continue

        if name.startswith("+"):
            multiplier = int(name[1:])
            total += multiplier * len(voters)

    poll_totals[poll_id] = total

    if total >= 10:
        send_message("Mincha is ON today. We reached a Minyan.")
        print("Announcement sent.")

    print("Current total:", total)
    return "ok"
