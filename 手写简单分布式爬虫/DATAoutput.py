# coding:utf-8
import codecs
import time


class DataOutput(object):
    def __init__(self):
        self.filepath = 'bike_%s.html' % (
            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        self.output_head(self.filepath)
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self.output_html(self.filepath)

    def output_head(self, path):
        '''
        将HTML头写进去
        '''
        with codecs.open(path, 'w', encoding='utf-8') as fout:
            fout.write("<html>")
            fout.write("<body>")
            fout.write("<table>")

    def output_html(self, path):
        '''
        将数据写入HTML文件中

        '''
        with codecs.open(path, 'a', encoding='utf-8') as fout:
            for data in self.datas:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['url'])
                fout.write("<td>%s</td>" % data['title'])
                fout.write("<td>%s</td>" % data['summary'])
                fout.write("</tr>")
                self.datas.remove(data)

    def ouput_end(self, path):
        '''
        输出HTML结束

        '''
        with codecs.open(path, 'a', encoding='utf-8') as fout:
            fout.write("</table>")
            fout.write("</body>")
            fout.write("</html>")
