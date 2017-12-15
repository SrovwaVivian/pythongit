# coding:utf-8

'''
爬虫调度器需要用到分布式进程中工作进程的代码，
具体内容可以参考第一章的分布式进程章节。
爬虫调度器需要先连接上控制节点，然后依次完成从url_q队列中获取URL，
下载并解析网页，将获取的数据交给result_q队列，返回给控制节点等各项任务，
'''
from multiprocessing.managers import BaseManager
from HTMLdownloader import HtmlDownloader
from HTMLparser import HtmlParser


class SpriderWork(object):

    def __init__(self):
        # 初始化分布式进程中的工作节点的连接工作
        # 实现第一步：使用BaseManager注册获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '127.0.0.1'
        print('Connect to server %s' % server_addr)
        # 实现第二步：连接到服务器:
        self.m = BaseManager(address=(server_addr, 8000), authkey=b'baike')
        self.m.connect()
        # 实现第三步：获取Queue的对象:
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finished')


    def crawler(self):
        while 1:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作...')
                        # 接着通知其它节点停止工作
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print('爬虫节点正在解析:%s' % url)
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({'new_urls': new_urls, 'data': data})
            except EOFError:
                print('连接工作节点失败')
                return
            except Exception as e:
                print(e)
                print('Crawler Field!')

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of str

if __name__ == '__main__':
    spider = SpriderWork()
    spider.crawler()
