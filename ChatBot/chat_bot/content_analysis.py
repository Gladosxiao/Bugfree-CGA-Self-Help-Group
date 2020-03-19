import random
import os
from .search_engine import search_description, search_reply
from .word_cloud import send_keyword_cloud
from .utils import img_path


def check_in(check_group, keyword_group):
    for item in keyword_group:
        for sub_item in check_group:
            if item == sub_item:
                return True
    return False


def content_analysis(chat_group, content):
    if content == ['更新']:
        reply_msg = 'bug-free群聊bot v1.0\n' \
                    '1. 发送[关键字]or[群聊关键词是什么]or[刚才聊天啥关键字]等类似语句获取沙雕词云\n' \
                    '2. 发送[整两个表情]or[bqb gkd]or[mm bqb来]等类似语句获取kamm bqb\n' \
                    '3. 其他对话根据拆解结果尽量尝试回复www\n' \
                    'p.s.由于使用jieba分词，因此无间隔的英文无法识别，如[kammbqb]无法发送表情包qwq'
        chat_group.send(reply_msg)
    elif check_in(content, ['关键字', '关键词']):
        send_keyword_cloud(chat_group)
    elif check_in(content, ['表情', 'bqb']):
        image_sort = random.sample(os.listdir(img_path + 'bqb/'), 1)[0] + '/'
        bqb_name = random.sample(os.listdir(img_path + 'bqb/' + image_sort), 1)[0]
        chat_group.send_image(img_path + 'bqb/' + image_sort + bqb_name)
    else:
        reply_msg = search_description(''.join(content))
        if reply_msg is None:
            reply_msg = search_reply('+'.join(content))
        chat_group.send(reply_msg)
