import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from log_config import get_logger

logger = get_logger(__name__)
# 요청할 URL
base_url = "https://www.clien.net/service/board/jirum"


def convert_link(full_link):
    # URL 파싱
    parsed_url = urlparse(full_link)
    # 쿼리 파라미터 추출
    params = parse_qs(parsed_url.query)
    # print(params)
    # od, po, category
    del params['od']
    del params['po']
    del params['category']
    # 새 쿼리 문자열 생성
    new_query = urlencode(params, doseq=True)
    # 수정된 URL 생성
    new_link = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, new_query, parsed_url.fragment)
    )
    # print(new_link)
    # return new_link
    return full_link.replace(
        'www.clien',
        'm.clien')


def append_list(found_list, link, title, comment, good, bad):
    full_link = urljoin(base_url, link)
    m_link = convert_link(full_link)
    found_list.append(
        {
            "site": "클리앙",
            "site_id": "clien",
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
    logger.info(f">>> clien\tlist http status : {response.status_code}")

    found_list = []
    # 응답 확인
    if response.status_code == 200:
        # BeautifulSoup을 이용해 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 게시물 리스트 테이블 찾기
        rows = soup.find_all(class_='list_item symph_row jirum')
        search_keyword_list = []
        if(search_keyword is not None):
            search_keyword_list = search_keyword.split(",")
        # print(search_keyword_list)
        # 게시물 정보 추출
        for row in rows:
            try:
                """
                title = row.find('span', class_='list_subject')['title'].strip()
                comment_obj = row.find('span', class_='rSymph05')
                comment = 0
                if(comment_obj):
                    comment = int(comment_obj.text)
                link = row.find('span', class_='list_subject').find('a')['href']
                author = row.find('span', class_='nickname').text.strip()
                date = row.find('span', class_='timestamp').text.strip()
                good = row.find('div', class_='list_symph').text.strip()
                bad = 0
                views = row.find('span', class_='hit').text.strip()
                """
                title = row.find('span', class_='list_subject')['title'].strip()
                link = row.find('span', class_='list_subject').find('a')['href']
                comment_obj = row.find('span', class_='rSymph05')
                comment = 0
                if(comment_obj):
                    comment = int(comment_obj.text)
                good = row.find('div', class_='list_symph').text.strip()
                bad = 0

                append_list(
                    found_list,
                    link,
                    title,
                    comment,
                    good,
                    bad
                )

                # 결과 출력
                # print(f"제목:{title}")
                # print(f"제목: {title}, 댓글: {comment}, 글쓴이: {author}, 등록일: {date}, 추천: {good}, 조회: {views}")
            except Exception as e:
                logger.error(f">>> clien\texception : {e}")
                pass
    else:
        print("페이지 요청 실패")

    return found_list


if __name__ == "__main__":
    search_keyword = "크록스"
    found_list = find_keyword(search_keyword)
    if(len(found_list) > 0):
        print(found_list)