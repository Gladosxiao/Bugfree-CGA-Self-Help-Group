import re

import requests
from lxml import etree

headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}


def search_reply(wd):
    search_url = 'https://www.dogedoge.com/results?q=' + wd
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    books = etree.HTML(html_content.replace('<em>', '').replace('<b>', ''))
    results = re.findall('<div id="r-(\d+\.\d+)', html_content)
    for result in results:
        link_url = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/div[1]/div/a/span[1]/text()'))
        if '...' not in link_url:
            description = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/h2/a/text()'))
            return '已为您找到相关信息：\n{}\n{}'.format(description, link_url).replace('\t', '')
    return '已为您找到相关信息：\n'


def search_description(wd):
    search_url = 'https://baike.baidu.com/item/' + wd
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content="(.*)">', html_content, flags=0)
    return '' if result is None else '\n' + result.group(1)


def search_stock(wd):
    if '美' in wd:
        code = re.search("[a-z]+", wd.replace('@bug-free群聊bot', '').lower())
        if code is None:
            return "本喵喵没有找到股票代码诶"
        search_url = 'http://hq.sinajs.cn/list=gb_' + code.group(0)
        html_content = requests.get(search_url, headers=headers).content.decode('gbk').split('"')[1].split(',')
        return "不存在此股票代码喵" if len(html_content) == 0 else '{}\n现价{}\n昨收{}\n今开{}\n今日最高{}\n今日最低{}' \
            .format(*html_content[:2], html_content[26], *html_content[5:8])
    else:
        code = re.search("[\d]{6}", wd)
        if code is None:
            return "本喵喵没有找到股票代码诶"
        key = 'sz' if '深' in wd else 'hk' if '港' in wd else 'sh'
        search_url = 'http://hq.sinajs.cn/list=' + key + code.group(0)
        html_content = requests.get(search_url, headers=headers).content.decode('gbk').split('"')[1].split(',')
        if '港' in wd:
            return "不存在此股票代码喵" if len(html_content) == 0 \
                else '{}\n今开{}\n昨收{}\n今日最高{}\n今日最低{}\n现价{}'.format(*html_content[1:])
        else:
            return "不存在此股票代码喵" if len(html_content) == 0 \
                else '{}\n今开{}\n昨收{}\n现价{}\n今日最高{}\n今日最低{}'.format(*html_content)


if __name__ == "__main__":
    print(search_stock("美zoominc"))
