"""
F:
cd F:\01 Codes\Python\YuGiOh
pyinstaller -Fw deck_generator.py
"""
import copy
import random
import time
from tkinter import *

# Todo: 同名异画卡

joint_set = """
弹丸 枪管
圣 阿托利斯 兰斯洛特
破坏剑 破坏之剑士
艾克佐迪亚 被封印
虫惑 洞 落穴
守墓 王家长眠之谷
六武众 影六武众 紫炎
魔术师 灵摆
"""
remove_set = """
融合
升阶魔法
帝王
"""


def dictionary_append(dictionary, key, value):
    if key in dictionary.keys():
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def prepare_analysis():
    universal_items = []
    with open("universal.ydk", 'r', encoding='utf-8') as universal_file:
        universal_data = universal_file.readlines()
    for universal_line in universal_data[2:]:
        if not ('extra' in universal_line or 'side' in universal_line):
            universal_items.append(universal_line.replace('\n', ''))

    joint_items = []
    for joint_line in joint_set.split('\n'):
        joint_items.append(joint_line.split(' '))

    remove_items = []
    for remove_line in remove_set.split('\n'):
        remove_items.append(remove_line)

    series_name_dict = {}
    with open("set_name.txt", "r", encoding='utf-8') as set_name_file:
        set_name_data = set_name_file.readlines()
    for set_name_line in set_name_data[1:]:
        # if '#' not in set_name_line:
        line_data = set_name_line.split(' ')
        series_name = line_data[2].split('\t')[0].replace('\n', '')
        if eval(line_data[1]) < 0xfff:
            series_name_dict[line_data[1]] = series_name
    return universal_items[1:-1], joint_items[1:-1], remove_items[1:-1], series_name_dict


def get_analysis_result():
    universal_items, joint_items, remove_items, series_name_dict = prepare_analysis()

    card_dict = {}
    series_dict = {}
    with open("cards.txt", 'rb') as card_file:
        card_data = card_file.readlines()
    for card_line in card_data:
        card_line = str(card_line)
        if 'INSERT or replace into datas values' in card_line:
            line_index_1 = card_line.find('(')
            line_index_2 = card_line.find(')')
            line_data = card_line[line_index_1 + 1:line_index_2].split(',')

            card_number = line_data[0]
            allowed_quantity = eval(line_data[1])
            card_type = eval(line_data[4])

            if allowed_quantity == 0 or card_type & 0x4000:  # or card_type & 0x8008:
                continue

            if card_number in universal_items:
                card_dict[card_number] = [card_type & 0x4802040, allowed_quantity]
                dictionary_append(series_dict, '泛用', card_number)

            set_name_index = line_data[3]
            if eval(set_name_index) == 0:
                continue

            if eval(set_name_index) > 0xfff:
                set_name_index = str(hex(eval('0x' + set_name_index[-3:])))

            card_dict[card_number] = [card_type & 0x4802040, allowed_quantity]
            if set_name_index in series_name_dict.keys():
                set_name = series_name_dict[set_name_index]
                dictionary_append(series_dict, set_name, card_number)
            else:
                dictionary_append(series_dict, set_name_index, card_number)

    for joint_item in joint_items:
        key_item = joint_item[0]
        for sub_item in joint_item[1:]:
            if sub_item in series_dict.keys():
                series_dict[key_item] = series_dict[key_item] + series_dict[sub_item]
                del series_dict[sub_item]

    for remove_item in remove_items:
        del series_dict[remove_item]

    return card_dict, series_dict


def generate_deck_file():
    def add_one_card(pool, main, extra, side):
        random_card_name = random.sample(pool, len(pool))[0]
        extra_flag, allowed_quantity = card_data_dict[random_card_name]
        side_count = side.count(random_card_name)
        if extra_flag:
            extra_count = extra.count(random_card_name)
            if extra_count + side_count < allowed_quantity:
                if len(extra) < 15:
                    extra.append(random_card_name)
                elif len(side) < 15:
                    side.append(random_card_name)
                else:
                    pool.remove(random_card_name)
            else:
                pool.remove(random_card_name)
        else:
            main_count = main.count(random_card_name)
            if main_count + side_count < allowed_quantity:
                if len(main) < deck_length:
                    main.append(random_card_name)
                elif len(side) < 15:
                    side.append(random_card_name)
                else:
                    pool.remove(random_card_name)
            else:
                pool.remove(random_card_name)
        return extra_flag, random_card_name

    key_path = key_path_entry.get()
    key_path.replace('\\', "\\\\")
    series_name = series_name_entry.get()
    deck_name = deck_name_entry.get()
    deck_length = int(deck_length_entry.get())

    main_cards = []
    extra_cards = []
    side_cards = []
    universal_card = copy.deepcopy(series_random_pool['泛用'])
    card_pool = copy.deepcopy(series_random_pool[series_name])

    while (len(main_cards) < deck_length or len(extra_cards) < 15) and len(card_pool) > 0:
        add_one_card(card_pool, main_cards, extra_cards, side_cards)

    if len(extra_cards) == 0:
        if len(main_cards) + 4 > deck_length:
            main_cards = main_cards[:deck_length - 4]
        # 超魔导
        main_cards.extend(['46986414', '74677422', '6172122'])
        extra_cards.extend(['37818794', '70369116', ])
        # 拷问
        main_cards.append('75732622')
        extra_cards.extend(['28776350', '98978921', '98978921'])
        extra_cards.extend(['99111753', '41999284', '41999284'])

    while (len(main_cards) < deck_length or len(extra_cards) < 15) and len(universal_card) > 0:
        is_extra, random_card = add_one_card(universal_card, main_cards, extra_cards, side_cards)
        if is_extra and random_card in universal_card:
            universal_card.remove(random_card)

    deck = "#created by ygopro2"
    deck += "\n#main\n" + "\n".join(main_cards)
    deck += "\n#extra\n" + "\n".join(extra_cards)
    deck += "\n!side\n" + "\n".join(side_cards)
    with open(key_path + "\\deck\\" + deck_name, 'w') as deck_file:
        deck_file.write(str(deck))

    print(deck_name, len(card_pool), len(main_cards), len(extra_cards), len(side_cards))


def refresh():
    def entry_set(entry, value):
        entry.delete(0, END)
        entry.insert(0, value)

    new_series_name = random.sample(series_random_pool.keys(), 1)[0]
    entry_set(series_name_entry, new_series_name)

    new_deck_name = time.strftime('%y%m%d', time.localtime(time.time())) + new_series_name + '.ydk'
    if '|' in new_deck_name:
        new_deck_name = new_deck_name.split('|')[0] + '.ydk'
    entry_set(deck_name_entry, new_deck_name)


if __name__ == "__main__":
    card_data_dict, series_random_pool = get_analysis_result()
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

    refresh()

    deck_generator.mainloop()
