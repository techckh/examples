import time
import re
from lxml import etree


def ddm2dec(dms_str):
    """Return decimal representation of DDM (degree decimal minutes)

    >>> ddm2dec("45° 17,896' N")
    48.8866111111F
    """

    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute_decimal = numbers[1]
    decimal_val = numbers[2] if len(numbers) > 2 else '0'
    minute_decimal += "." + decimal_val

    return sign * (int(degree) + float(minute_decimal) / 60)


def find_lat_lon_01(span):
    span = span.xpath(".//span[@class='geo-dec']")
    if span:
        geo_text = span[0].text
        lat = geo_text.split(' ')[0]
        lon = geo_text.split(' ')[1]
        if "'" not in lat and '"' not in lat:
            lat = lat.replace('°', '').replace('N', '').replace('E', '').replace('S', '').replace('W', '')
            lon = lon.replace('°', '').replace('N', '').replace('E', '').replace('S', '').replace('W', '')
            return float(lat), float(lon)
        if lat and lon:
            return ddm2dec(lat), ddm2dec(lon)
    return None, None


def find_lat_lon_02(top):
    span = top.xpath(".//span[@class='latitude']")
    lat = None
    lon = None
    if span:
        lat = span[0].text
    span = top.xpath(".//span[@class='longitude']")
    if span:
        lon = span[0].text
    return ddm2dec(lat), ddm2dec(lon)


def get_wiki_coordinates(html_str):
    tree = etree.HTML(html_str)

    lat = None
    lon = None
    span = tree.xpath(".//span[@class='geo-default']")
    if span:
        lat, lon = find_lat_lon_01(span[0])
        if not lat or not lon:
            lat, lon = find_lat_lon_02(span[0])
        if lat and lon:
            return lat, lon

    span = tree.xpath(".//span[@class='latitude']")
    lat = None
    lon = None
    if span:
        lat = span[0].text
    span = tree.xpath(".//span[@class='longitude']")
    if span:
        lon = span[0].text

    span = tree.xpath(".//span[@class='geo-dec']")
    """
    ths = tree.xpath(".//th[@class='infobox-label']")
    data = dict()
    for th in ths:
        if th.text == 'Coordinates':
            td = th.xpath('.//following-sibling::td')
            if td:
                td = td[0]
            links = td.xpath('.//a[@class="external text"]')
            for link in links:
                url = link.attrib['href']
                if url.startswith('//geohack'):
                    parts = url.split('&')
                    params = parts[1].split(':')
                    lat = params[0].split('_N_')[0].replace('params=', '')
                    lon = params[0].split('_N_')[1].replace('_E_region', '')
                    return lat, lon
    """

    if not lat or not lon:
        return None, None
    return ddm2dec(lat), ddm2dec(lon)


def parse_wiki_subway_page(html_str):
    tree = etree.HTML(html_str)

    tables = tree.xpath(".//table")
    target_table = None
    for table in tables:
        ths = table.xpath('.//th')
        for th in ths:
            if str(th.text).strip() == 'Line name':
                print(len(ths))
                target_table = table
                break

    stations = dict()
    trs = target_table.xpath('.//tr')
    for tr in trs:
        tds = tr.xpath('.//td')
        if len(tds)>=3:
            link = tds[1].xpath('.//a')
            if link:
                link = link[0]
                stations[link.text] = link.attrib['href']
            else:
                # first tr
                link = tds[2].xpath('.//a')
                link = link[0]
                stations[link.text] = link.attrib['href']
    return stations
