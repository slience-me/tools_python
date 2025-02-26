# Author: slience_me
# Date: 2025/2/26 12:41
# Blog: https://slienceme.cn


import os
import re

# 读取Markdown文件并提取图片路径
def extract_image_paths(md_file_path):
    # 正则表达式匹配图片路径
    img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    image_paths = []

    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        image_paths = img_pattern.findall(content)

    image_paths = [str(name).replace('/images/', '') for name in image_paths]

    return image_paths

# 检查图片是否存在于指定文件夹
def check_images_in_folder(image_paths, folder_path):
    existing_images = []

    for image_path in image_paths:
        # 拼接完整路径
        image_full_path = os.path.join(folder_path, os.path.basename(image_path))

        if not os.path.exists(image_full_path):
            existing_images.append(image_path)

    return existing_images

# 使用示例
md_file = 'D:\codeHub\\notebook\DevNotes\docs\\notes\python\matplotlib.md'  # Markdown文件路径
folder = 'D:\codeHub\\notebook\DevNotes\docs\public\images'      # 图片存储文件夹路径

# 获取Markdown文件中的图片路径
image_paths = extract_image_paths(md_file)

# 判断图片是否存在于文件夹
not_existing_images = check_images_in_folder(image_paths, folder)

# 输出存在的图片路径
print("不存在的图片:")
for image in not_existing_images:
    print(image)
