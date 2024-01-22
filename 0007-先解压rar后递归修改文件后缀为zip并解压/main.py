# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 11:29
# @Author  : slience_me
# @FileName: main.py
# @Software: PyCharm
# @Blog    : https://slienceme.xyz
import os
import shutil
import patoolib


def extract_rar_files(root_folder):
    for folder_path, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(folder_path, file)

            # 判断是否为RAR文件
            if os.path.isfile(file_path) and file.endswith(".rar"):
                # 解压RAR文件
                patoolib.extract_archive(file_path, outdir=folder_path)


def modify_and_unzip_files(root_folder):
    for folder_path, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(folder_path, file)

            # 判断是否为文件
            if os.path.isfile(file_path):
                # 修改后缀为"ziw"的文件为"zip"
                if file.endswith(".ziw"):
                    new_file_path = os.path.join(folder_path, file.rsplit('.', 1)[0] + ".zip")

                    # 检查目标文件是否存在，如果存在，给新文件一个不同的名字
                    index = 1
                    while os.path.exists(new_file_path):
                        new_file_path = os.path.join(folder_path, file.rsplit('.', 1)[0] + f"_{index}.zip")
                        index += 1

                    os.rename(file_path, new_file_path)

                    # 解压操作
                    shutil.unpack_archive(new_file_path, folder_path, 'zip')

    print("递归操作完成")


# 替换为你的根文件夹路径
root_folder = "temp"

# 先解压RAR文件
extract_rar_files(root_folder)

# 再执行递归操作
modify_and_unzip_files(root_folder)
