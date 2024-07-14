from requests import post, Response
import sys
from log_config import get_logger

logger = get_logger(__name__)
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
    response = post(SLACK_API_URL, json=payload, headers=headers)
    logger.info(f">>> slack\tsend http status : {response.status_code}")

    return response


if __name__ == "__main__":
    SLACK_BOT_TOKEN = sys.argv[1]
    SLACK_CHANNEL = sys.argv[2]
    if(None != sys.argv[3]):
        MESSAGE = sys.argv[3]

    send_message(SLACK_BOT_TOKEN, SLACK_CHANNEL, MESSAGE)