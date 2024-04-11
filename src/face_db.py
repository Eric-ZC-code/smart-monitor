 # -*- coding: utf-8 -*-
"""
@author:zhangchen
@time:2024-04-20
"""

import face_recognition
from parameters import Face

# 加载并编码多张图像
def learn_face():
    known_face_encodings = []
    known_face_names = []

    for file in Face:
        name = file.name
        image_path = file.value
        # 加载图像文件
        image = face_recognition.load_image_file(image_path)
        # 查找图像中的人脸并编码
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            # 如果图像中存在人脸，则将编码存储到已知人脸编码列表中
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
        else:
            print("No face found in image:", image_path)

    return known_face_encodings, known_face_names

# 调用函数学习多张图像
known_face_encodings, known_face_names = learn_face()

