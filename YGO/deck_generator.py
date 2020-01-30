"""
F:
cd F:\01 Codes\Python\YuGiOh
pyinstaller -Fw deck_generator.py
"""
import random
import time
from tkinter import *


def analysis_cards_cdb(set_name_path, card_path):
    def dictionary_append(dictionary, key, value):
        if key in dictionary.keys():
            dictionary[key].append(value)
        else:
            dictionary[key] = [value]

    series_name_dict = {}
    with open(set_name_path, "r", encoding='utf-8') as set_name_file:
        set_name_data = set_name_file.readlines()
    for set_name_line in set_name_data[1:]:
        line_data = set_name_line.split(' ')
        series_name_dict[line_data[1]] = line_data[2].split('\t')[0].replace('\n', '')

    with open(card_path, 'rb') as card_file:
        card_data = card_file.readlines()
    card_dict = {}
    series_dict = {}
    for card_line in card_data:
        card_line = str(card_line)
        if 'INSERT or replace into datas values' in card_line:
            line_index_1 = card_line.find('(')
            line_index_2 = card_line.find(')')
            line_data = card_line[line_index_1 + 1:line_index_2].split(',')

            card_number = line_data[0]
            allowed_quantity = eval(line_data[1])
            set_name_index = line_data[3]
            card_type = line_data[4]

            if allowed_quantity == 0 or eval(set_name_index) == 0:
                continue

            if eval(card_type) & 0x4802040:
                card_dict[card_number] = [True, allowed_quantity]
            else:
                card_dict[card_number] = [False, allowed_quantity]

            if set_name_index in series_name_dict.keys():
                set_name = series_name_dict[set_name_index]
                dictionary_append(series_dict, set_name, card_number)
            elif '00' in set_name_index:
                set_name_index_list = set_name_index[2:].split('00')
                for set_name_index_item in set_name_index_list:
                    if '0x' + set_name_index_item in series_name_dict.keys():
                        set_name = series_name_dict['0x' + set_name_index_item]
                        dictionary_append(series_dict, set_name, card_number)
                    else:
                        dictionary_append(series_dict, '0x' + set_name_index_item, card_number)
            else:
                dictionary_append(series_dict, set_name_index, card_number)

    random_pool = {}
    for set_name in series_dict.keys():
        if len(series_dict[set_name]) > 15:
            random_pool[set_name] = series_dict[set_name]

    return card_dict, random_pool


def generate_deck_file():
    key_path = key_path_entry.get()
    key_path.replace('\\', "\\\\")
    series_name = series_name_entry.get()
    deck_name = deck_name_entry.get()
    deck_length = int(deck_length_entry.get())

    # Generate the deck content
    card_pool = series_random_pool[series_name]
    main_cards = []
    extra_cards = []
    count = 0
    while len(main_cards) < deck_length:
        random_card_name = random.sample(card_pool, 1)[0]
        extra, allowed_quantity = card_data_dict[random_card_name]
        if extra and len(extra_cards) < 15:
            if extra_cards.count(random_card_name) < allowed_quantity:
                extra_cards.append(random_card_name)
        else:
            if main_cards.count(random_card_name) < allowed_quantity:
                main_cards.append(random_card_name)
        count += 1
        if count > 10 * deck_length:
            break

    deck = "#created by ygopro2\n#main\n" + "\n".join(main_cards) + "#extra\n" + "\n".join(extra_cards) + "!side\n"
    with open(key_path + "\\deck\\" + deck_name, 'w') as deck_file:
        deck_file.write(str(deck))
    print(deck_name, len(main_cards), len(extra_cards))


def refresh():
    def entry_set(entry, value):
        entry.delete(0, END)
        entry.insert(0, value)

    new_series_name = random.sample(series_random_pool.keys(), 1)[0]
    entry_set(series_name_entry, new_series_name)

    new_deck_name = time.strftime('%y%m%d', time.localtime(time.time()))[2:] + new_series_name + '.ydk'
    entry_set(deck_name_entry, new_deck_name)


if __name__ == "__main__":
    card_data_dict, series_random_pool = analysis_cards_cdb("set_name.txt", "cards.txt")
    deck_generator = Tk()
    deck_generator.title("YGO卡组生成器")

    Label(deck_generator, text="YGOPRO2路径:").grid(column=1, row=1, sticky=(W, E))
    key_path_entry = Entry(deck_generator, width=25, textvariable=StringVar(value=r"F:\05 Game\YGOPro2"))
    key_path_entry.grid(column=2, row=1, sticky=(W, E))

    Label(deck_generator, text="系列名称:").grid(column=1, row=11, sticky=(W, E))
    series_name_entry = Entry(deck_generator, width=25)
    series_name_entry.grid(column=2, row=11)

    Label(deck_generator, text="生成卡组名称:").grid(column=1, row=12, sticky=(W, E))
    deck_name_entry = Entry(deck_generator, width=25)
    deck_name_entry.grid(column=2, row=12)

    Label(deck_generator, text="随机卡片数量:").grid(column=1, row=13, sticky=(W, E))
    deck_length_entry = Entry(deck_generator, width=25, textvariable=StringVar(value="40"))
    deck_length_entry.grid(column=2, row=13)

    Button(deck_generator, text="验证血统", command=refresh).grid(column=1, row=21)
    Button(deck_generator, text="Yu-Gi-Oh！", command=generate_deck_file).grid(column=2, row=21)

    deck_generator.mainloop()
