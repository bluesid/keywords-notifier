import time
import argparse
import board_ppomppu as ppomppu
import board_clien as clien
import visited_files as vu
import slack as s

def finish_process(msg, send_list, full_url, site_id):
    send_or_print(msg)
    send_list.append(full_url)
    visited_urls = vu.visited_urls_open(site_id)
    visited_urls.add(full_url)
    vu.visited_urls_save(site_id, visited_urls)
    time.sleep(1)


def send_or_print(msg):
    if not ONLY_PRINT:
        s.send_message(SLACK_BOT_TOKEN, SLACK_CHANNEL, msg)
    else:
        print(msg)


def filtered_list(found_list, send_list, remove_keyword_list = []):
    # visited_urls
    filtered_list = []
    for found in found_list:
        visited_urls_file = "visited_urls_" + found['site_id'] + ".txt"
        visited_urls = vu.visited_urls_open(visited_urls_file)
        if found['full_url'] not in visited_urls:
            filtered_list.append(found)
    found_list = filtered_list

    # 이미 보낸 것
    filtered_list = []
    # 기존 리스트를 순회하면서 조건에 맞지 않는 항목들을 추가
    for found in found_list:
        if found['full_url'] not in send_list:
            filtered_list.append(found)
    found_list = filtered_list

    filtered_list = []
    for found in found_list:
        include = True
        for remove_keyword in remove_keyword_list:
            if remove_keyword.casefold() in found['title'].casefold():
                include = False
                break
        if include:
            filtered_list.append(found)
    found_list = filtered_list

    return found_list


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

    search_keyword_list = []
    if(search_keywords is not None):
        search_keyword_list = search_keywords.split(",")
    remove_keyword_list = []
    if(remove_keywords is not None):
        remove_keyword_list = remove_keywords.split(",")

    send_list = []
    found_list = filtered_list(found_list, send_list)
    for found in found_list:
        for search_keyword in search_keyword_list:
            # 키워드
            msg = f"{found['site']}, good : {found['good']}, keyword : {search_keyword}\r\n"
            if (search_keyword.casefold() in found['title'].casefold()):
                msg += f"{found['title']}\r\n{found['m_url']}\r\n"
                finish_process(msg, send_list, found['full_url'], found['site_id'])

    found_list = filtered_list(found_list, send_list, remove_keyword_list)
    send_list = []
    for idx, found in enumerate(found_list):
        # 좋아요
        msg = f"{found['site']}, good : {found['good']}, bad : {found['bad']}\r\n"
        if(int(found['good']) >= 10):
            msg += f"{found['title']}\r\n{found['m_url']}\r\n"
            finish_process(msg, send_list, found['full_url'], found['site_id'])

    found_list = filtered_list(found_list, send_list, remove_keyword_list)
    send_list = []
    for idx, found in enumerate(found_list):
        # 코멘트
        msg = f"{found['site']}, good : {found['good']}, comment : {found['comment']}\r\n"
        if(int(found['comment']) >= 10):
            msg += f"{found['title']}\r\n{found['m_url']}\r\n"
            finish_process(msg, send_list, found['full_url'], found['site_id'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sbt', type=str, required=False, help="slack bot token")
    parser.add_argument('--sc', type=str, required=False, help="slack channel")
    parser.add_argument('--p', type=str, required=False, help="search platform"
                        , default=None)
    parser.add_argument('--k', type=str, required=False, help="search keyword"
                        , default=None)
    parser.add_argument('--rk', type=str, required=False, help="remove keyword"
                        , default=None)
    args = parser.parse_args()

    ONLY_PRINT = False
    if(args.sbt is None or args.sc is None):
        # print('need a slack bot token and slack channel')
        # exit()
        ONLY_PRINT = True

    SLACK_BOT_TOKEN = args.sbt
    SLACK_CHANNEL = args.sc
    search_platforms = args.p
    search_keywords = args.k
    remove_keywords = args.rk
    main(search_keywords, search_platforms)