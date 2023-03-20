 # -*- coding: utf-8 -*-
"""
@author:zhangchen
@time:2023-03-20
"""
import sys, ctypes
from PyQt5.QtWidgets import *
from MyWindow import MyWindow


if __name__ == "__main__" :
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    sys.exit(app.exec_())