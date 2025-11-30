import requests
import os

ID_INSTANCE = os.getenv("ID_INSTANCE")
API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_mincha_poll():
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendPoll/{API_TOKEN}"
    payload = {
        "chatId": CHAT_ID,
        "message": "Mincha Minyan — who can come today?",
        "options": ["Out", "+1", "+2", "+3"],
        "multipleAnswers": False
    }
    r = requests.post(url, json=payload)
    print("Poll sent:", r.json())


if __name__ == "__main__":
    send_mincha_poll()
