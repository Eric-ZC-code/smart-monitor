import cv2
import face_recognition
from parameters import Face

face_list = []
know_face_encodings = []
know_face_names = []

for f in Face:
    face_list.append(cv2.imread(f.value))
    know_face_names.append(f.name)

# 对图片中人脸进行编码
for face in face_list:
    know_face_encodings.append(face_recognition.face_encodings(face)[0])

