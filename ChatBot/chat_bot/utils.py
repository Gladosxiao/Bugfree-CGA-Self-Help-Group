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


def send_kammbqb(chat_room):
    image_path = random.sample(os.listdir(img_path + 'kamm/'), 1)[0]

    chat_room.send_image(img_path + 'kamm/' + image_path)


if __name__ == "__main__":
    pass
