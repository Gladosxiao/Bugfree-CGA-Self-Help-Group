from random import randint

import jieba.posseg as jp
import wordcloud

img_path = 'img/'
v_stop = ['c', 'd', 'm', 'p', 'q', 'r', 'w', 'x', 'y', 'z', 'un', ]
w_filter = ['@bug-free群聊bot', '众神', 'Blanc',
            '知道', '现在', '应该', '没有', '感觉',
            '不要', '觉得', '今天', '不会', '出来',
            # "DINGDING", "群主",
            # 'xdg', 'XDG', "GlaDosX",
            # '落雨', '沈博',
            # '鱼鱼', 'YZX', 'yzx', 'ich', 'hei',
            # 'bg', '饼哥',
            # 'beig', '北哥',
            # '雪松', '松松',
            '哈', '哈哈', '哈哈哈', '哈哈哈哈',
            "不行", "不能", "可能", "是不是", '还有']


def teardown_msg(msg):
    for item in w_filter:
        msg = msg.replace(item, '')
    return set(key for key, value in jp.cut(msg) if len(key) > 1 and value not in v_stop)


def send_keyword_cloud(chat_group, bb=None):
    with open('text.txt') as text_file:
        chat_text = text_file.readlines()
    if len(chat_text) > 1000:
        chat_text = chat_text[-1000:]
    if bb:
        chat_len = len(chat_text)
        for _ in range(chat_len // 10):
            chat_text[randint(0, chat_len - 1)] = bb
    cloud = wordcloud.WordCloud(font_path="type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(' '.join(chat_text)).to_file(img_path + "cloud.jpg")
    chat_group.send_image(img_path + "cloud.jpg")


if __name__ == "__main__":
    pass
