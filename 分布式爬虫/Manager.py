# coding:utf-8
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from multiprocessing import Process
from URLmanager import UrlMannager
from DATAoutput import DataOutput
import time

'''
url_q队列是URL管理进程将URL传递给爬虫节点的通道
result_q队列是爬虫节点将数据返回给数据提取进程的通道
conn_q队列是数据提取进程将新的URL数据提交给URL管理进程的通道
store_q队列是数据提取进程将获取到的数据交给数据存储进程的通道
'''


class Manager(object):

    def start_manager(self, url_q, result_q):
        # 将Queue对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        #绑定端口8000，设置验证口令‘baike’。这个相当于对象的初始化
        manager = BaseManager(address=('127.0.0.1', 8000), authkey=b'baike')
        return manager

    # URL管理进程将从conn_q队列获取到的新URL提交给URL管理器，
    # 经过去重之后，取出URL放入url_queue队列中传递给爬虫节点
    def url_manager_proc(self, url_q, conn_q, root_url):
        url_manager = UrlMannager()
        url_manager.add_new_url(root_url)
        while 1:
            while (url_manager.has_new_url()):
                #从URL管理器获取新的url
                new_url = url_manager.get_new_url()
                #将新的URL发给工作节点
                url_q.put(new_url)
                print('old_url=', url_manager.old_url_size())
                #加一个判断条件，当爬去2000个链接后就关闭,并保存进度
                if url_manager.old_url_size() > 2000:
                    #通知爬行节点工作结束
                    url_q.put('end')
                    print('控制节点发起结束通知')
                    #关闭管理节点，同时存储set状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress(
                        'old_urls.txt', url_manager.old_urls)
                    return
            # 将从result_solve_proc获取到的urls添加到URL管理器之间
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except:
                time.sleep(0.1)  # 延时休息

    # 数据提取进程从result_queue队列读取返回的数据，并将数据中的URL添加到conn_q队列交给URL管理进程，
    # 将数据中的文章标题和摘要添加到store_q队列交给数据存储进程。
    def result_solve_proc(self, result_q, conn_q, store_q):
        while 1:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls'] == 'end':
                        # 结果分析进程接受通知然后结束
                        print('结果分析进程接受通知然后结束!')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])  # url为set类型
                    store_q.put(content['data'])  # 解析出来的数据为dict类型
                else:
                    time.sleep(0.1)  # 延时休息
            except:
                time.sleep(0.1)  # 延时休息

    # 数据存储进程从store_q队列中读取数据，并调用数据存储器进行数据存储。
    def store_proc(self, store_q):
        output = DataOutput()
        while 1:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接受通知然后结束!')
                    output.ouput_end(output.filepath)
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)


# 将分布式管理器、URL管理进程、 数据提取进程和数据存储进程进行启动，并初始化4个队列。
if __name__ == '__main__':
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()
    conn_q = Queue()
    node = Manager()
    manager = node.start_manager(url_q, result_q)
    root_url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB'
    url_manager_proc = Process(target=node.url_manager_proc, args=(
        url_q, conn_q, root_url,))

    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,))

    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
