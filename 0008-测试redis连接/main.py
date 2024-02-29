# -*- coding: utf-8 -*-
# @Time    : 2024/2/29 10:35
# @Author  : slience_me
# @FileName: main.py
# @Software: PyCharm
# @Blog    : https://slienceme.xyz
import redis


def test_redis_connection(host, port, password=None):
    try:
        # 创建Redis连接
        r = redis.Redis(host=host, port=port, password=password)
        # 测试连接
        r.ping()
        print("Redis 连接成功！")
    except redis.ConnectionError:
        print("无法连接到 Redis 服务器，请检查配置。")
    except Exception as e:
        print("发生异常：", e)


if __name__ == '__main__':
    # 假设你的Redis服务器在本地，端口为6379，没有密码
    test_redis_connection('192.168.5.130', 6379)
