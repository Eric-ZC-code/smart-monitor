 # -*- coding: utf-8 -*-
"""
@author:zhangchen
@time:2023-03-20
"""
import os
import cv2, time


# 删除指定路径上所有的文件和文件夹
def delAll(path):
    if os.path.isdir(path):
        files = os.listdir(path)  
        # 遍历并删除文件
        for file in files:
            p = os.path.join(path, file)
            if os.path.isdir(p):
                # 递归
                delAll(p)
            else:
                os.remove(p)
    else:
        pass


# 保存有人的图像 ("class_ids = 1")
def save_pos(result: list, path_pos, frame):
    class_ids = result[0]['class_ids'][0]
    if class_ids == 1:
        cv2.imwrite(path_pos, frame)
        time.ctime

# 返回人物特征的列表
def re_attributes(result: list) -> list:
    attributes = result[0]['attributes']
    return attributes

