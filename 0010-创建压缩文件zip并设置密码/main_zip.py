# Author: slience_me
# Date: 2025/6/4 17:17
# Blog: https://slienceme.cn
import os
from pathlib import Path

import pyzipper

# 1. 自己指定
# 要压缩的文件路径列表
file_list = [
    './data/example1.txt',
    './data/example2.png',
]

# 2. 自动遍历文件夹获取所有文件路径、
# file_list = get_all_files('./data')
def get_all_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths

# 3. 只压缩指定类型的文件（如只压图片或文本）
# file_list = get_files_by_extension('./data', ['.txt', '.png'])
def get_files_by_extension(folder_path, extensions):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths

# 4.递归获取所有文件
# file_list = [str(p) for p in Path('./data').rglob('*') if p.is_file()]

# 输出的zip文件名
zip_filename = 'secure_archive.zip'
# 设置的压缩密码
password = b'123456'

with pyzipper.AESZipFile(zip_filename,
                         'w',
                         compression=pyzipper.ZIP_DEFLATED,
                         encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(password)
    for file_path in file_list:
        zf.write(file_path, arcname=file_path)  # arcname 可自定义zip内的路径
