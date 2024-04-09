 # -*- coding: utf-8 -*-
"""
@author:zhangchen
@time:2023-03-20
"""
import sys, ctypes
import threading, cv2, datetime, os, requests
import numpy as np
import paddleclas
import face_recognition
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from parameters import *
from face_db import know_face_encodings, know_face_names
from methods import delAll, re_attributes, save_pos
from ui_Detection import Ui_Form


window_on = True

class MyWindow(QMainWindow):
    # 声明一个信号
    my_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.init_ui()
        self.imgName = []
        self.msg_history = list()  # 用来存放消息
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 创建显示视频流的lab1和显示抓拍图片的lab2
        self.lab1 = self.ui.label
        self.lab2 = self.ui.label_2
        self.lab1.setPixmap(QPixmap(Picture.screen_1.value))
        self.lab2.setPixmap(QPixmap(Picture.screenshot_0.value))

        # 创建显示人物特征信息的textbrowser
        self.textbrowser = self.ui.textBrowser

        # 设置右键菜单
        self.listView = self.ui.listView
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单
        self.listView.customContextMenuRequested[QtCore.QPoint].connect(self.rightMenuShow)
 
        # 创建按钮
        self.btnOK = self.ui.pushButton
        self.selectbtn = self.ui.pushButton_2
        self.warningbtn = self.ui.pushButton_3

        # 查看按钮状态
        self.checkBox1 = QCheckBox()
        self.checkBox1.setChecked(False)
        self.checkBox1.stateChanged.connect(lambda: self.btnstate(self.checkBox1))
 
        # 用来显示检测到的信息
        self.lab_msg = QLabel("")
        self.lab_msg.resize(640, 15)
        self.lab_msg.setWordWrap(True)  # 自动换行
        self.lab_msg.setAlignment(Qt.AlignTop)  # 靠上
        # self.lab_msg.setStyleSheet("background-color: yellow; color: black;")

        # 创建一个滚动对象
        scroll = self.ui.scrollArea
        scroll.setWidget(self.lab_msg)

        # 添加顶部菜单栏
        bar = self.menuBar()
        file = bar.addMenu("Start")
        edit = bar.addMenu("About")
        file.addAction("Open")
        file.addAction("Edit")
        file.addAction("Quit")
 
        # 窗口
        self.setWindowTitle('SmartMonitor')
        self.setWindowIcon(QIcon(Picture.camera_3.value))
        self.center()

        # 绑定事件
        self.selectbtn.clicked.connect(self.openimage)
        self.listView.doubleClicked.connect(self.clicked)
        self.listView.clicked.connect(self.clicked)
        self.btnOK.clicked.connect(self.camera)
        self.warningbtn.clicked.connect(self.check)

        # 绑定信号和槽
        self.my_signal.connect(self.my_slot)

        # 弹窗输入ntfy topic
        self.getTopic()

    def my_slot(self, msg):
        # 更新内容
        print(msg)
        self.msg_history.append(msg)
        self.lab_msg.setText("<br>".join(self.msg_history))
        self.lab_msg.resize(640, self.lab_msg.frameSize().height() + 20)
        self.lab_msg.repaint()  # 更新内容，如果不更新可能没有显示新内容

        # 定时清空滚动条
        if self.lab_msg.frameSize() == QtCore.QSize(617, 1496):
            self.msg_history = []
            self.lab_msg.clear()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def rightMenuShow(self):
        rightMenu = QtWidgets.QMenu(self.listView)
        # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。
        removeAction = QtWidgets.QAction(u"Delete", self, triggered=self.removeimage) 
        rightMenu.addAction(removeAction)
        rightMenu.exec_(QtGui.QCursor.pos())
 
    def btnstate(self, btn):
        chk1Status = self.checkBox1.isChecked()
        print(chk1Status)
        if chk1Status:
            QMessageBox.information(self, "Tips", "是", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            QMessageBox.information(self, "Tips", "否")
 
    def clicked(self, qModelIndex):
        # 显示抓拍图片
        QMessageBox.information(self, "图片", "你选择了: "+ img_names[qModelIndex.row()])
        qp = QPixmap(imgFullPath[qModelIndex.row()])
        self.lab2.setPixmap(QPixmap.scaled(qp, 400, 300, aspectRatioMode=Qt.IgnoreAspectRatio))
        pic_path = imgFullPath[qModelIndex.row()]

        # 检测人物特征
        model_a = paddleclas.PaddleClas(model_name="person_attribute", batch_size = 64)
        result_a= model_a.predict(input_data=pic_path)

        # 显示人物特征
        self.textbrowser.clear()
        for result in result_a:
            person_info = re_attributes(result)
            for item in person_info:
                self.textbrowser.append(item)
            self.textbrowser.repaint()

    def openimage(self):
        global img_names
        global imgFullPath
        imgFullPath, imgType = QtWidgets.QFileDialog.getOpenFileNames(
            self, "多文件选择", "camera_cap", "Images (*.png *.xpm *.jpg)")
        
        # 得到图片名称
        img_names = []
        for p in imgFullPath:
            imgPath, imgName = os.path.split(p)
            img_names.append(imgName)
        
        slm = QStringListModel()
        slm.setStringList(img_names)
        self.listView.setModel(slm)
 
    def removeimage(self):
        selected = self.listView.selectedIndexes()
        itemmodel = self.listView.model()
        for i in selected:
            itemmodel.removeRow(i.row())

    def processimage(self):
        QMessageBox.information(self, "Tips", "Done!")

    def check(self):
        warning_file = Args.log_path.value + "\\warning.txt"
        os.startfile(warning_file)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        global window_on
        if reply == QMessageBox.Yes:
            window_on = False
            event.accept()
        else:
            window_on = True
            event.ignore()

    # 获取用户在ntfy平台的topic
    def getTopic(self):
        topic, ok = QInputDialog.getText(self, "ntfy topic", "请输入你的 ntfy topic", QLineEdit.PasswordEchoOnEdit, text="")
        if ok & (topic != ""):
            self.ntfy_topic = "https://ntfy.sh/" + topic
        else: 
            self.ntfy_topic = "https://ntfy.sh/app"
            QMessageBox.warning(self, "warning", "未输入topic，默认接收地址为https://ntfy.sh/app")

    def setcamera(self, cap):
        # 摄像头状态
        print('IP摄像头是否开启: {}'.format(cap.isOpened()))
 
        # 设置缓存区的大小
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print('buffersize: {}'.format(cap.get(cv2.CAP_PROP_BUFFERSIZE)))
 
        # 调节摄像头分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print('width:', cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('height:', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
        # 设置FPS
        fps = 30
        cap.set(cv2.CAP_PROP_FPS, fps)
        print('FPS值为:', cap.get(cv2.CAP_PROP_FPS))

    # 显示检测信息，同时发短信提示
    def warning(self, result, time_stamp):
        global sms
        class_ids = result[0]['class_ids'][0]
        msg = "正在监测[%s]的实时画面..." % time_stamp
        if class_ids == 1:
            # 显示检测信息
            self.my_signal.emit(msg + "【发现异常人员！！！】")
            # 发短信提示
            requests.post(self.ntfy_topic, data = (msg + "【发现异常人员！！！】").encode(encoding='utf-8'))
            # 保存报警信息
            with open(Args.log_path.value + "\\warning.txt", "a") as f:
                f.write("[%s]的实时画面中出现异常人员\n" % time_stamp)
        else:
            self.my_signal.emit(msg)

    def faceRec(self, know_face_encodings, know_face_names):
        # 发现人脸的位置
        locations = face_recognition.face_locations(self.frame)

        # 对图片人脸进行编码
        face_encodings = face_recognition.face_encodings(self.frame, locations)

        # 遍历locations,face_encodings，识别图片中的人脸
        for (top, right, bottom, left), face_encoding in zip(locations, face_encodings):
            # 比较人脸
            matches = face_recognition.compare_faces(know_face_encodings, face_encoding)

            # 查找匹配的人脸
            name = "unknown"
            if True in matches:
                index = matches.index(True)
                name = know_face_names[index]	

                # 标记人脸位置
                cv2.rectangle(self.frame, (left, top), (right, bottom), (0,0,255), 1)

                # 标记人脸姓名
                cv2.putText(self.frame, name, (left, top-20), cv2.FONT_HERSHEY_COMPLEX , 1, (255, 0, 0), 1)

    def processFrame(self, lock):
        lock.acquire() # 申请线程锁

        i = -20 # 帧索引（由于线程启动时间差距，前20帧无效）
        while window_on:
            cv2.waitKey(0)

            # 图片以时间戳命名
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            frame_path = Args.all_path.value + "\\" + time_stamp + ".jpg"
            pos_path = Args.pos_path.value + "\\" + time_stamp + ".jpg"

            # 保存所有图片
            cv2.imwrite(frame_path, self.frame)

            # 检测有人/无人
            model_e = paddleclas.PaddleClas(inference_model_dir=Models.person_exist.value, batch_size=64)
            result_e = model_e.predict(input_data=frame_path)
            
            # 处理检测结果
            for result in result_e:
                save_pos(result, pos_path, self.frame)
                self.warning(result, time_stamp)

            # 删除无效帧
            if i < 0:
                os.remove(frame_path)

            # 帧索引+1
            i = i + 1

        lock.release() # 释放线程锁

    def monitor(self, lock):
        lock.acquire() # 申请线程锁

        # 创建摄像头
        cap = cv2.VideoCapture(Args.camera_0.value)
        # 设置camera信息
        self.setcamera(cap)

        while window_on:
            ret, self.frame = cap.read()
            if ret:
                cv2.waitKey(1)

                # 标记人脸框
                self.faceRec(know_face_encodings, know_face_names)
                # 显示监控图像
                frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                self.img = QImage(frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                self.lab1.setPixmap(QPixmap(self.img))
            else:
                break

        # 释放VideoCapture对象
        cap.release()
        # 销毁所有窗口
        cv2.destroyAllWindows()

        lock.release() # 释放线程锁

    def camera_threads(self):
        # 创建线程锁，并行线程数量上限设为10
        lock = threading.BoundedSemaphore(10)

        # 创建线程
        thread_monitor = threading.Thread(target=self.monitor, args=(lock,), name="thread_monitor")
        thread_processFrame = threading.Thread(target=self.processFrame, args=(lock,), name="thread_processFrame")

        # 把线程添加到线程列表
        threads = []
        threads.append(thread_monitor)
        threads.append(thread_processFrame)

        # 启动线程
        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        # print(threading.active_count())
        # print(threading.enumerate())

    def camera(self):
        # 删除数据库原有文件
        delAll(Args.all_path.value)
        delAll(Args.pos_path.value)

        # 多线程执行
        self.camera_threads()


if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())
 