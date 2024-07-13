from requests import post, Response
import sys

# SLACK 설정
SLACK_API_URL = "https://slack.com/api/chat.postMessage"
MESSAGE = "Hello World"

def send_message(slack_bot_token, slack_channel, message: str) -> Response:
    payload = {
        "text": f"> \n{message}",
        "channel": slack_channel,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {slack_bot_token}",
    }
    res = post(SLACK_API_URL, json=payload, headers=headers)
    print(f">>> slack\tsend http status : {res.status_code}")
    return res


if __name__ == "__main__":
    SLACK_BOT_TOKEN = sys.argv[1]
    SLACK_CHANNEL = sys.argv[2]
    if(None != sys.argv[3]):
        MESSAGE = sys.argv[3]

    send_message(SLACK_BOT_TOKEN, SLACK_CHANNEL, MESSAGE)