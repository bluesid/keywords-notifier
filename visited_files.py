def visited_urls_open(visited_urls_file):
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    return visited_urls


def visited_urls_save(visited_urls_file, visited_urls):
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')