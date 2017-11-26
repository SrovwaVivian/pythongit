#!usr/bin/env python
# coding:utf-8
import requests, re
from bs4 import BeautifulSoup

start_url = 'https://movie.douban.com/top250'

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    try:
        html = requests.get(url, headers=headers).content
    except TimeoutError:
        raise ('请求超时')
    # print (html)
    return html


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('ol', class_='grid_view')
    data_list = data.find_all('li')

    for li in data_list:
        name = li.find('span', class_='title').get_text()
        act = li.find('p', class_='').get_text().strip()
        star = li.find('span', class_='rating_num').get_text()
        num = li.find(text=re.compile('评价'))
        inq = li.find('span', class_='inq').get_text()
        # print(name, act, star, num, inq)

        with open('douban_movie.txt', 'a') as f:
            f.write(name + ' ' + star + ' ' + num + ' ' + inq + '\n' + act + '\n')

    page = soup.find('span', class_='next').find('a')
    if page is not None:
        next_page = page['href']
        return start_url + next_page
    print('没有下一页了')
    return None

url = start_url
while url:
    html = get_html(url)
    url = get_data(html)

print('读取完成')
