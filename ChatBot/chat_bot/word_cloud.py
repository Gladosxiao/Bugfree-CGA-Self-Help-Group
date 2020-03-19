import wordcloud
from .utils import data_path, img_path


def send_keyword_cloud(chat_group):
    with open(data_path + 'text.txt') as text_file:
        chat_text = text_file.read()
    cloud = wordcloud.WordCloud(font_path=data_path + "type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(chat_text).to_file(img_path + "cloud.jpg")
    chat_group.send_image(img_path + "cloud.jpg")
