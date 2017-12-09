# coding: utf-8
import pickle
import hashlib


class UrlMannager(object):
    def __init__(self):
        self.new_urls = self.load_process('new_urls.txt')  # 未爬取URL集合
        self.old_urls = self.load_process('old_urls.txt')  # 已爬取URL集合

    def has_new_url(self):
        # 判断是否有未爬取的URL
        return self.new_url_size() != 0

    def get_new_url(self):
        # 获取一个未爬取的URL，将其从队列中删除，hash一下放入旧队列中
        # hash一下可以节省内存
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        # python3编码为unicode，需要先变成bytes再update
        m.update(new_url.encode('utf-8'))
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self, url):
        '''
        将新的URL添加到未爬取的URL集合中,
        判断：如果既不在新队列，又不在旧队列，就加入新队列
        以供爬取
        '''
        if url is None:
            return None
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        # 把某一页抓取的链接全部判断一遍，加入新队列
        if urls is None or len(urls) == 0:
            return None
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        # 获取未爬取URL集合的s大小
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self, path, data):
        # 保存进度
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    # 断点续抓
    def load_process(self, path):
        print('[+]从文件加载进度：%s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('[+]无进度文件，创建：%s' % path)
        return set()
