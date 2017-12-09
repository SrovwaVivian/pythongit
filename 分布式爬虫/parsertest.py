import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
r = requests.get(url,headers=headers)

soup = BeautifulSoup(r.text,'html.parser')
links = soup.find_all('a', href=re.compile(r'/item/'))
# print(links)
new_urls = set()
page_url = url
for link in links:
    new_url = link['href']
    new_full_url = urllib.parse.urljoin(page_url, new_url)
    new_urls.add(new_full_url)
print (new_urls)
# title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
# summary = soup.find('div', class_='lemma-summary')
#
# print(summary.get_text())