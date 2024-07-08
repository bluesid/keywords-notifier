import sys
import board_ppomppu as ppomppu
import slack as s

def main(search_keyword):
    found_list = []
    found_list += ppomppu.find_keyword(search_keyword)

    for found in found_list:
        msg = f"{found['title']}\r\n{found['url']}\r\n"
        response = s.send_message(SLACK_BOT_TOKEN, SLACK_CHANNEL, msg)
        print(f"slack send STATUS : {response.status_code}")


if __name__ == "__main__":
    SLACK_BOT_TOKEN = sys.argv[1]
    SLACK_CHANNEL = sys.argv[2]
    search_keyword = sys.argv[3]
    main(search_keyword)