#!usr/bin/env python
from threading import Thread, Lock
from queue import Queue
import urllib.parse
import re
import socket
import time
from multiprocessing.pool import ThreadPool

# 已解析的网页链接
seen_urls = set(['/'])
# 创建锁的实例
lock = Lock()


# 核心代码，创建任务实例的类


class Fecher(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True

    def run(self):
        while True:
            # 获取任务
            url = self.tasks.get()
            print(url)
            sock = socket.socket()
            sock.connect(('localhost', 5000))
            get = 'GET {} HTTP/1.0\r\nHost: localhost\r\n\r\n'.format(url)
            sock.send(get.encode('ascii'))
            response = b''
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            # 解析页面上的所有链接
            links = self.parse_links(url, response)

            # 得到新链接加入任务队列与seen_urls中，links是集合
            for link in links.difference(seen_urls):
                # 放入任务，tasks其实就是queue,消息队列
                self.tasks.put(link)
            # 更新已解析页面的集合，因为已经放入任务了
            seen_urls.update(links)
            self.tasks.task_done()

    # 解析页面，获取连接
    def parse_links(self, fetched_url, response):
        # 没有返回内容，返回空集
        if not response:
            print('error:{}'.format(fetched_url))
            return set()

        if not self._is_html(response):
            return set()

        # 通过href属性找到所有链接
        urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                              self.body(response)))

        links = set()

        for url in urls:
            # 可能找到的url是相对路径，这时候就需要join一下，绝对路径的话就还是会返回url
            normalized = urllib.parse.urljoin(fetched_url, url)
            # url的信息会被分段存在parts里
            parts = urllib.parse.urlparse(normalized)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            host, port = urllib.parse.splitport(parts.netloc)
            if host and host.lower() not in ('localhost'):
                continue
            # 有的页面会通过地址里的#frag后缀在页面内跳转，这里去掉frag的部分
            defragmented, frag = urllib.parse.urldefrag(parts.path)
            links.add(defragmented)

        return links

    # 得到报文的html正文
    def body(self, response):
        body = response.split(b'\r\n\r\n', 1)[1]
        return body.decode('utf-8')

    def _is_html(self, response):
        head, body = response.split(b'\r\n\r\n', 1)
        headers = dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
        return headers.get('Content-Type', '').startswith('text/html')


if __name__ == '__main__':
    start = time.time()
    pool = ThreadPool()
    # 创建消息队列
    tasks = Queue()
    tasks.put('/')
    # 开启４个消息队列
    workers = [Fecher(tasks) for i in range(4)]
    # 放入线程池，自动分配线程
    pool.map_async(lambda x: x.run(), workers)
    tasks.join()
    pool.close()
    print('{} URLs fetched in {:.1f} seconds'.format(
        len(seen_urls), time.time() - start))
