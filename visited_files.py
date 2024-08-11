def visited_urls_open(site_id):
    visited_urls_file = "visited_urls_" + site_id + ".txt"
    try:
        file = open(visited_urls_file, 'r')
        visited_urls = set(file.read().splitlines())
    except FileNotFoundError:
        print(f'{visited_urls_file} file not found')
        visited_urls = set()

    return visited_urls


def visited_urls_save(site_id, visited_urls):
    visited_urls_file = "visited_urls_" + site_id + ".txt"
    file = open(visited_urls_file, 'w')
    for url in visited_urls:
        file.write(url + '\n')