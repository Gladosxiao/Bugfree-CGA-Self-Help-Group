import re

import requests
from lxml import etree

headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}


def search_description(wd):
    search_url = 'https://baike.baidu.com/item/' + wd
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content="(.*)">', html_content, flags=0)
    return None if result is None else result.group(1)


def search_reply(wd):
    search_url = 'https://www.dogedoge.com/results?q=' + wd
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    books = etree.HTML(html_content.replace('<em>', '').replace('<b>', ''))
    results = re.findall('<div id="r-(\d+\.\d+)', html_content)
    for result in results:
        link_url = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/div[1]/div/a/span[1]/text()'))
        if '...' not in link_url:
            description = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/h2/a/text()'))
            result = '已为您找到相关信息：\n%s\n%s' % (description, link_url.replace("...", ""))
            return result.replace('\t', '')