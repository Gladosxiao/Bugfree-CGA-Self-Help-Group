# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:32:25 2020

@author: GlaDo
"""

import os
import random
import time

key_path = "D:\\YGOPro2\\picture\\card"
file_name = os.listdir(key_path)
main = [i[:-4] for i in random.sample(file_name, 50)]
extra = [i[:-4] for i in random.sample(file_name, 15)]

deck = "#created by ygopro2\n#main\n"
deck += "\n".join(main)
deck += "#extra\n"
deck += "\n".join(extra)
deck += "!side\n"

deck_file = open(str(time.time()) + '.ydk', 'w')
deck_file.write(str(deck))
deck_file.close()