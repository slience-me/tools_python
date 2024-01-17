# -*- coding: utf-8 -*-
# @Time    : 2024/1/17 9:59
# @Author  : slience_me
# @FileName: main.py
# @Software: PyCharm
# @Blog    : https://slienceme.xyz


if __name__ == '__main__':

    input_file_path = 'test.log'
    output_file_path = 'result.log'

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            if 'cost time:' not in line:
                output_file.write(line)
