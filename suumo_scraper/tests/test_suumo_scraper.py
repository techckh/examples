import os
import json
from suumo_scraper.for_sale import download_for_sale_page, download_all_pages, parse_for_sale_listing
from suumo_scraper.for_sale import parse_input_options


def test_parse_for_sale_listing():
    all_data = dict()
    files = os.listdir('../data')
    for file in files:
        if not file.startswith('for_sale_131'):
            continue
        print('parsing {}'.format(file))
        with open('../data/{}'.format(file), 'r', encoding='utf8') as f:
            html_str = f.read()
        data = parse_for_sale_listing(html_str)
        for key in data:
            if key in all_data:
                assert False, 'duplicate key, %s' % key
            all_data[key] = data[key]

    print(len(all_data))
    with open('../data/all_listings.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(all_data, indent=2, ensure_ascii=False))


def test_parse_input_options():
    filename = 'data/tokyo_listings_query_page.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    data = parse_input_options(html_str, 'checkbox', 'sc')
    for name in data:
        sc = data[name][0]
        count = data[name][1]
        if int(sc) > 13200:
            continue
        print(name, sc, count)
        total_pages = int(count/100)+1
        download_all_pages(sc, total_pages=total_pages)

