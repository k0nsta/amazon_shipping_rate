import re
import csv
import json

import requests


def format_price(raw_str):
    """
    Format price - remove all unecessary characters

    :param raw_str: string contains price data
    :type raw_str: unicode
    :return: clean-up price, only digits and delimiter
    :rtype: unicode
    """
    re_pattern = r'(([\.,]?\d+[ \.,]?(\d+))|\d+[\. ,]\d+([, .]\d+)?)'
    try:
        return re.search(re_pattern, raw_str).group()
    except AttributeError:
        return 'Error'


def load_initial_ulrs(csv_path, rescrape):
    """
    Url loader (csv)

    Load csv which contains prasing urls. According Ivan's gathered data or new one.
    One of usecase - rescrape urls hasn't had price value.
    Colums must have name: 'url' for rescrape options (according to project settings) or 'URL'
    for Ivan's data.

    :param csv_path: csv path
    :type csv_path: unicode
    :param rescrape: 0 or 1. Define from spider argument '-a'
    :type rescrape: int
    :return: list of urls
    :rtype: list
    """
    with open(csv_path) as csv_file:
        data = csv.DictReader(csv_file)
        if rescrape:
            urls = [url.get('url') for url in data if not url.get('price')]
        else:
            urls = [url.get('URL') for url in data]
        urls = [url.decode('utf-8') for url in urls]
    return urls


def get_from_proxyrotator():
    """
    Proxy API handler

    Proxy supplier API handler, each request return new proxy with predefine settings

    :return: proxy address
    :rtype: unicode
    """
    url = 'http://falcon.proxyrotator.com:51337/'
    params = dict(apiKey='6s4DvKjUdF5HV7BEeakbYo9x3TRMQWZS')

    resp = requests.get(url, params=params)
    proxy = json.loads(resp.text).get('proxy')
    if proxy:
        return 'http://{}'.format(proxy)