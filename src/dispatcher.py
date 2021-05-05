'''
Author: mount_potato
Date: 2021-04-29 00:31:57
LastEditTime: 2021-05-04 11:20:02
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Elevator-Dispatching\dispatcher.py
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from elevator_ui import *
from utils import *
import numpy as np
import time

class Dispatcher(object):
    def __init__(self,main_window):
        self.main_window=main_window

        self.by_task=NUM_ELEVATOR*[]
        self.oppo_task=NUM_ELEVATOR*[]

        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    
    def responseOBN(self,elevator_sn):
        pass
    

    def innerDispatch(self,target_level,curr_level):
        pass

    def outerDispatch(self,order,level):
        pass
    


    def update(self):
        pass
