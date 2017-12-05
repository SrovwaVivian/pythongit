# coding:utf-8
from bs4 import BeautifulSoup
import requests
import json
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
douban_movies = client['douban_movies']
movie_urls = douban_movies['movie_urls']


def get_response(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0 (X11Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 62.0.3202.94 Safari / 537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except TimeoutError:
        pass
    return response


def get_tags():
    start_url = 'https://movie.douban.com/j/search_tags?type=movie'

    wb_data = get_response(start_url)
    tags = wb_data.json().get('tags')

    print(type(tags), tags)
    return tags


def get_channel_tags():
    movies = []
    tags = get_tags()
    for tag in tags:
        pgstart = 0
        while 1:
            url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=time&page_limit=20&page_start={}'.format(
                tag, pgstart)
            time.sleep(1)
            response = get_response(url)
            subjects = response.json().get('subjects')
            print(subjects)
            if len(subjects) == 0:
                print('没有加载更多了')
                break
            for item in subjects:
                movie_urls.insert_one(item)
                movies.append(item)
            pgstart += 20
    print(len(movies))


cursor = movie_urls.aggregate([{'$group': {'_id': "$title", 'url': {'$push': "$url"}}}])
channel_urls = []
for result in cursor:
    print(result)

