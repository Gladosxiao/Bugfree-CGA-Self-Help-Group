# encoding: utf-8
import itchat
from itchat.content import *
import random
import requests
import re

seq = ['众神傻逼', '你说你ma呢', '哈哈哈 坏掉了吗，机器人，嗯！', '干！干！干！']
reply_dict = {'': '我在 众神傻逼', '哈哈哈': '本群禁止哈哈哈!'}


def read_reply_dict():
    with open('reply_dict.txt', 'r+') as reply_dict_file:
        for line in reply_dict_file.readlines():
            result = line.split('\t')
            if len(result) == 2:
                send, reply = result[0], result[1]
                reply_dict[send] = reply[:-1]


def save_reply_dict():
    try:
        with open('reply_dict.txt', 'w+') as reply_dict_file:
            for send in reply_dict.keys():
                if send != '':
                    reply_dict_file.writelines(send + '\t' + reply_dict[send] + '\n')
    except UnicodeEncodeError as e:
        print(e)


def search_keyword(wd):
    search_url = 'https://baike.baidu.com/item/' + wd
    headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content=".*>', html_content, flags=0)
    if result is None:
        return -1
    else:
        start, end = result.span()
        return html_content[start + 34:end - 2]


def content_analysis(content):
    content = content.replace('@bug-free群聊bot\u2005', '').strip()
    if content in reply_dict.keys():
        reply_msg = reply_dict[content]
    elif '：' in content:
        send, reply = content.split('：')
        reply_dict[send] = reply
        save_reply_dict()
        reply_msg = '奇怪的知识增加了!'
    else:
        content = content.replace('什么是', '')
        reply_msg = search_keyword(content)
        if reply_msg == -1:
            reply_msg = random.sample(seq, 1)[0]
    return content, reply_msg


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(msg['IsAt'], msg['Content'])
    if '@bug-free群聊bot' in msg['Content'] and msg['IsAt']:
        content, reply_msg = content_analysis(msg['Content'])
        print('\tNeed to reply:%s\n\tDecide to send:%s' % (content, reply_msg))
        return reply_msg


if __name__ == "__main__":
    read_reply_dict()
    itchat.auto_login(hotReload=False)
    itchat.run(True)
