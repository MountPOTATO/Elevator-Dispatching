'''
Author: mount_potato
Date: 2021-04-26 16:10:03
LastEditTime: 2021-04-29 00:38:52
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \os_elevator\elevator_ui.py
'''
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *


from utils import *


#TODO:设置按钮长按效果

class Ui_MainWindow(object):
    def __init__(self):
        
        #模块集合集合
        self.elevator_pos=[]  #电梯图标坐标的位置
        self.elevator_lcd_pos=[] #电梯LCD楼层显示的位置
        self.inner_open_button_pos=[] #五台电梯内部按钮位置，关闭，警告根据与它的相对位置推出
        self.inner_level_one_button_pos=[] #五台电梯内部按钮
        self.outer_level_one_button_up_pos=[] #电梯外部一楼上按钮
        self.outer_level_one_button_down_pos=[] #电梯内部一楼下按钮

        self.elevator_open_image=[] #电梯开门图标的位置
        self.elevator_close_image=[] #电梯关门图标的位置
        self.open_gif_label=[]  #电梯开门动画标签，用时1s
        self.close_gif_label=[]  #电梯关门动画标签，用时1s
        self.elevator_lcd=[] #电梯LCD楼层

        self.inner_open_button=[]   #电梯内部开门按钮
        self.inner_close_button=[]  #电梯内部关门按钮
        self.inner_warn_button=[]   #电梯内部警报按钮
        #self.inner_level_button=[[0 for x in range(NUM_ELEVATOR)]for y in range(NUM_LEVEL)]  #电梯内部楼层按钮
        self.inner_level_button=[[] for i in range(NUM_ELEVATOR)]  #电梯内部楼层按钮
        self.outer_up_button=[]    #电梯外的上楼按钮
        self.outer_down_button=[]  #电梯外的下楼按钮

        
    
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(1550,656)
        MainWindow.resize(1240,980)
        MainWindow.setStyleSheet("")
        self.central_widget=QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralWidget")

        #LayoutWidget设置
        self.layout_widget = QtWidgets.QWidget(self.central_widget)
        self.layout_widget.setGeometry(QtCore.QRect(300, 240, 111, 31))
        self.layout_widget.setObjectName("layoutWidget")

        self.textBrowser=QtWidgets.QTextBrowser(self.central_widget)

        #按钮qss读入
        warn_button_style=QSS_READER.read("style/inner_warn_button.qss")
        op_button_style=QSS_READER.read("style/inner_op_button.qss")
        level_button_style=QSS_READER.read("style/inner_level_button.qss")
        lcd_number_style=QSS_READER.read("style/lcd_number.qss")
        outer_button_style=QSS_READER.read("style/outer_button.qss")

        #设置Qt字体
        font=QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        #组件位置信息初始化
        self.elevator_pos.extend([30, 260, 490, 720, 950])    #初设电梯图片位置
        self.elevator_lcd_pos.extend([100,330,560,790,1020])  #初设电梯LCD位置
        self.inner_open_button_pos.extend([70,300,530,760,990])
        self.inner_level_one_button_pos.extend([50,280,510,740,970])
        self.outer_level_one_button_up_pos.extend([250,600])
        self.outer_level_one_button_down_pos.extend(([300,650]))

        #输出框设置
        self.textBrowser.setGeometry(QtCore.QRect(720,560,441,250))

        for i in range (0,NUM_ELEVATOR):
            
            #放入开门电梯的图像
            self.elevator_open_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_open_image[i].setGeometry(QtCore.QRect(self.elevator_pos[i], 360, 191,181))
            self.elevator_open_image[i].setPixmap(QtGui.QPixmap("resources/elevator/elevator_open.png"))
            self.elevator_open_image[i].setObjectName("elevatorOpenImage"+str(i))
            self.elevator_open_image[i].setVisible(True)
            
            #放入关门电梯的图像
            self.elevator_close_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_close_image[i].setGeometry(QtCore.QRect(self.elevator_pos[i], 360, 191,181))
            self.elevator_close_image[i].setPixmap(QtGui.QPixmap("resources/elevator/elevator_closed.png"))
            self.elevator_close_image[i].setObjectName("elevatorCloseImage"+str(i))
            self.elevator_close_image[i].setVisible(False)

            self.open_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.open_gif_label[i].setGeometry(QtCore.QRect(self.elevator_pos[i], 360, 191,181))
            self.open_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/open_ani.gif"))

            #TODO:调用动画方法
            #self.open_gif_label[i].movie().start()
            #self.open_gif_label[i].show()

            self.close_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.close_gif_label[i].setGeometry(QtCore.QRect(self.elevator_pos[i], 360, 191,181))
            self.close_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/close_ani.gif"))


            #放入LCD
            self.elevator_lcd.append(QtWidgets.QLCDNumber(self.central_widget))
            self.elevator_lcd[i].setStyleSheet(lcd_number_style)
            self.elevator_lcd[i].setGeometry(QtCore.QRect(self.elevator_lcd_pos[i], 290, 51, 61))
            self.elevator_lcd[i].setFrameShape(QtWidgets.QFrame.Box)
            self.elevator_lcd[i].setFrameShadow(QtWidgets.QFrame.Raised)
            self.elevator_lcd[i].setLineWidth(4)
            self.elevator_lcd[i].setSmallDecimalPoint(False)
            self.elevator_lcd[i].setDigitCount(2)
            self.elevator_lcd[i].setMode(QtWidgets.QLCDNumber.Dec)
            self.elevator_lcd[i].setProperty("value", 1.0)
            self.elevator_lcd[i].setProperty("intValue", 1)
            self.elevator_lcd[i].setObjectName("elevatorLCD"+str(i))

            #开门按钮加入组件
            self.inner_open_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_open_button[i].setStyleSheet(op_button_style)
            self.inner_open_button[i].setGeometry(QtCore.QRect(self.inner_open_button_pos[i], 240, 31, 31))
            self.inner_open_button[i].setObjectName("innerOpenButton"+str(i))
            #开门按钮设置槽函数InnerOpButtonClicked
            self.inner_open_button[i].clicked.connect(MainWindow.InnerOpButtonClicked)
            #关门按钮加入组件
            self.inner_close_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_close_button[i].setStyleSheet(op_button_style)
            self.inner_close_button[i].setGeometry(QtCore.QRect(self.inner_open_button_pos[i]+40, 240, 31, 31))
            self.inner_close_button[i].setObjectName("innerCloseButton"+str(i))
            #关门按钮设置槽函数InnerOpButtonClicked
            self.inner_close_button[i].clicked.connect(MainWindow.InnerOpButtonClicked)
            #警告按钮加入组件
            self.inner_warn_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_warn_button[i].setStyleSheet(warn_button_style)
            self.inner_warn_button[i].setGeometry(QtCore.QRect(self.inner_open_button_pos[i] + 80, 240, 31, 31))
            self.inner_warn_button[i].setObjectName("innerWarnButton"+str(i))
            #警告按钮设置槽函数InnerWarnButtonClicked
            self.inner_warn_button[i].clicked.connect(MainWindow.InnerWarnButtonClicked)

            #添加每个电梯的内部楼层按钮
            self.inner_level_button.append(QtWidgets.QPushButton(self.central_widget))
            for j in range(0,NUM_LEVEL):
                self.inner_level_button[i].append(QtWidgets.QPushButton(self.central_widget))
                self.inner_level_button[i][j].setStyleSheet(level_button_style)
                self.inner_level_button[i][j].setGeometry(
                    QtCore.QRect(self.inner_level_one_button_pos[i]+40*(j%4), 200-40*(int(j/4)), 31, 31))
                self.inner_level_button[i][j].setObjectName("innerLevelButton_" + str(i) + "_" + str(j))
                #每个楼层按钮设置槽函数
                self.inner_level_button[i][j].clicked.connect(MainWindow.InnerLevelButtonClicked)


        #添加外部每个楼层的上下按钮
        for j in range(0,NUM_LEVEL):
            self.outer_up_button.append(QtWidgets.QPushButton(self.central_widget))
            self.outer_up_button[j].setStyleSheet(outer_button_style)
            self.outer_up_button[j].setGeometry(
                  QtCore.QRect(self.outer_level_one_button_up_pos[int(j / 10)], 910 - 40 * (j % 10), 31, 31))
            self.outer_up_button[j].setObjectName("OuterUpButton" + str(j))

            self.outer_down_button.append(QtWidgets.QPushButton(self.central_widget))
            self.outer_down_button[j].setStyleSheet(outer_button_style)
            self.outer_down_button[j].setGeometry(
                QtCore.QRect(self.outer_level_one_button_down_pos[int(j / 10)], 910 - 40 * (j % 10), 31, 31))
            self.outer_down_button[j].setObjectName("OuterDownButton"+str(j))
            #外部操作按钮设置槽函数
            self.outer_up_button[j].clicked.connect(MainWindow.OuterButtonClicked)
            self.outer_down_button[j].clicked.connect(MainWindow.OuterButtonClicked)
        

        
        #Menubar和Statebar设定
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar=QtWidgets.QMenuBar(MainWindow)
        self.statusbar=QtWidgets.QStatusBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,1550,18))
        self.menubar.setObjectName("Menu Bar")
        self.statusbar.setObjectName("Status Bar")
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.printMessage("电梯1")
        
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        for i in range(0,NUM_ELEVATOR):
            self.inner_open_button[i].setText(_translate("MainWindow", "开"))
            self.inner_close_button[i].setText(_translate("MainWindow", "关"))
            self.inner_warn_button[i].setText(_translate("MainWindow", "✖"))

            for j in range(0,NUM_LEVEL):
                self.inner_level_button[i][j].setText(_translate("MainWindow",str(j+1)))
        
        for j in range(0,NUM_LEVEL):
            self.outer_up_button[j].setText(_translate("MainWindow","▲"))
            self.outer_down_button[j].setText(_translate("MainWindow","▼"))

    def printMessage(self,text_string):
        self.textBrowser.append(text_string)
        self.cursor=self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()

    #槽函数设置
    #TODO:设置槽函数内部信息
    def InnerLevelButtonClicked(self):
        pass

    def InnerOpButtonClicked(self):
        pass

    def InnerWarnButtonClicked(self):
        pass

    def OuterButtonClicked(self):
        pass

    #TODO:在调度器中与本窗口连接，使得调度器可使用printMessage输出调度信息
    








