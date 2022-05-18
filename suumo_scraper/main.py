import json
import pandas as pd
import re

from suumo_scraper.for_sale import download_for_sale_page, download_all_pages, parse_for_sale_listing
from suumo_scraper.for_sale import parse_input_options, get_new_listings


pattern = re.compile(r'\「(.*?)\」')


def download_data():
    filename = 'data/tokyo_listings_query_page.html'
    with open(filename, 'r', encoding='utf8') as f:
        html_str = f.read()
    data = parse_input_options(html_str, 'checkbox', 'sc')
    start = True
    ward_count = 0
    for name in data:
        sc = data[name][0]
        count = data[name][1]
        if int(sc) > 13200:
            continue

        """
        if int(sc) == 13109:
            start = True
        """

        if not start:
            continue

        print(ward_count, name, sc, count)
        ward_count += 1
        total_pages = int(count / 100) + 1
        download_all_pages(sc, total_pages=total_pages)


def generate_df(trade_date):
    with open('data/{}_all_listings.json'.format(trade_date), 'r', encoding='utf8') as f:
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


"""
def convert_balcony(x):
    try:
        x = x.replace('m', '').replace('㎡', '')
        return float(x)
    except Exception as ex:
        items = x.split('～')
        if len(items) > 1:
            return float(items[1].replace('㎡', ''))
    assert False, 'unknown error'
"""


def convert_price(x):
    if '～' in x or '・' in x:
        x = x.replace('～', '-').replace('・', '-')
        items = x.split('-')
        val = float(items[1].replace('万円', '').replace('億', ''))
    else:
        val = float(x.replace('万円', '').replace('億', '').replace('円', ''))
    return val


def convert_balcony(x):
    if '～' in x:
        parts = x.split('～')
        x = parts[-1]
        val = float(x.replace('㎡', '').replace('-', '0').strip())
    else:
        val = float(x.replace('m', '').replace('-', '0').strip())
    return val


def convert_area(x):
    x = x.replace('東京都', '').split('区')[1]
    x = x.replace('-', '').replace('－', '').strip()
    val = re.sub(r'\d+', '', x)
    return val


def convert_station(x):
    matched = re.search(pattern, x)
    if matched:
        span = matched.span()
        subway_line = x[0:span[0]]
        val = matched.group()
        walking = x[span[1]:]
        # bus 1 mi is 300m, walking 1 min is 80m
        if walking.startswith('バス'):
            walking_time = int(walking.split('停歩')[-1].replace('分', ''))*4
        else:
            walking_time = int(walking.replace('徒歩', '').replace('分', ''))
        val = val.replace('「', '').replace('」', '')
        return subway_line, val, walking_time
    return '', '', 0


def convert_built_year(x):
    parts = x.split('年')
    year = str(parts[0])
    month = int(parts[1].replace('月', ''))
    return year, month


def clean_suumo_data(df):

    """
    ['name', 'url', 'notes', '販売価格', '専有面積', '所在地', 'バルコニー', '沿線・駅', '間取り',
       '築年月', 'id']
    """

    df['id'] = df['url'].apply(lambda x: x.split('_')[-1].replace('.html', ''))
    df = df.drop(' ', axis=1)
    df = df.drop('notes', axis=1)
    df = df.drop('url', axis=1)
    df.sort_values(by=['name'], inplace=True)

    new_list = list()
    cur_name = None
    cur_built_year = None
    cur_size = None
    for index, row in df.iterrows():
        new_name = row['name']
        new_built_year = row['築年月']
        new_size = row['専有面積']

        if cur_name == None:
            cur_name = new_name
            cur_built_year = new_built_year
            cur_size = new_size
            new_list.append(row.values)
            continue

        if new_name != cur_name:
            cur_name = new_name
            cur_built_year = new_built_year
            cur_size = new_size
            new_list.append(row.values)
            continue

        if new_name == cur_name:
            if new_built_year != cur_built_year or new_size != cur_size:
                new_list.append(row.values)

    df = pd.DataFrame(new_list, columns=df.columns)
    df['バルコニー'] = df['バルコニー'].fillna('0')
    df['バルコニー'] = df['バルコニー'].apply(convert_balcony)
    df['バルコニー'] = df['バルコニー'].astype(float)

    df['専有面積'] = df['専有面積'].fillna('0')
    df['専有面積'] = df['専有面積'].apply(lambda x: float(x.replace('m', '')))
    df['専有面積'] = df['専有面積'].astype(float)

    col = '販売価格'
    df[col] = df[col].fillna('0')
    df[col] = df[col].apply(convert_price)
    df[col] = df[col].astype(float)

    df['ward'] = df['所在地'].apply(lambda x: '%s区'%x.replace('東京都', '').split('区')[0])
    df['area'] = df['所在地'].apply(convert_area)
    df['subway'], df['station'], df['walking'] = zip(*df['沿線・駅'].apply(convert_station))
    df['built_year'], df['built_month'] = zip(*df['築年月'].apply(convert_built_year))

    assert df.isnull().values.any() == False
    return df


def clean_data():
    trade_date = '20220510'
    old_df = pd.read_pickle('{}_all_listing.pkl'.format(trade_date))
    trade_date = '20220516'
    new_df = pd.read_pickle('{}_all_listing.pkl'.format(trade_date))
    df = pd.concat([old_df, new_df])
    df = clean_suumo_data(df)
    df.to_pickle('{}_filtered.pkl'.format(trade_date))


def convert_to_pickle():
    with open('data/20220510_all_listings.json', 'r', encoding='utf8') as f:
        data = f.read()
    old_data = json.loads(data)

    with open('data/20220516_all_listings.json', 'r', encoding='utf8') as f:
        data = f.read()
    new_data = json.loads(data)

    trade_date = '20220510'
    old_df = generate_df(trade_date)
    old_df.to_pickle('{}_all_listing.pkl'.format(trade_date))

    trade_date = '20220516'
    new_df = generate_df(trade_date)
    new_df.to_pickle('{}_all_listing.pkl'.format(trade_date))


if __name__ == '__main__':

    """
    df = generate_df()
    df = df.drop([' '], axis=1)
    df['url'] = df['url'].apply(lambda x: convert_url(x))
    df['専有面積'] = df['専有面積'].apply(lambda x: float(x.replace('m', '')))
    df['バルコニー'] = df['バルコニー'].apply(lambda x: 0.0 if x == '-' else convert_balcony(x))
    df['ratio'] = df['バルコニー'] / df['専有面積']
    df.sort_values(by=['ratio'], ascending=False, inplace=True)
    df.to_csv('data/test.csv')    
    """

    """
    # https://suumo.jp/ms/chuko/tokyo/city/
    # need to copy the dom source
    download_data()
    print('done')
    """

    # convert_to_pickle()
    # clean_data()
    # diff = get_new_listings(old_data, new_data)
