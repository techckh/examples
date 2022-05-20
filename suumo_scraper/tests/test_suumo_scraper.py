import os
import json
import time
import requests
import pandas as pd

from suumo_scraper.for_sale import download_for_sale_page, download_all_pages, parse_for_sale_listing
from suumo_scraper.for_sale import parse_input_options
from suumo_scraper.utils import get_wiki_coordinates, parse_wiki_subway_page


def test_parse_for_sale_listing():
    trade_date = '20220516'
    all_data = dict()
    files = os.listdir('../data/%s' % trade_date)
    for file in files:
        if not file.startswith('for_sale_131'):
            continue
        print('parsing {}'.format(file))
        with open('../data/{}/{}'.format(trade_date, file), 'r', encoding='utf8') as f:
            html_str = f.read()
        data = parse_for_sale_listing(html_str)
        for key in data:
            if key in all_data:
                assert False, 'duplicate key, %s' % key
            all_data[key] = data[key]

    print(len(all_data))
    with open('../data/%s_all_listings.json' % trade_date, 'w', encoding='utf8') as f:
        f.write(json.dumps(all_data, indent=2, ensure_ascii=False))


def test_parse_input_options():
    filename = 'data/tokyo_listings_query_page.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    data = parse_input_options(html_str, 'checkbox', 'sc')
    ward_count = 0
    for name in data:
        sc = data[name][0]
        count = data[name][1]
        if int(sc) > 13200:
            continue
        total_pages = int(count/100)+1
        print(ward_count, name, sc, count, total_pages)
        ward_count += 1
        #download_all_pages(sc, total_pages=total_pages)


def test_get_wiki_coordinates():
    filename = 'data/wiki_ebisu_station.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    lat, lon = get_wiki_coordinates(html_str)
    print(lat, lon)
    assert lat == 35.641333333333336
    assert lon == 139.706


def test_get_wiki_coordinates_url():
    url = 'https://en.wikipedia.org/wiki/Shinagawa_Station'
    res = requests.get(url)
    assert res.status_code == 200
    lat, lon = get_wiki_coordinates(res.text)
    print(lat, lon)
    assert lat == 35.62383333333333
    assert lon == 139.73683333333332

    url = 'https://en.wikipedia.org/wiki/Shinjuku_Station'
    res = requests.get(url)
    assert res.status_code == 200
    lat, lon = get_wiki_coordinates(res.text)
    print(lat, lon)
    assert lat == 35.689475
    assert lon == 139.700349


def test_parse_wiki_subway_page():
    filename = 'data/wiki_yamanote_line.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    stations = parse_wiki_subway_page(html_str)
    for key in stations:
        print(key)
    df = pd.DataFrame({'station': stations.keys(), 'url': stations.values()})
    df['url'] = df['url'].apply(lambda x:'https://en.wikipedia.org%s' % x)

    lat_list = list()
    lon_list = list()
    for url in stations.values():
        url = 'https://en.wikipedia.org%s' % url
        res = requests.get(url)
        assert res.status_code == 200
        lat, lon = get_wiki_coordinates(res.text)
        lat_list.append(lat)
        lon_list.append(lon)
        print(url, lat, lon)
        time.sleep(3)

    df['lat'] = lat_list
    df['lon'] = lon_list
    print(df.head())
    pd.to_pickle(df, 'data/tokyo_yamanote_line.pkl')
