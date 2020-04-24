import jieba.posseg as jp
import wordcloud

img_path = 'img/'
v_stop = ['c', 'd', 'm', 'p', 'q', 'r', 'w', 'x', 'y', 'z', 'un', ]
w_filter = ['@bug-free群聊bot', '众神', 'Blanc',
            '知道', '现在', '应该', '没有', '感觉', '不要', '觉得', '今天', '不会', '出来', ]


def teardown_msg(msg):
    for item in w_filter:
        msg = msg.replace(item, '')
    return set(key for key, value in jp.cut(msg) if len(key) > 1 and value not in v_stop)


def send_keyword_cloud(chat_group):
    with open('text.txt') as text_file:
        chat_text = text_file.readlines()
    if len(chat_text) > 1000:
        chat_text = chat_text[-1000:]
    cloud = wordcloud.WordCloud(font_path="type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(' '.join(chat_text)).to_file(img_path + "cloud.jpg")
    chat_group.send_image(img_path + "cloud.jpg")


if __name__ == "__main__":
    pass
