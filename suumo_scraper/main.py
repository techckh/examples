import json
from suumo_scraper.for_sale import download_for_sale_page, download_all_pages, parse_for_sale_listing
from suumo_scraper.for_sale import parse_input_options


if __name__ == '__main__':
    filename = 'data/tokyo_listings_query_page.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    data = parse_input_options(html_str, 'checkbox', 'sc')
    start = False
    for name in data:
        sc = data[name][0]
        count = data[name][1]
        if int(sc) > 13200:
            continue

        if int(sc) == 13109:
            start = True

        if not start:
            continue
        print(name, sc, count)
        total_pages = int(count / 100) + 1
        download_all_pages(sc, total_pages=total_pages)
