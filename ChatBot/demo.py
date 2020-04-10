# encoding: utf-8
import itchat
from itchat.content import *

from chat_bot import *

last_msg = None
last_sender = None


@itchat.msg_register(TEXT, isGroupChat=True)
def _(msg):
    """
        'MsgId', 'FromUserName', 'ToUserName', 'MsgType', 'Content',
        'Status', 'ImgStatus', 'CreateTime', 'VoiceLength', 'PlayLength',
        'FileName', 'FileSize', 'MediaId', 'Url', 'AppMsgType',
        'StatusNotifyCode', 'StatusNotifyUserName', 'RecommendInfo',
        'ForwardFlag', 'AppInfo', 'HasProductId', 'Ticket', 'ImgHeight',
        'ImgWidth', 'SubMsgType', 'NewMsgId', 'OriContent', 'EncryFileName',
        'ActualNickName', 'IsAt', 'ActualUserName', 'User', 'Type', 'Text'
    """
    if chat_group_name in msg.user.nickName:
        global last_msg, last_sender
        print("%s, Sender:%s, Msg:%s" % (msg.createTime, msg.actualNickName, msg.content))
        if 25140 <= msg.createTime % 86400 <= 25200:
            print("\tLeetcode日常")
            return "多人在线史诗巨作Leetcode美服又更新辣,是兄弟就来刷本!"
        elif last_msg == msg.content and last_sender != msg.actualNickName:
            last_sender, last_msg = None, None
            print("\tNeed to +1:", msg.content)
            return msg.content
        else:
            last_sender, last_msg = msg.actualNickName, msg.content
            word_list = teardown_msg(msg.content)
            print('\tNeed to reply:%s\n' % word_list)
            if '@bug-free群聊bot' in msg.content:
                content_analysis(chat_group, word_list)
            elif len(word_list) > 0:
                with open(data_path + 'text.txt', 'a+') as file:
                    file.writelines(' '.join(word_list) + '\n')


if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    chat_group_name = 'bug-free'
    chat_group = itchat.search_chatrooms(name=chat_group_name)[0]
    itchat.run(True)
