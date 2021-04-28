'''
Author: mount_potato
Date: 2021-04-26 16:40:26
LastEditTime: 2021-04-26 20:27:07
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \os_elevator\main.py
'''

import sys,threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils import *
from elevator_ui import *


class ElevatorInterface(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ElevatorInterface,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Operator System Elevator Dispatcher')
        self.setWindowIcon(QIcon('resources/window_icon.png'))



if __name__=='__main__':
    app=QApplication(sys.argv)

    main_window=ElevatorInterface()
    main_window.show()

    sys.exit(app.exec())