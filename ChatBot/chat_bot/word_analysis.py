import re

import jieba
import requests
import wordcloud
from lxml import etree

from .utils import data_path, img_path


def search_reply(wd):
    search_url = 'https://www.dogedoge.com/results?q=' + wd.replace(' ', '+')
    headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    books = etree.HTML(html_content.replace('<em>', ''))
    result_path = re.search('<div id="r-(\d+\.\d+)', html_content, flags=0).group(1)
    result = '已为您找到相关信息：\n'
    result += ''.join(books.xpath('//*[@id="r-' + result_path + '"]/div/h2/a/text()')) + '\n'
    result += ''.join(books.xpath('//*[@id="r-' + result_path + '"]/div/div[1]/div/a/span[1]/text()')) + '\n'
    return result.replace('\t', '')


def get_keyword_description(wd):
    search_url = 'https://baike.baidu.com/item/' + wd
    headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content=".*>', html_content, flags=0)
    if result is None:
        return None
    else:
        start, end = result.span()
        description = html_content[start + 34:end - 2]
        return description


def send_keyword_cloud(chat_room, send_img=True):
    with open(data_path + 'text.txt') as text:
        cut_text = list(jieba.cut(text.read()))
    for index in range(len(cut_text) - 1, 0, -1):
        for item in ['众神', '这', '个', '是', '@', '\n']:
            if item in cut_text[index]:
                cut_text.pop(index)
    cloud = wordcloud.WordCloud(font_path=data_path + "type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(" ".join(cut_text).replace('众神', ''))
    if send_img:
        cloud.to_file(img_path + "cloud.jpg")
        chat_room.send_image("img/cloud.jpg")
    else:
        return list(cloud.words_.keys())[0:10]


if __name__ == "__main__":
    print(get_keyword_description('学习'))
    send_keyword_cloud('test', send_img=False)
