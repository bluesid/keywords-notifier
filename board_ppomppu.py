import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from log_config import get_logger

logger = get_logger(__name__)
# 요청할 URL
base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
page_url = "https://www.ppomppu.co.kr/zboard/zboard.php?"


def parse_num(value):
    try:
        return int(value)
    except ValueError:
        return 0


def convert_link(full_link):
    # URL 파싱
    parsed_url = urlparse(full_link)
    # 쿼리 파라미터 추출
    params = parse_qs(parsed_url.query)
    # print(params)
    # id, page, divpage, no
    del params['page']
    del params['divpage']
    # 새 쿼리 문자열 생성
    new_query = urlencode(params, doseq=True)
    # 수정된 URL 생성
    new_link = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, new_query, parsed_url.fragment)
    )
    # print(new_link)
    # return new_link
    return new_link.replace(
        'www.ppomppu.co.kr/zboard/view',
        'm.ppomppu.co.kr/new/bbs_view')


def append_list(found_list, link, title, comment, good, bad):
    full_link = urljoin(page_url, link)
    m_link = convert_link(full_link)

    found_list.append(
        {
            "site": "뽐뿌",
            "site_id": "ppomppu",
            "title": title,
            "full_url": full_link,
            "m_url": m_link,
            "comment": comment,
            "good": good,
            "bad": bad
        }
    )


def find_keyword(search_keyword):
    # 페이지 요청
    response = requests.get(base_url)
    logger.info(f">>> ppomppu\tlist http status : {response.status_code}")

    found_list = []
    # 응답 확인
    if response.status_code == 200:
        # BeautifulSoup을 이용해 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 게시물 리스트 테이블 찾기
        rows = soup.find_all(class_='baseList bbs_new1')
        search_keyword_list = []
        if(search_keyword is not None):
            search_keyword_list = search_keyword.split(",")
        # print(search_keyword_list)
        # 게시물 정보 추출
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) == 7:  # 유효한 게시물 행인지 확인
                    continue

                # 번호, 제목, 글쓴이, 등록일, 추천, 조회 데이터 추출
                """
                num = cells[0].text.strip()
                title = cells[1].find('a', class_='baseList-title').text
                comment_obj = cells[1].find('span', class_='baseList-c')
                comment = 0
                if(comment_obj):
                    comment = int(comment_obj.text)
                link = cells[1].find('a', class_='baseList-title')['href']
                author = cells[2].find('span').text.strip()
                date = cells[3].get('title')
                recommend = cells[5].text.strip()
                good = 0
                bad = 0
                recommend = cells[4].text.split('-')
                if(len(recommend)>1):
                    good = recommend[0].strip()
                    bad = recommend[1].strip()
                views = cells[5].text.strip()
                """
                num = cells[0].text.strip()
                if(parse_num(num) > 0):
                    title = cells[1].find('a', class_='baseList-title').text
                    link = cells[1].find('a', class_='baseList-title')['href']
                    comment_obj = cells[1].find('span', class_='baseList-c')
                    comment = 0
                    if(comment_obj):
                        comment = int(comment_obj.text)
                    recommend = cells[5].text.strip()
                    good = 0
                    bad = 0
                    recommend = cells[4].text.split('-')
                    if(len(recommend)>1):
                        good = recommend[0].strip()
                        bad = recommend[1].strip()

                    append_list(
                        found_list,
                        link,
                        title,
                        comment,
                        good,
                        bad
                    )

                    # 결과 출력
                    # print(f"번호:{num}, 제목:{title}")
                    # print(f"번호: {num}, 제목: {title}, 댓글: {comment}, 글쓴이: {author}, 등록일: {date}, 추천: {good}/{bad}, 조회: {views}")
            except Exception as e:
                logger.error(f">>> ppomppu\texception : {e}")
                pass
    else:
        print("페이지 요청 실패")

    return found_list


if __name__ == "__main__":
    search_keyword = "cdhc"
    found_list = find_keyword(search_keyword)
    if(len(found_list) > 0):
        print(found_list)