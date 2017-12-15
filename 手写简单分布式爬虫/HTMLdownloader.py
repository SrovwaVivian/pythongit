# coding:utf-8
'''
爬虫调度器从控制节点中的url_q队列读取URL
爬虫调度器调用HTML下载器、HTML解析器获取网页中新的URL和标题摘要
最后爬虫调度器将新的URL和标题摘要传入result_q队列交给控制节点
'''
import requests


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
