import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import visited_files as vu

base_url = "https://www.clien.net/service/board/jirum"


def convert_m_page(full_link):
    return full_link.replace(
        'www.clien',
        'm.clien')


def append_list(found_list, link, title, visited_urls):
    full_link = urljoin(base_url, link)
    if full_link in visited_urls:
        return  # 이미 방문한 링크는 건너뛰기

    m_link = convert_m_page(full_link)
    found_list.append(
        {"title": title, "url": m_link}
    )
    # Add the visited link to the set
    visited_urls.add(full_link)


def find_keyword(search_keyword, visited_urls_file='visited_urls_clien.txt'):
    visited_urls = vu.visited_urls_open(visited_urls_file)

    # 페이지 요청
    response = requests.get(base_url)
    print(f">>> clien\tlist http status : {response.status_code}")

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
                views = row.find('span', class_='hit').text.strip()
                """
                title = row.find('span', class_='list_subject')['title'].strip()
                link = row.find('span', class_='list_subject').find('a')['href']
                comment_obj = row.find('span', class_='rSymph05')
                comment = 0
                if(comment_obj):
                    comment = int(comment_obj.text)

                # 키워드
                for search_keyword in search_keyword_list:
                    if (search_keyword.casefold() in title.casefold()):
                        append_list(found_list, link, title, visited_urls)
                # 코멘트
                if(comment >= 10):
                    append_list(found_list, link, title, visited_urls)

                # 결과 출력
                # print(f"제목:{title}")
                # print(f"제목: {title}, 댓글: {comment}, 글쓴이: {author}, 등록일: {date}, 추천: {good}, 조회: {views}")
            except Exception as e:
                print(e)
                pass
    else:
        print("페이지 요청 실패")

    vu.visited_urls_save(visited_urls_file, visited_urls)

    return found_list


if __name__ == "__main__":
    search_keyword = "크록스"
    found_list = find_keyword(search_keyword)
    if(len(found_list) > 0):
        print(found_list)