import time
import requests
from lxml import etree


def get_new_listings(old_data, new_data):
    assert type(old_data) == dict, 'error type'
    assert type(new_data) == dict, 'error type'
    diff = list(set(new_data) - set(old_data))
    return diff


def parse_input_options(html_str, input_type, input_name):
    tree = etree.HTML(html_str)
    rows = tree.xpath(".//input[@type='{}' and @name='{}']".format(input_type, input_name))
    data = dict()
    for row in rows:
        name = row.attrib['name']
        assert name == 'sc', 'error name, %s' % name
        nexts = row.xpath('following-sibling::*')
        if len(nexts):
            next = nexts[0]
            if next.tag == 'label':
                label = next.text.strip()
                ward_code = row.attrib['value']
                if ward_code == '13102':
                    d = True
                try:
                    tmp = next.xpath('.//span')[0].text
                    listing_count = int(tmp.replace(',', '').replace('(', '').replace(')', ''))
                except Exception as ex:
                    listing_count = 0
                data[label] = [ward_code, listing_count]
    return data


def download_for_sale_page(sc, page_num):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    #url = 'https://suumo.jp/jj/bukken/ichiran/JJ012FC002/?ar=030&bknlistmodeflg=2&bs=011&cn=9999999&cnb=0&ekTjCd=&ekTjNm=&kb=1&kt=9999999&mb=0&mt=9999999&sc={}&ta=13&tj=0&pc=100&po=1&pj=2&pn={}'.format(sc, page_num)
    url = 'https://suumo.jp/jj/bukken/ichiran/JJ012FC002/?ar=030&bknlistmodeflg=2&bs=011&cn=9999999&cnb=0&ekTjCd=&ekTjNm=&kb=1&kr=A&kt=9999999&mb=0&md=1&mt=9999999&sc={}&ta=13&tj=0&po=0&pj=1&pc=100&pn={}'.format(sc, page_num)
    print(url)
    res = requests.get(url, headers=headers)
    assert res.status_code == 200, 'error status code, %s' % res.status_code
    return res.text


def download_all_pages(sc, total_pages):
    for i in range(1, total_pages+1):
        try_count = 3
        while try_count:
            try:
                print('downloading page {} of {}'.format(i, total_pages))
                txt = download_for_sale_page(sc, i)
                with open('data/for_sale_{}_{}.txt'.format(sc, i), 'w', encoding='utf8') as f:
                    f.write(txt)
                time.sleep(3)
                break
            except Exception as ex:
                print(ex)
                try_count -= 1
                time.sleep(3*try_count)
        assert try_count, 'max try count'


def parse_for_sale_listing(html_str):
    tree = etree.HTML(html_str)
    rows = tree.xpath("//div[@id='js-bukkenList']/div")

    data = dict()
    for row in rows:
        listing = dict()
        main = row.xpath("./div")[1]
        header = main.xpath("./div")[0]
        link = header.xpath("./h2/a")[0]
        listing['name'] = link.text
        listing['url'] = link.attrib['href']
        detail_divs = row.xpath("./div[2]/div[2]/div/div[2]/div/div")
        for div in detail_divs:
            tables = div.xpath('./table')
            assert len(tables) == 1, 'error table'
            table = tables[0]
            trs = table.xpath('.//tr')
            for tr in trs:
                tds = tr.xpath('.//td')
                if len(tds) == 1:
                    listing['notes'] = tds[0].text
                elif len(tds) == 2:
                    title = None
                    dd = ''
                    for td in tds:
                        dts = td.xpath('.//dt')
                        if dts:
                            title = dts[0].text
                            #print(title)
                        dds = td.xpath('.//dd')
                        if dds:
                            if title == '販売価格':
                                dd = dds[0].xpath('.//span')[0].text
                            else:
                                dd = dds[0].text
                            #print(data)
                        if title:
                            listing[title] = dd
        assert listing['url'] not in data, '%s already in data' % listing['url']
        data[str(listing['url'])] = listing
    return data
