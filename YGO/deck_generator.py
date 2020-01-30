# import cdblib
import os
import random
import time
from tkinter import *


def get_card_data(key_path):
    # Read cards
    # cdb_path = key_path + "cdb\\cards.cdb"
    # with open(cdb_path, 'rb') as cdb_file:
    #     cdb_data = cdb_file.read()
    # reader = cdblib.Reader(cdb_data)
    #
    # for key, value in reader.iteritems():
    #     print('+{},{}:{}->{}'.format(len(key), len(value), key, value))
    pic_path = key_path + "\\picture\\card\\"
    card_name_list = os.listdir(pic_path)
    card_name_list = list(map(lambda x: x[:-4], card_name_list))
    return card_name_list


def generate_deck_file():
    key_path = key_path_entry.get()
    key_path.replace('\\', "\\\\")
    deck_name = deck_name_entry.get()
    deck_length = int(deck_length_entry.get())

    # Generate the deck content
    random_cards = random.sample(get_card_data(key_path), deck_length)
    deck = "#created by ygopro2\n#main\n" + "\n".join(random_cards) + "#extra\n!side\n"
    with open(key_path + "\\deck\\" + deck_name, 'w') as deck_file:
        deck_file.write(str(deck))

    refresh()


def entry_set(entry, value):
    entry.delete(0, END)
    entry.insert(0, value)


def refresh():
    entry_set(series_name_entry, "Temporarily useless")
    refresh_name = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time())) + '.ydk'
    entry_set(deck_name_entry, refresh_name)


if __name__ == "__main__":
    deck_generator = Tk()
    deck_generator.title("YGO卡组生成器")

    Label(deck_generator, text="YGOPRO2路径:").grid(column=1, row=1, sticky=(W, E))
    key_path_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=r"F:\05 Game\YGOPro2"))
    key_path_entry.grid(column=2, row=1, sticky=(W, E))

    Label(deck_generator, text="系列名称:").grid(column=1, row=11, sticky=(W, E))
    series_name_entry = Entry(deck_generator, width=25, textvariable=StringVar(value="Temporarily useless"))
    series_name_entry.grid(column=2, row=11)

    Label(deck_generator, text="生成卡组名称:").grid(column=1, row=12, sticky=(W, E))
    default_name = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time())) + '.ydk'
    deck_name_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=default_name))
    deck_name_entry.grid(column=2, row=12)

    Label(deck_generator, text="随机卡片数量:").grid(column=1, row=13, sticky=(W, E))
    deck_length_entry = Entry(deck_generator, width=25, textvariable=StringVar(value="60"))
    deck_length_entry.grid(column=2, row=13)

    Button(deck_generator, text="Yu-Gi-Oh！", command=generate_deck_file).grid(column=2, row=21)

    deck_generator.mainloop()
