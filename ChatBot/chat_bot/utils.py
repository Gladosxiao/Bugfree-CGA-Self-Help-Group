import jieba.posseg as posseg

data_path = 'data/'
img_path = 'img/'


def teardown_msg(msg):
    msg_data = []
    for key, value in posseg.cut(msg.replace('@bug-free群聊bot', '').replace('众神', '')):
        if len(key) > 1 and value not in ['c', 'd', 'm', 'p', 'q', 'r', 'w', 'x', 'y', 'z', 'un', ]:
            msg_data.append(key)
    return list(set(msg_data))


if __name__ == "__main__":
    # for key, value in posseg.cut("有返校的彩蛋"):
    #     print(key, value)
    print(teardown_msg("返校的彩蛋"))
