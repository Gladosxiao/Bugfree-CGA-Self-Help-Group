# encoding: utf-8
import itchat
from itchat.content import *

from chat_bot import *

seq = ['哈哈哈', '嘿嘿嘿', '呜呜呜', '嘤嘤嘤', '嗯嗯嗯']
threshold = 0.05


def random_action():
    random_num = random.random()
    if random_num < threshold:
        send_bqb(chat_room)
    elif random_num > 1 - threshold:
        chat_room.send(random.sample(seq, 1)[0])


def content_analysis(content):
    if content in ['关键字', '群聊关键字', '关键词', '群聊关键词']:
        send_keyword_cloud(chat_room)
    elif (':' in content or '：' in content) and '- - - - -' not in content and 'http' not in content:
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
            result = get_keyword_description(content)
            if result is None:
                chat_room.send(search_reply(content))
            else:
                chat_room.send(adjust_msg(result), False)
    random_action()


def cget(items):
    if isinstance(items, Iterable):
        bt.send('\n'.join(items))
    else:
        bt.send(str(items))


def cset(key, value):
    globals()[key] = value
    cget(key)


def console_analysis(content):
    try:
        exec(content)
    except Exception as e:
        bt.send('Receive: %s\nError: %s' % (content, e))


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
            text_list.append(adjust_msg(msg['Content']) + '\n')
    elif 'bot' in msg['User']['NickName']:
        if msg['Content'] == '~':
            help_str = '欢迎来到控制台模式，参考指令如下：\n'
            help_str += "cget(bt, items)\n"
            help_str += "cset(chat_room, key, value)\n"
            help_str += "sys.exit()\n"
            bt.send(help_str)
        else:
            console_analysis(msg['Content'])


if __name__ == "__main__":
    chat_room_name = 'bug-free'
    reply_dict = ReplyDict()
    with open(data_path + 'text.txt') as text:
        text_list = text.readlines()
    itchat.auto_login(hotReload=True)
    bt = itchat.search_chatrooms(name='bot')[0]
    chat_room = itchat.search_chatrooms(name=chat_room_name)[0]
    itchat.run(True)
