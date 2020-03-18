import datetime
import os
import random

data_path = 'data/'
img_path = 'img/'
receive_dict = {'\u2005': '', '\xdf': 'ss', '\U0001f434': '[ma]'}
send_dict = {'[ma]': '\U0001f434'}


def get_time():
    cur = datetime.datetime.now()
    return cur.hour, cur.minute


def adjust_msg(msg, receive=True):
    if receive:
        for key in receive_dict.keys():
            msg = msg.replace(key, receive_dict[key])
    else:
        for key in send_dict.keys():
            msg = msg.replace(key, send_dict[key])
    return msg.strip()


def append_text(seq):
    with open(data_path + 'text.txt', 'a+') as text_file:
        text_file.writelines(seq + '\n')


def send_bqb(chat_room):
    image_sort = random.sample(os.listdir(img_path + 'bqb/'), 1)[0] + '/'
    bqb_name = random.sample(os.listdir(img_path + 'bqb/' + image_sort), 1)[0]
    chat_room.send_image(img_path + 'bqb/' + image_sort + bqb_name)


if __name__ == "__main__":
    test_img_path = '../' + img_path
    test_image_sort = random.sample(os.listdir(test_img_path + 'bqb/'), 1)[0] + '/'
    test_bqb_name = random.sample(os.listdir(test_img_path + 'bqb/' + test_image_sort), 1)[0]
    print(test_img_path + 'bqb/' + test_image_sort + test_bqb_name)
