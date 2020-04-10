import os
import random

from .search_engine import search_description, search_reply
from .utils import img_path
from .word_cloud import send_keyword_cloud


def check_in(check_group, keyword_group):
    for item in keyword_group:
        for sub_item in check_group:
            if item == sub_item:
                return True
    return False


def content_analysis(chat_group, content):
    if len(content) == 0 or check_in(content, ['表情', 'mmbqb', 'bqb']):
        image_sort = random.sample(os.listdir(img_path + 'bqb/'), 1)[0] + '/'
        bqb_name = random.sample(os.listdir(img_path + 'bqb/' + image_sort), 1)[0]
        chat_group.send_image(img_path + 'bqb/' + image_sort + bqb_name)
        # chat_group.send_image('img/01.jpg')
    elif check_in(content, ['关键字', '关键词']):
        send_keyword_cloud(chat_group)
    else:
        reply_msg = search_description(''.join(content))
        if reply_msg is None:
            reply_msg = search_reply('+'.join(content))
        chat_group.send(reply_msg)
