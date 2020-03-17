# encoding: utf-8
import itchat
from itchat.content import *
import random
from chat_bot import *

seq = ['哈哈哈', '嘿嘿嘿', '呜呜呜', '嘤嘤嘤', '嗯嗯嗯',
       '众神傻逼', '机器人 坏掉了!', '你说你\U0001f434呢']


def content_analysis(content):
    if content in ['关键字', '群聊关键字', '关键词', '群聊关键词']:
        send_keyword_cloud(chat_room)
    elif (':' in content or '：' in content) and '- - - - -' not in content:
        reply_dict.refresh_reply_dict(content)
        chat_room.send('奇怪的知识增加了!')
    elif reply_dict.is_in_dict(content):
        chat_room.send(reply_dict.get_reply_msg(content))
    else:
        reply_index = []
        for index, line in enumerate(text_list):
            if content + '\n' == line:
                reply_index.append(index + 1)
        if len(reply_index) > 0:
            chat_room.send(adjust_msg(text_list[random.sample(reply_index, 1)[0]][:-1], False))
        else:
            result = adjust_msg(get_keyword_description(content), False)
            if result is None:
                send_bqb(chat_room)
            else:
                chat_room.send(result)
                if 'AI' in result or '智能' in result:
                    chat_room.send('长江后浪推前浪 想来%s不如我' % content)


@itchat.msg_register(TEXT, isGroupChat=True)
def _(msg):
    if chat_room_name in msg['User']['NickName']:
        hour, minute = get_time()
        print("%d:%d" % (hour, minute), msg['IsAt'], msg['Content'])
        if '@bug-free群聊bot' in msg['Content']:
            content = adjust_msg(msg['Content']).replace('@bug-free群聊bot', '').strip()
            content_analysis(content)
        else:  # if len(msg['Content']) < 25:
            append_text(adjust_msg(msg['Content']))
            text_list.append(adjust_msg(msg['Content']) + '\n')


if __name__ == "__main__":
    chat_room_name = 'bug-free'
    reply_dict = ReplyDict()
    with open(data_path + 'text.txt') as text:
        text_list = text.readlines()
    itchat.auto_login(hotReload=False)
    chat_room = itchat.search_chatrooms(name=chat_room_name)[0]
    itchat.run(True)
