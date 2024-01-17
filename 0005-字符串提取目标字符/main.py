# -*- coding: utf-8 -*-
# @Time    : 2024/1/10 9:09
# @Author  : slience_me
# @FileName: main.py
# @Software: PyCharm
# @Blog    : https://slienceme.xyz
from matplotlib import pyplot as plt


def Loss_Image(loss_values):
    plt.plot(loss_values, marker='o')  # marker='o' 用圆圈标记数据点
    plt.xlabel('Epochs')  # 设置 X 轴标签
    plt.ylabel('Loss')  # 设置 Y 轴标签
    plt.title('Training Loss over Epochs')  # 设置图表标题
    plt.grid(True)  # 添加网格线
    plt.savefig('images/2.png', dpi=300, bbox_inches='tight')  # 可以根据需要调整dpi，控制图片质量
    plt.show()

def fun1():
    # 打开日志文件
    file_path = 'temp.log'  # 替换为你的日志文件路径
    keyword = "训练损失值为"


    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line:
                # 找到包含关键词的行
                start_index = line.find(keyword)
                value_start_index = start_index + len(keyword) + 1  # 跳过关键词和冒号
                value = line[value_start_index:].strip().split()[0][:-1]  # 提取数值
                data_list.append(float(value))

    # 对data_list求平均值
    print("data_list为:", data_list)
    average = sum(data_list) / len(data_list)
    print("平均训练损失值为:", average)


def fun2():
    # 打开日志文件
    file_path = 'test.log'  # 替换为你的日志文件路径
    keyword = "Train Loss:"

    data_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if keyword in line:
                # 找到包含关键词的行
                start_index = line.find(keyword)
                value_start_index = start_index + len(keyword) + 1  # 跳过关键词和冒号
                value = line[value_start_index:].strip().split()[0][:-1]  # 提取数值
                data_list.append(float(value))

    # 对data_list求平均值
    print("data_list为:", data_list)
    average = sum(data_list) / len(data_list)
    print("平均训练损失值为:", average)
    return data_list

if __name__ == '__main__':

    Loss_Image(fun2())