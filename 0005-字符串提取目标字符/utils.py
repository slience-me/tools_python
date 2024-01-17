# -*- coding: utf-8 -*-
# @Time    : 2024/1/10 9:23
# @Author  : slience_me
# @FileName: utils.py
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

Loss_Image([0.08225743141558549, 0.08029364023769801, 0.06008791516997728, 0.11111109245995418, 0.08711136025262796,
            0.11607186403637003, 0.1266402960192305, 0.1877888865436953, 0.35650418066384504, 0.4424873877796206,
            0.411358027580646, 0.4110798540681896, 0.41205430255815534, 0.41314131051006886, 0.4141546734378184,
            0.41502699886660765, 0.41573207191016415, 0.4162624864147441, 0.4166195994925381, 0.41681594442170444])
