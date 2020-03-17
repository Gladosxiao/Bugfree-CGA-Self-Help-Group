import requests
import re
import wordcloud
import jieba
import cv2
from .utils import data_path, img_path


def get_keyword_description(wd):
    search_url = 'https://baike.baidu.com/item/' + wd
    headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    html_content = requests.get(search_url, headers=headers).content.decode('utf8')
    result = re.search('<meta name="description" content=".*>', html_content, flags=0)
    if result is None:
        return None
    else:
        start, end = result.span()
        return html_content[start + 34:end - 2]


def append_text(seq):
    with open(data_path + 'text.txt', 'a+') as text_file:
        text_file.writelines(seq + '\n')


def send_keyword_cloud(chat_room, send_img=True):
    with open(data_path + 'text.txt') as text:
        cut_text = jieba.cut(text.read())
    cloud = wordcloud.WordCloud(font_path=data_path + "type.ttf",
                                background_color='white',
                                mask=cv2.imread(img_path + "mask.jpg"),
                                max_words=1000, max_font_size=20)
    cloud.generate(" ".join(cut_text))
    cloud.to_file(img_path + "cloud.png")
    if send_img:
        chat_room.send_image("img/cloud.png")


if __name__ == "__main__":
    print(get_keyword_description('学习'))
    send_keyword_cloud('test', send_img=False)
