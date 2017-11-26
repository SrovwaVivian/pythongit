#!usr/bin/env python
#coding:utf-8

from bs4 import BeautifulSoup
import requests,urllib

url = "http://www.mzitu.com"

def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def get_title(html):
    soup = BeautifulSoup(html,'html.parser')
    all_title = soup.find('div',class_='postlist').find_all('a',target="_blank")
    for title in all_title:
        title = title.get_text()
        print title
    return title

def get_img(html):
    pic_max = soup.find_all('span')[10].text
    title = soup.find('h2',class_='main-title').text
    for i in range(1,int(pic_max) + 1):
        href = url+str(i)
        html = requests.get(href)
        html_soup = BeautifulSoup(html.text,'html.parser')

        pic_url = html_soup.find('img',alt = title)
        html = requests.get(pic_url['src'])

        #获取图片的名字方便命名
        file_name = pic_url['src'].split(r'/')[-1]

        #图片不是文本文件，以二进制格式写入，所以是html.content
        f = open(file_name,'wb')
        f.write(html.content)
        f.close()


if __name__ == '__main__':
	get_title(get_html(url))
    get_img()