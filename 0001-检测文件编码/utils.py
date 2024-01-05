import chardet

# 指定文件路径
file_path = ''

# 读取文件内容并检测编码
with open(file_path, 'rb') as file:
    rawdata = file.read()
    result = chardet.detect(rawdata)

# 从检测结果中获取编码
detected_encoding = result['encoding']

print(f"The detected encoding is: {detected_encoding}")

with open(file_path, 'r', encoding=detected_encoding) as file:
    content = file.read()
