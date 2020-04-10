import os
import random

from search_engine import search_description, search_reply
from utils import img_path, send_keyword_cloud


def content_analysis(chat_group, content):
    if len(content) == 0 or len(content & {'表情', 'mmbqb', 'bqb'}) > 0:
        chat_group.send_image(img_path + 'bqb/' + random.sample(os.listdir(img_path + 'bqb/'), 1)[0])
    elif len(content & {'关键字', '关键词'}) > 0:
        send_keyword_cloud(chat_group)
    else:
        chat_group.send(search_reply('+'.join(content)) + search_description(''.join(content)))


if __name__ == '__main__':
    pass
