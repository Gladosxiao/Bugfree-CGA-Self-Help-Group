import itchat
from itchat.content import TEXT
from apscheduler.schedulers.background import BackgroundScheduler

from responser import response


def remind_water():
    chat_group.send_image("./img/work/water.jpg")


def remind_sport():
    chat_group.send("喵呜~爆肝学(shui)习(qun)也要记得动一动鸭~")


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
        day_time = msg.createTime % 86400
        hour, minute, second = (day_time // 3600 + 8) % 24, (day_time % 3600) // 60, day_time % 60

        global last_msg
        if last_msg[0] != msg.actualNickName and last_msg[1] == msg.content:
            last_msg = None, None
            teardown, reply, value = "[Need to +1]", 1, msg.content
        else:
            last_msg = msg.actualNickName, msg.content
            teardown, reply, value = response(msg.content)

        if reply == 1:
            chat_group.send(value)
        elif reply == 2:
            chat_group.send_image(value)
        print(f"{hour}:{minute}:{second}, Sender:{msg.actualNickName}, Msg:{msg.content}, {teardown}")


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    chat_group_name = 'bug-free'
    last_msg = None, None
    chat_group = itchat.search_chatrooms(name=chat_group_name)[0]

    scheduler = BackgroundScheduler()
    scheduler.add_job(remind_water, 'cron', hour='8-22', minute='0', second='0')
    scheduler.add_job(remind_sport, 'cron', hour='8-22', minute='30', second='0')

    scheduler.start()
    itchat.run()
