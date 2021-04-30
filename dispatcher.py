'''
Author: mount_potato
Date: 2021-04-29 00:31:57
LastEditTime: 2021-04-30 11:31:22
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Elevator-Dispatching\dispatcher.py
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from elevator_ui import *
from utils import *
import numpy as np
import time,threading

class Dispatcher(object):
    def __init__(self,main_window):
        self.main_window=main_window

    def responseOBN(self,elevator_sn):
        pass
