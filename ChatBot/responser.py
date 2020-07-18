import os
import re
from random import sample
import requests

from lxml import etree
import jieba.posseg as jp
import wordcloud

word_filter = ['@bug-free群聊bot', '哈', '哈哈', '哈哈哈', '哈哈哈哈',
               '知道', '现在', '应该', '没有', '感觉', '不要', '觉得', '今天', '不会', '出来',
               '不行', '不能', '可能', '是不是', '还有', '意思', '只能', '直接', '主要', '时候', ]
speech_filter = ['c', 'd', 'm', 'p', 'q', 'r', 'w', 'x', 'y', 'z', 'un', ]
headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

encoding = 'utf-8'


def generate_keyword_cloud():
    with open('./log/teardown.txt', encoding=encoding) as text_file:
        chat_text = text_file.readlines()
    chat_len = len(chat_text)
    if chat_len > 1000:
        chat_text = chat_text[-1000:]
    # cloud
    cloud = wordcloud.WordCloud(font_path="./log/type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(' '.join(chat_text)).to_file("./img/work/cloud.jpg")


def search_reply(msg, td):
    # description
    search_url = 'https://baike.baidu.com/item/' + ' '.join(td)
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content="(.*)">', html_content, flags=0)
    reply_info = "已为您找到相关信息:" if result is None else f"已为您找到相关信息:\n{result.group(1)}"
    # information
    search_url = 'https://www.dogedoge.com/results?q=' + msg.replace(' ', '+')
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    books = etree.HTML(html_content.replace('<em>', '').replace('<b>', ''))
    result = re.findall('<div id="r-(\d+\.\d+)', html_content)[0]
    link_url = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/div[1]/div/a/span[1]/text()')).replace('...', '')
    description = ''.join(books.xpath('//*[@id="r-' + result + '"]/div/h2/a/text()')).replace('\t', '')
    reply_info += f'\n{description}\n{link_url}'
    return reply_info


# def search_stock(wd):
#     if '美' in wd:
#         code = re.search("[a-z]+", wd.replace('@bug-free群聊bot', '').lower())
#         if code is None:
#             return "本喵喵没有找到股票代码诶"
#         search_url = 'http://hq.sinajs.cn/list=gb_' + code.group(0)
#         html_content = requests.get(search_url, headers=headers).content.decode('gbk').split('"')[1].split(',')
#         return "不存在此股票代码喵" if len(html_content) == 0 else '{}\n现价{}\n昨收{}\n今开{}\n今日最高{}\n今日最低{}' \
#             .format(*html_content[:2], html_content[26], *html_content[5:8])
#     else:
#         code = re.search("[\d]{6}", wd)
#         if code is None:
#             return "本喵喵没有找到股票代码诶"
#         key = 'sz' if '深' in wd else 'hk' if '港' in wd else 'sh'
#         search_url = 'http://hq.sinajs.cn/list=' + key + code.group(0)
#         html_content = requests.get(search_url, headers=headers).content.decode('gbk').split('"')[1].split(',')
#         if '港' in wd:
#             return "不存在此股票代码喵" if len(html_content) == 0 \
#                 else '{}\n今开{}\n昨收{}\n今日最高{}\n今日最低{}\n现价{}'.format(*html_content[1:])
#         else:
#             return "不存在此股票代码喵" if len(html_content) == 0 \
#                 else '{}\n今开{}\n昨收{}\n现价{}\n今日最高{}\n今日最低{}'.format(*html_content)


def response(message):
    # save
    # with open('./log/message.txt', 'a+', encoding=encoding) as file:
    #     file.writelines(message + '\n')

    # teardown
    teardown = message
    for item in word_filter:
        teardown = teardown.replace(item, '')
    teardown = set(key for key, value in jp.cut(teardown) if len(key) > 1 and value not in speech_filter)

    if '@bug-free群聊bot' in message:
        # bqb
        if len(teardown & {'表情', 'mmbqb', 'bqb'}) > 0:
            return teardown, 2, f"./img/bqb/{sample(os.listdir('./img/bqb/'), 1)[0]}"

        # key word
        if len(teardown & {'关键字', '关键词', '搜榜'}) > 0:
            generate_keyword_cloud()
            return teardown, 2, "./img/work/cloud.jpg"

        # reply
        message = message.replace('@bug-free群聊bot', '').replace('\u2005 ', '')
        return teardown, 1, search_reply(message, teardown)
    else:
        try:
            with open('./log/test.txt', 'w', encoding=encoding) as test_file:
                test_file.writelines(' '.join(teardown) + '\n')
            with open('./log/test.txt', encoding=encoding) as test_file:
                test_file.readlines()
        except Exception as e:
            return teardown, 1, e
        else:
            with open('./log/teardown.txt', 'a+', encoding=encoding) as file:
                file.writelines(' '.join(teardown) + '\n')
            return teardown, 0, 0


if __name__ == "__main__":
    print(response("我快不认识亿这个单位了 周冬雨拍一部戏也能赚一个亿"))
    print(response("@bug-free群聊bot 我快不认识bqb这个单位了 周冬雨拍一部戏也能赚一个亿"))
    print(response("@bug-free群聊bot 我快不认识关键字这个单位了 周冬雨拍一部戏也能赚一个亿"))
