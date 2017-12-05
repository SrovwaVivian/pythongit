# coding:utf-8
from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import random
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
ganjidata = ganji['ganjidata']


# proxy_list = [
#     'http://42.49.119.225:8118',
#     'http://153.99.16.84:8118',
#     'http://183.130.155.105:8118'
# ]
# proxy_ip = random.choice(proxy_list)
# proxies = {'http': proxy_ip}


def get_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    try:
        wb_data = requests.get(url, headers=headers, timeout=10)
    except TimeoutError:
        print('请求超时')
        pass
    return wb_data


def get_channel_list():
    base_url = 'http://xinxiang.ganji.com'
    url = 'http://xinxiang.ganji.com/wu/'
    url_lists = []
    data = {}
    wb_data = get_response(url)
    soup = BeautifulSoup(wb_data.content, 'html.parser')
    categorys = list(map(lambda x: x.text.strip().split('\n'), soup.select('.fenlei dt')))
    categorys = sum(categorys, [])
    urls = list(map(lambda x: x.get('href'), soup.select('.fenlei dt a')))
    for category, url in zip(categorys, urls):
        url_lists.append(base_url + url)
        data[category] = url
    return url_lists


def get_every_list(url):
    page = 1
    while 1:
        time.sleep(.5)
        url = url + 'o{}'.format(page)
        try:
            wb_data = get_response(url)
            soup = BeautifulSoup(wb_data.content, 'html.parser')
        except:
            pass
        if len(soup.select('tr.zzinfo')) < 10:
            print('没有东西了')
            break
        titles = list(map(lambda x: x.text, soup.select('tr.zzinfo td.t a')))
        url_list = list(map(lambda x: x.get('href').split('?')[0], soup.select('tr.zzinfo td.t a')))
        prices = list(map(lambda x: x.text, soup.select('tr.zzinfo td.t span.price')))
        areas = list(map(lambda x: x.text.strip(), soup.select('tr.zzinfo td.t span.fl')))
        for t, u, p, a in zip(titles, url_list, prices, areas):
            data = {
                'title': t,
                'url': u,
                'price': p,
                'area': a
            }
            ganjidata.insert_one(data)
        page += 1
        print('下一页第%s页' % (page))


if __name__ == '__main__':
    pool = Pool(4)
    url_list = get_channel_list()

    pool.map(get_every_list, url_list)

    print('done!')
