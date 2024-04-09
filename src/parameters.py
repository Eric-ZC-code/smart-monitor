 # -*- coding: utf-8 -*-
"""
@author:zhangchen
@time:2024-04-20
"""
from enum import Enum

class Args(Enum):
    camera_0 = 0 # USB摄像头
    camera_1 = "rtsp://user2:1234abcd@120.224.60.237:554/Streaming/Channels/101" # rtsp协议获取网络摄像头
    camera_2 = 'http://admin:12345@192.168.1.101:8081/' # http协议获取ip摄像头
    video_0 = "./camera_cap/gangsters/gangster.mp4" # 歹徒入侵视频
    all_path = "./camera_cap/all"
    pos_path = "./camera_cap/positive"
    log_path = "./log"

class Models(Enum):
    person_exist = "./models/PPLCNet_x1_0_person" # 推测有人/无人的模型
    person_attribute = "./models/PPLCNet_x1_0_person_attribute_infer" # 推测人物属性的模型

class Picture(Enum):
    # camera
    camera_0 = "./pic/camera_0.jpeg"
    camera_1 = "./pic/camera_1.jpg"
    camera_2 = "./pic/camera_2.jpeg"
    camera_3 = "./pic/camera_3.jpeg"
    # screen
    screen_0 = "./pic/screen_0.jpg"
    screen_1 = "./pic/screen_1.jpg"
    # screenshot
    screenshot_0 = "./pic/screenshot_0"
    screenshot_1 = "./pic/screenshot_1"

class Face(Enum):
    # face
    xintao = ["./pic/face_database/xintao.jpg"]
    yihao = ["./pic/face_database/yihao.jpg"]
    yixin = ["./pic/face_database/yixin.jpg"]
    zhaoyuzhuo = ["./pic/face_database/zhaoyuzhuo.jpg"]
    zhangchen = ["./pic/face_database/zhangchen/1.jpg", 
                 "./pic/face_database/zhangchen/2.jpg", 
                 "./pic/face_database/zhangchen/3.jpg",
                 "./pic/face_database/zhangchen/4.jpg",
                 "./pic/face_database/zhangchen/5.jpg",]



