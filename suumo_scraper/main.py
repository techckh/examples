import json
import pandas as pd

from suumo_scraper.for_sale import download_for_sale_page, download_all_pages, parse_for_sale_listing
from suumo_scraper.for_sale import parse_input_options


def download_data():
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


def generate_df():
    with open('data/20220510_all_listings.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())

    data_list = list()
    for key in data:
        d = data[key]
        d[' '] = ''
        data_list.append(d)

    df = pd.DataFrame.from_records(data_list)
    return df


def convert_url(x):
    return 'https://suumo.jp/%s' % x


def convert_balcony(x):
    try:
        x = x.replace('m', '').replace('㎡', '')
        return float(x)
    except Exception as ex:
        items = x.split('～')
        if len(items) > 1:
            return float(items[1].replace('㎡', ''))
    assert False, 'unknown error'


if __name__ == '__main__':
    df = generate_df()
    df = df.drop([' '], axis=1)
    df['url'] = df['url'].apply(lambda x: convert_url(x))
    df['専有面積'] = df['専有面積'].apply(lambda x: float(x.replace('m', '')))
    df['バルコニー'] = df['バルコニー'].apply(lambda x: 0.0 if x == '-' else convert_balcony(x))
    df['ratio'] = df['バルコニー'] / df['専有面積']
    df.sort_values(by=['ratio'], ascending=False, inplace=True)
    df.to_csv('data/test.csv')
    print('done')
