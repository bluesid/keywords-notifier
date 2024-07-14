import time
import argparse
import board_ppomppu as ppomppu
import board_clien as clien
import slack as s


def main(search_keywords, search_platforms):
    found_list = []

    search_platform_list = []
    if(search_platforms is not None):
        search_platform_list = search_platforms.split(",")
    else:
        search_platform_list.append("ppomppu")
        search_platform_list.append("clien")

    for platform in search_platform_list:
        if platform == "ppomppu":
            found_list += ppomppu.find_keyword(search_keywords)
        elif platform == "clien":
            found_list += clien.find_keyword(search_keywords)

    for found in found_list:
        msg = f"{found['title']}\r\n{found['url']}\r\n"
        s.send_message(SLACK_BOT_TOKEN, SLACK_CHANNEL, msg)
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sbt', type=str, required=True, help="slack bot token")
    parser.add_argument('--sc', type=str, required=True, help="slack channel")
    parser.add_argument('--p', type=str, required=False, help="search platform"
                        , default=None)
    parser.add_argument('--k', type=str, required=False, help="search keyword"
                        , default=None)
    args = parser.parse_args()

    if(args.sbt is None or args.sc is None):
        print('need a slack bot token and slack channel')
        exit()

    SLACK_BOT_TOKEN = args.sbt
    SLACK_CHANNEL = args.sc
    search_platforms = args.p
    search_keywords = args.k
    main(search_keywords, search_platforms)