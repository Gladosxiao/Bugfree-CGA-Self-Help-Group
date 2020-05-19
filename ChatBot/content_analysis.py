import os
import random

from search_engine import search_description, search_reply
from utils import img_path, send_keyword_cloud


def content_analysis(chat_group, content, artificial_hot_search):
    flag = True
    if len(content) == 0 or len(content & {'表情', 'mmbqb', 'bqb'}) > 0:
        flag = False
        chat_group.send_image(img_path + 'bqb/' + random.sample(os.listdir(img_path + 'bqb/'), 1)[0])
    if len(content & {'关键字', '关键词', '搜榜'}) > 0:
        flag = False
        send_keyword_cloud(chat_group, artificial_hot_search)
    if flag:
        chat_group.send(search_reply('+'.join(content)) + search_description(''.join(content)))


if __name__ == '__main__':
    pass
