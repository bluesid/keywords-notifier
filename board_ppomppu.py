import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
page_url = "https://www.ppomppu.co.kr/zboard/zboard.php?"

def find_keyword(search_keyword, visited_urls_file='visited_urls_ppomppu.txt'):
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    response = requests.get(base_url)
    print(f"ppomppu\tlist get HTTP STATUS : {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')

    list_subject_links = soup.find_all(class_='baseList-box')

    search_keyword_list = search_keyword.split(",")
    found_list = []
    for subject in list_subject_links:
        a_tag = subject.find('a', href=True)
        if a_tag:
            # print(a_tag.text)
            for search_keyword in search_keyword_list:
                if search_keyword.casefold() in a_tag.text.casefold():
                    full_link = urljoin(page_url, a_tag['href'])
                    found_list.append(
                        {"title": a_tag.text, "url": full_link}
                    )
                    # Add the visited link to the set
                    visited_urls.add(full_link)

    # Save the updated visited URLs to the file
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')

    return found_list


if __name__ == "__main__":
    search_keyword = "cdhc"
    found_list = find_keyword(search_keyword)
    if(len(found_list) > 0):
        print(found_list)