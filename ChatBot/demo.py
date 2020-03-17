# encoding: utf-8
import itchat
from itchat.content import *

from .chat_bot import *


def content_analysis(content):
    if '众神' in content:
        chat_room.send('众神傻逼')
    elif content in ['关键字', '群聊关键字', '关键词', '群聊关键词']:
        send_keyword_cloud(chat_room)
    elif ':' in content or '：' in content:
        reply_dict.refresh_reply_dict(content)
        chat_room.send('奇怪的知识增加了!')
    elif reply_dict.is_in_dict(content):
        chat_room.send(reply_dict.get_reply_msg(content))
    else:
        result = get_keyword_description(content)
        if result is None:
            send_bqb(chat_room)
        else:
            chat_room.send(result)


@itchat.msg_register(TEXT, isGroupChat=True)
def _(msg):
    if chat_room_name in msg['User']['NickName']:
        hour, minute = get_time()
        print("%d:%d" % (hour, minute), msg['IsAt'], msg['Content'])
        if '@bug-free群聊bot' in msg['Content']:
            content = adjust_msg(msg['Content']).replace('@bug-free群聊bot', '').strip()
            content_analysis(content)
        else:
            append_text(adjust_msg(msg['Content']))


if __name__ == "__main__":
    chat_room_name = 'bug-free'
    reply_dict = ReplyDict()
    itchat.auto_login(hotReload=True)
    chat_room = itchat.search_chatrooms(name=chat_room_name)[0]
    itchat.run(True)
