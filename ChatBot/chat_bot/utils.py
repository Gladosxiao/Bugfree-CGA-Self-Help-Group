import jieba.posseg as posseg

data_path = 'data/'
img_path = 'img/'


def teardown_msg(msg):
    msg_data = []
    for key, value in posseg.cut(msg.replace('@bug-free群聊bot', '')):
        if len(key) > 1 and value not in ['c', 'm', 'p', 'q', 'r', 'w', 'x', 'y', 'z', 'un', ]:
            msg_data.append(key)
    return msg_data
