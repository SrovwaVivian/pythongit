# coding:utf-8
import requests, re, os, time
import pdfkit
import logging
from bs4 import BeautifulSoup

html_template = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
</head> 
<body> 
{content} 
</body> 
</html> 

"""

start_url = 'https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'


def parse_html(url, name):
    header = {
        'Referer': 'https://www.liaoxuefeng.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    try:
        html = requests.get(url, headers=header)
        soup = BeautifulSoup(html.content, 'html.parser')

        title = soup.find('h4').get_text()
        body = soup.find_all(class_="x-wiki-content")[0]
        # 插入标签，让title居中
        center_tag = soup.new_tag('center')
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)
        html = str(body)
        pattern = "(<img .*?src=\")(.*?)(\")"

        # 把图片的相对路径改成绝对路径
        def re_func(s):
            if not s.group(2).startswith('http'):
                rtn = s.group(1) + 'https://www.liaoxuefeng.com' + s.group(2) + s.group(3)
                return rtn
            else:
                s.group(1) + s.group(2) + s.group(3)

        html = re.sub(pattern, re_func, html)
        html = html_template.format(content=html)
        html = html.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name
    except Exception as e:
        logging.error("解析错误", exc_info=True)


# 得到所有目录链接
def get_urllist(start_url):
    header = {
        'Referer': 'https://www.liaoxuefeng.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    r = requests.get(start_url, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')
    menu = soup.select('ul.uk-nav.uk-nav-side')[-1]
    menu_li = menu.find_all('li')
    urls = []
    for li in menu_li:
        url = 'https://www.liaoxuefeng.com' + li.a.get('href')
        urls.append(url)
    return urls
    # print(len(urls))


def save_pdf(htmls, fname):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, fname, options=options)


def main():
    fname = 'lxf_python3'
    urls = get_urllist(start_url)
    print(urls)
    for i, url in enumerate(urls):
        parse_html(url, str(i) + '.html')
        time.sleep(2)
        print('转换第%s个' % str(i))
    htmls, pdfs = [], []
    for i in range(0, 128):
        htmls.append(str(i) + '.html')
        # pdfs.append(fname+str(i)+'.pdf')
        # save_pdf(str(i)+'.html',fname+str(i)+'.pdf')
    save_pdf(htmls, fname)
    # 删除创建的html文件
    for html in htmls:
        os.remove(html)


if __name__ == '__main__':
    main()
