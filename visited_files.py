def visited_urls_open(site_id):
    visited_urls_file = "visited_urls_" + site_id + ".txt"
    try:
        with open(visited_urls_file, 'r') as file:
            visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        visited_urls = set()

    return visited_urls


def visited_urls_save(site_id, visited_urls):
    visited_urls_file = "visited_urls_" + site_id + ".txt"
    with open(visited_urls_file, 'w') as file:
        for url in visited_urls:
            file.write(url + '\n')