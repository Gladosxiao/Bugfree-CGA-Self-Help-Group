import random
import time
from tkinter import *


def get_cards_data():
    with open("cards.txt", 'rb') as file:
        data = file.readlines()
    series_dict = {}
    for line in data:
        line = str(line)
        if 'INSERT or replace into datas values' in line:
            line_index_1 = line.find('(')
            line_index_2 = line.find(')')
            line_data = line[line_index_1 + 1:line_index_2].split(',')
            if not line_data[3] == '0x0':
                epochs = int(len(line_data[3]) / 2 - 1)
                for epoch in range(epochs):
                    series = line_data[3][2 * epoch + 2:2 * epoch + 4]
                    if not series == '00':
                        if series in series_dict.keys():
                            series_dict[series].append(line_data[0])
                        else:
                            series_dict[series] = [line_data[0]]
    random_pool = {}
    for key in series_dict.keys():
        if len(series_dict[key]) > 13:
            random_pool[key] = series_dict[key]
    return random_pool


def generate_deck_file():
    key_path = key_path_entry.get()
    key_path.replace('\\', "\\\\")
    series_name = series_name_entry.get()
    deck_name = deck_name_entry.get()
    deck_length = int(deck_length_entry.get())

    # Generate the deck content
    card_pool = series_data[series_name]
    random_cards = []
    while len(random_cards) < deck_length:
        random_cards += random.sample(card_pool, 2)

    deck = "#created by ygopro2\n#main\n" + "\n".join(random_cards) + "#extra\n!side\n"
    with open(key_path + "\\deck\\" + deck_name, 'w') as deck_file:
        deck_file.write(str(deck))

    refresh()


def refresh():
    def entry_set(entry, value):
        entry.delete(0, END)
        entry.insert(0, value)

    new_series_name = random.sample(series_data.keys(), 1)
    entry_set(series_name_entry, new_series_name)

    new_deck_name = time.strftime('%m%d', time.localtime(time.time())) + ''.join(new_series_name) + '.ydk'
    entry_set(deck_name_entry, new_deck_name)


if __name__ == "__main__":
    series_data = get_cards_data()

    deck_generator = Tk()
    deck_generator.title("YGO卡组生成器")

    Label(deck_generator, text="YGOPRO2路径:").grid(column=1, row=1, sticky=(W, E))
    key_path_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=r"F:\05 Game\YGOPro2"))
    key_path_entry.grid(column=2, row=1, sticky=(W, E))

    Label(deck_generator, text="系列名称:").grid(column=1, row=11, sticky=(W, E))
    random_series_name = random.sample(series_data.keys(), 1)
    series_name_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=random_series_name))
    series_name_entry.grid(column=2, row=11)

    Label(deck_generator, text="生成卡组名称:").grid(column=1, row=12, sticky=(W, E))
    default_name = time.strftime('%m%d', time.localtime(time.time())) + ''.join(random_series_name) + '.ydk'
    deck_name_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=default_name))
    deck_name_entry.grid(column=2, row=12)

    Label(deck_generator, text="随机卡片数量:").grid(column=1, row=13, sticky=(W, E))
    deck_length_entry = Entry(deck_generator, width=25, textvariable=StringVar(value="60"))
    deck_length_entry.grid(column=2, row=13)

    Button(deck_generator, text="Yu-Gi-Oh！", command=generate_deck_file).grid(column=2, row=21)

    deck_generator.mainloop()
