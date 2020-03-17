import datetime
import os
import random

data_path = 'data/'
img_path = 'img/'


def get_time():
    cur = datetime.datetime.now()
    return cur.hour, cur.minute


def adjust_msg(msg):
    return msg.replace('\u2005', '').strip()


def send_bqb(chat_room):
    image_sort = random.sample(os.listdir(img_path + 'bqb/'), 1)[0] + '/'
    bqb_name = random.sample(os.listdir(img_path + 'bqb/' + image_sort), 1)[0]
    chat_room.send_image(img_path + 'bqb/' + image_sort + bqb_name)


if __name__ == "__main__":
    test_img_path = '../' + img_path
    test_image_sort = random.sample(os.listdir(test_img_path + 'bqb/'), 1)[0] + '/'
    test_bqb_name = random.sample(os.listdir(test_img_path + 'bqb/' + test_image_sort), 1)[0]
    print(test_img_path + 'bqb/' + test_image_sort + test_bqb_name)
