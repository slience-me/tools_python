# -*- coding: utf-8 -*-
# @Time    : 2024/1/8 21:21
# @Author  : slience_me
# @FileName: main.py
# @Software: PyCharm
# @Blog    : https://slienceme.xyz
import numpy as np
import pandas as pd

# 读取 .npy 文件
full_data = np.load('data/DASHlink_full_fourclass_raw_comp.npz')
data = full_data['data']
label = full_data['label']

# 转换为 DataFrame
df = pd.DataFrame(data)
df_l = pd.DataFrame(label)

# 保存为 .csv 文件
df.to_csv('data.csv', index=False)  # index=False 可以防止保存索引列
df_l.to_csv('label.csv', index=False)  # index=False 可以防止保存索引列
