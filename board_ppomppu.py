import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import visited_files as vu

# 요청할 URL
base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
page_url = "https://www.ppomppu.co.kr/zboard/zboard.php?"

def parse_num(value):
    try:
        return int(value)
    except ValueError:
        return 0


def convert_m_page(full_link):
    return full_link.replace('www.ppomppu', 'm.ppomppu') \
        .replace('/zboard', '') \
        .replace('view.php', 'new/bbs_view.php')


def append_list(found_list, link, title, visited_urls):
    full_link = urljoin(page_url, link)
    if full_link in visited_urls:
        return  # 이미 방문한 링크는 건너뛰기

    m_link = convert_m_page(full_link)
    found_list.append(
        {"title": title, "url": m_link}
    )
    # Add the visited link to the set
    visited_urls.add(full_link)


def find_keyword(search_keyword, visited_urls_file='visited_urls_ppomppu.txt'):
    visited_urls = vu.visited_urls_open(visited_urls_file)

    # 페이지 요청
    response = requests.get(base_url)
    print(f">>> ppomppu\tlist http status : {response.status_code}")
    # 응답 확인
    if response.status_code == 200:
        # BeautifulSoup을 이용해 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 게시물 리스트 테이블 찾기
        rows = soup.find_all(class_='baseList bbs_new1')
        # print(rows)
        # 게시물 정보 추출
        search_keyword_list = search_keyword.split(",")
        # print(search_keyword_list)
        found_list = []
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
                comment = "0"
                if(comment_obj):
                    comment = comment_obj.text
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
                    comment = "0"
                    if(comment_obj):
                        comment = comment_obj.text

                    # 키워드
                    for search_keyword in search_keyword_list:
                        if (search_keyword.casefold() in title.casefold()):
                            append_list(found_list, link, title, visited_urls)
                    # 코멘트
                    comment_cnt = int(comment)
                    if(comment_cnt >= 10):
                        append_list(found_list, link, title, visited_urls)

                    # 결과 출력
                    # print(f"번호:{num}, 제목:{title}")
                    # print(f"번호: {num}, 제목: {title}, 댓글: {comment}, 글쓴이: {author}, 등록일: {date}, 추천: {good}/{bad}, 조회: {views}")
            except Exception as e:
                print(e)
                pass
    else:
        print("페이지 요청 실패")

    vu.visited_urls_save(visited_urls_file, visited_urls)

    return found_list


if __name__ == "__main__":
    search_keyword = "cdhc"
    found_list = find_keyword(search_keyword)
    if(len(found_list) > 0):
        print(found_list)