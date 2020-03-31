# encoding: utf-8
import itchat
from itchat.content import *
from chat_bot import *


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
        if globals()['last_msg'] == msg.content and globals()['last_sender'] != msg.actualNickName:
            globals()['last_msg'] = None
            globals()['last_sender'] = None
            print("Need to +1:", msg.content)
            return msg.content
        else:
            globals()['last_sender'] = msg.actualNickName
            globals()['last_msg'] = msg.content
        word_list = teardown_msg(msg.content)
        print("%s, Sender:%s, Msg:%s, Key Words:%s"
              % (msg.createTime, msg.actualNickName, msg.content, ' '.join(word_list)))
        if '@bug-free群聊bot' in msg.content:
            print('\tNeed to reply:%s\n' % word_list)
            content_analysis(chat_group, word_list)
        else:
            with open(data_path + 'text.txt', 'a+') as file:
                file.writelines(' '.join(word_list) + '\n')
    # elif 'bot' in msg.user.nickName:
    #     console_analysis(bot_test, msg.content)


if __name__ == "__main__":
    last_msg = None
    last_sender = None
    itchat.auto_login(hotReload=True)
    chat_group_name = 'bug-free'
    # bot_test = itchat.search_chatrooms(name='bot')[0]
    chat_group = itchat.search_chatrooms(name=chat_group_name)[0]
    # chat_group = bot_test
    itchat.run(True)
