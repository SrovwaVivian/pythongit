#!usr/bin/env python
# coding:utf-8
# __author__ = 'afetmin'
import requests, re
from bs4 import BeautifulSoup
from openpyxl import Workbook

start_url = 'https://movie.douban.com/top250'


# 获取页面信息
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


# 获取电影信息
def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('ol', class_='grid_view')
    data_list = data.find_all('li')
    movie_name = []
    movie_act = []
    movie_star = []
    movie_num = []
    movie_inq = []
    for li in data_list:
        name = li.find('span', class_='title').get_text()
        act = li.find('p', class_='').get_text().strip()
        star = li.find('span', class_='rating_num').get_text()
        num = li.find(text=re.compile('评价'))
        inq = li.find('span', class_='inq').get_text()
        # print(name, act, star, num, inq)
        movie_name.append(name)  # 名字都放到一个列表里，其他信息同
        movie_act.append(act)
        movie_star.append(star)
        movie_num.append(num)
        movie_inq.append(inq)

        # with open('douban_movie.txt', 'a') as f:
        #     f.write(name + ' ' + star + ' ' + num + ' ' + inq + '\n' + act + '\n')

    page = soup.find('span', class_='next').find('a')
    if page is not None:
        next_page = page['href']
        return start_url + next_page, movie_name, movie_act, movie_star, movie_num, movie_inq
    print('没有下一页了')
    return None, movie_name, movie_act, movie_star, movie_num, movie_inq


# 循环写入xlsx文件
def result_xlsx():
    url = start_url
    name, act, star, num, inq = [], [], [], [], []
    while url:
        url, movie_name, movie_act, movie_star, movie_num, movie_inq = get_data(get_html(url))
        name = name + movie_name
        act = act + movie_act
        star = star + movie_star
        num = num + movie_num
        inq = inq + movie_inq

    wb = Workbook()
    filename = '豆瓣电影top250.xlsx'
    ws1 = wb.active
    ws1.title = 'top250'
    for n, a, s, m, i in zip(name, act, star, num, inq):
        name_index = name.index(n) + 1
        ws1['A%d' % name_index].value = n  # 电影名
        ws1['B%d' % name_index].value = s  # 电影评分
        ws1['C%d' % name_index].value = m  # 评论人数
        ws1['D%d' % name_index].value = i  # 短评
        ws1['E%d' % name_index].value = a  # 导演演员

    wb.save(filename=filename)


if __name__ == '__main__':
    result_xlsx()
    print('写入完成')
