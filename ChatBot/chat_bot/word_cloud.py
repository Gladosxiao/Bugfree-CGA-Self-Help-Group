import wordcloud

from chat_bot.utils import data_path, img_path


def send_keyword_cloud(chat_group):
    with open(data_path + 'text.txt') as text_file:
        chat_text = text_file.readlines()
    if len(chat_text) > 500:
        chat_text = chat_text[-500:]
    cloud = wordcloud.WordCloud(font_path=data_path + "type.ttf", width=480, height=270, scale=2,
                                max_words=1000, min_font_size=4, background_color='white')
    cloud.generate(' '.join(chat_text)).to_file(img_path + "cloud.jpg")
    chat_group.send_image(img_path + "cloud.jpg")


if __name__ == '__main__':
    with open('../data/text.txt') as test_text_file:
        test_chat_text = test_text_file.readlines()
    if len(test_chat_text) > 500:
        test_chat_text = test_chat_text[-500:]
    test_cloud = wordcloud.WordCloud(font_path="../data/type.ttf", width=480, height=270, scale=2,
                                     max_words=1000, min_font_size=4, background_color='white')
    test_cloud.generate(' '.join(test_chat_text)).to_file("../img/cloud.jpg")
