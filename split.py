# input = raw_input("masukkan: ")

import re


string="juan:keluarParkir"
mat = re.findall(r'^\w+|\w+$', string)
print(mat)[0]
