'''
Author: mount_potato
Date: 2021-04-26 16:10:03
LastEditTime: 2021-05-12 16:48:55
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \os_elevator\elevator_ui.py
'''
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *
import threading

from utils import *
from dispatcher import *




class Ui_MainWindow(object):

    def __init__(self):
        self.dispatcher=Dispatcher(self)
        
        #模块位置集合
        #电梯图标坐标的位置，动画位置与其位置相同
        self.elevator_x=[]  
        self.elevator_y=0 
        #电梯LCD楼层显示位置
        self.elevator_lcd_x=[] #电梯LCD楼层显示x轴位置
        self.elevator_lcd_y=0
        #五台电梯内部按钮位置，关闭，警告根据与它的相对位置推出
        self.inner_open_button_x=[]
        self.inner_open_button_y=0 
        #五台电梯内部一楼按钮位置，其他楼层按钮根据与它的相对位置推出
        self.inner_level_one_button_x=[] 
        self.inner_level_one_button_y=0 
        #电梯外部一楼上按钮位置，其他楼层按钮根据与它的相对位置推出
        self.outer_level_one_button_up_x=[] 
        self.outer_level_one_button_up_y=0
        #电梯内部一楼下按钮位置，其他楼层按钮根据与它的相对位置推出
        self.outer_level_one_button_down_x=[] 
        self.outer_level_one_button_down_y=0
        #电梯修理按钮位置
        self.repair_button_x=[] 
        self.repair_button_y=0
        #电梯上下标识动画位置
        self.up_down_gif_x=[] 
        self.up_down_gif_y=0
        #电梯标号图片位置设置
        self.mark_image_x=[]
        self.mark_image_y=0
        #楼层指示位置
        self.level_label_x=[] 
        self.level_label_y=0

        #界面模块
        self.elevator_open_image=[] #电梯开门图标
        self.elevator_close_image=[] #电梯关门图标
        self.elevator_mark_image=[]  #电梯标号图片位置
        self.open_gif_label=[]  #电梯开门动画标签，用时0.7s
        self.close_gif_label=[]  #电梯关门动画标签，用时0.7s
        self.up_gif_label=[]   #up动画标签 
        self.down_gif_label=[] #down动画标签
        self.elevator_lcd=[] #电梯LCD楼层
        self.repair_button=[] #电梯修理按钮
        self.level_label=[] # 楼层指示
        self.inner_open_button=[]   #电梯内部开门按钮
        self.inner_close_button=[]  #电梯内部关门按钮
        self.inner_warn_button=[]   #电梯内部警报按钮
        self.inner_level_button=[[] for i in range(NUM_ELEVATOR)]  #电梯内部楼层按钮
        self.outer_up_button=[]    #电梯外的上楼按钮
        self.outer_down_button=[]  #电梯外的下楼按钮

        
    
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1240,970)
        MainWindow.setStyleSheet("background-color:rgb(230,230,230);")
        self.central_widget=QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralWidget")
        MainWindow.setCentralWidget(self.central_widget)
        MainWindow.setWindowOpacity(0.95)

        self.textBrowser=QtWidgets.QTextBrowser(self.central_widget)

        #按钮qss文件读入
        self.warn_button_style=QSS_READER.read("style/inner_warn_button.qss")
        self.op_button_style=QSS_READER.read("style/inner_op_button.qss")
        self.level_button_style=QSS_READER.read("style/inner_level_button.qss")
        self.lcd_number_style=QSS_READER.read("style/lcd_number.qss")
        self.outer_button_style=QSS_READER.read("style/outer_button.qss")
        self.level_long_pressed_style=QSS_READER.read("style/inner_level_long_pressed.qss")
        self.warn_long_pressed_style=QSS_READER.read("style/inner_warn_long_pressed.qss")
        self.outer_long_pressed_style=QSS_READER.read("style/outer_long_pressed.qss")
        self.text_style=QSS_READER.read("style/label_text.qss")

        #组件位置信息初始化
        self.elevator_x.extend([30, 260, 490, 720, 950])    #初设电梯图片位置
        self.elevator_y=360  #电梯图标坐标的y轴位置 
        self.elevator_lcd_x.extend([100,330,560,790,1020])  #初设电梯LCD位置
        self.elevator_lcd_y=290 #电梯LCD楼层显示y轴位置
        self.up_down_gif_x.extend([160,390,620,850,1080])   #初设上下gif位置
        self.up_down_gif_y=290 #电梯LCD楼层显示y轴位置
        self.mark_image_x.extend([50,280,510,740,970])      #初设电梯标号图片位置
        self.mark_image_y=880
        self.inner_open_button_x.extend([70,300,530,760,990]) #初设电梯内开门按钮位置
        self.inner_open_button_y=240
        self.inner_level_one_button_x.extend([50,280,510,740,970]) #初设电梯内一楼按钮设置
        self.inner_level_one_button_y=200
        self.level_label_x.extend([160,510])   #初设电梯外楼层文本位置
        self.level_label_y=910
        self.outer_level_one_button_up_x.extend([250,600]) #初设电梯外一楼上按钮位置
        self.outer_level_one_button_up_y=910
        self.outer_level_one_button_down_x.extend([300,650]) #初设电梯外一楼下按钮位置
        self.outer_level_one_button_down_y=910
        self.repair_button_x.extend([755,835,915,995,1075]) #初设五个电梯修理按钮位置
        self.repair_button_y=830
        

        # #输出框设置
        self.textBrowser.setGeometry(QtCore.QRect(720,560,441,250))

        for i in range (0,NUM_ELEVATOR):
            
            #放入开门电梯的图像:命名规则i_eoi_电梯编号
            self.elevator_open_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_open_image[i].setGeometry(QtCore.QRect(self.elevator_x[i], self.elevator_y, 191,181))
            self.elevator_open_image[i].setPixmap(QtGui.QPixmap("resources/elevator/elevator_open.png"))
            self.elevator_open_image[i].setObjectName(open_img_name+str(i))
            self.elevator_open_image[i].setVisible(False)
            
            #放入关门电梯的图像:命名规则i_eci_电梯编号
            self.elevator_close_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_close_image[i].setGeometry(QtCore.QRect(self.elevator_x[i], self.elevator_y, 191,181))
            self.elevator_close_image[i].setPixmap(QtGui.QPixmap("resources/elevator/elevator_closed.png"))
            self.elevator_close_image[i].setObjectName(close_img_name+str(i))
            self.elevator_close_image[i].setVisible(True)

            #放入电梯开门动画标签:命名规则i_ogl_电梯编号
            self.open_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.open_gif_label[i].setGeometry(QtCore.QRect(self.elevator_x[i], self.elevator_y, 191,181))
            self.open_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/open_ani.gif"))
            self.open_gif_label[i].setObjectName(open_gif_name+str(i))
            self.open_gif_label[i].setVisible(False)
            self.open_gif_label[i].movie().setPaused(True)


            #放入电梯关门动画标签:命名规则i_cgl_电梯编号
            self.close_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.close_gif_label[i].setGeometry(QtCore.QRect(self.elevator_x[i], self.elevator_y, 191,181))
            self.close_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/close_ani.gif"))
            self.close_gif_label[i].setObjectName(close_gif_name+str(i))
            self.close_gif_label[i].setVisible(False)
            self.close_gif_label[i].movie().setPaused(True)
            self.close_gif_label[i].movie().setSpeed(70)

            #放入电梯上行动画标签:命名规则i_ugl_电梯编号
            self.up_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.up_gif_label[i].setGeometry(QtCore.QRect(self.up_down_gif_x[i], self.up_down_gif_y, 51,61))
            self.up_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/up.gif"))
            self.up_gif_label[i].setObjectName(up_gif_name+str(i))
            self.up_gif_label[i].setVisible(False)
            self.up_gif_label[i].movie().setPaused(False)
            self.up_gif_label[i].movie().setSpeed(100)

            #放入电梯下行动画标签:命名规则i_dgl_电梯编号
            self.down_gif_label.append(QtWidgets.QLabel(self.central_widget))
            self.down_gif_label[i].setGeometry(QtCore.QRect(self.up_down_gif_x[i], self.up_down_gif_y, 51,61))
            self.down_gif_label[i].setMovie(QtGui.QMovie("resources/elevator/down.gif"))
            self.down_gif_label[i].setObjectName(down_gif_name+str(i))
            self.down_gif_label[i].setVisible(False)
            self.down_gif_label[i].movie().setPaused(False)
            self.down_gif_label[i].movie().setSpeed(100)            

            #放入电梯标号图片:命名规则i_ugl_电梯编号
            self.elevator_mark_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_mark_image[i].setGeometry(QtCore.QRect(self.repair_button_x[i]+3, self.mark_image_y, 48,48))
            root="resources/mark/"+mark_img_name+str(i+1)+".png"
            self.elevator_mark_image[i].setPixmap(QtGui.QPixmap(root))
            self.elevator_mark_image[i].setObjectName(mark_img_name+str(i))
            self.elevator_mark_image[i].setVisible(True)            

            #放入LCD:命名规则i_lcd_电梯编号
            self.elevator_lcd.append(QtWidgets.QLCDNumber(self.central_widget))
            self.elevator_lcd[i].setStyleSheet(self.lcd_number_style)
            self.elevator_lcd[i].setGeometry(QtCore.QRect(self.elevator_lcd_x[i], self.elevator_lcd_y, 51, 61))
            self.elevator_lcd[i].setFrameShape(QtWidgets.QFrame.Box)
            self.elevator_lcd[i].setFrameShadow(QtWidgets.QFrame.Raised)
            self.elevator_lcd[i].setLineWidth(4)
            self.elevator_lcd[i].setSmallDecimalPoint(False)
            self.elevator_lcd[i].setDigitCount(2)
            self.elevator_lcd[i].setMode(QtWidgets.QLCDNumber.Dec)
            self.elevator_lcd[i].setProperty("value", 1.0)
            self.elevator_lcd[i].setProperty("intValue", 1)
            self.elevator_lcd[i].setObjectName(elevator_lcd_name+str(i))

            #放入修理按钮:命名规则o_rbn_电梯编号
            self.repair_button.append(QtWidgets.QPushButton(self.central_widget))
            self.repair_button[i].setStyleSheet(self.op_button_style)
            self.repair_button[i].setGeometry(QtCore.QRect(self.repair_button_x[i], self.repair_button_y, 48, 48))
            self.repair_button[i].setObjectName(repair_button_name+str(i))
            #修理按钮设置槽函数onRepairButtonClicked
            self.repair_button[i].clicked.connect(MainWindow.onRepairButtonClicked)

            #开门按钮加入组件:命名规则i_obn_电梯编号
            self.inner_open_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_open_button[i].setStyleSheet(self.op_button_style)
            self.inner_open_button[i].setGeometry(QtCore.QRect(self.inner_open_button_x[i],self.inner_open_button_y, 31, 31))
            self.inner_open_button[i].setObjectName(inner_open_button_name+str(i))
            #开门按钮设置触发函数InnerOpButtonClicked
            self.inner_open_button[i].clicked.connect(MainWindow.onInnerButtonClicked)
            #关门按钮加入组件：命名规则i_cbn_电梯编号
            self.inner_close_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_close_button[i].setStyleSheet(self.op_button_style)
            self.inner_close_button[i].setGeometry(QtCore.QRect(self.inner_open_button_x[i]+40, self.inner_open_button_y, 31, 31))
            self.inner_close_button[i].setObjectName(inner_close_button_name+str(i))
            #关门按钮设置触发函数InnerOpButtonClicked
            self.inner_close_button[i].clicked.connect(MainWindow.onInnerButtonClicked)
            #警告按钮加入组件：命名规则i_wbn_电梯编号
            self.inner_warn_button.append(QtWidgets.QPushButton(self.central_widget))
            self.inner_warn_button[i].setStyleSheet(self.warn_button_style)
            self.inner_warn_button[i].setGeometry(QtCore.QRect(self.inner_open_button_x[i] + 80, self.inner_open_button_y, 31, 31))
            self.inner_warn_button[i].setObjectName(inner_warn_button_name+str(i))
            #警告按钮设置触发函数onInnerButtonClicked
            self.inner_warn_button[i].clicked.connect(MainWindow.onInnerButtonClicked)

            #添加每个电梯的内部楼层按钮:命名规则i_lbn_电梯编号
            # self.inner_level_button.append(QtWidgets.QPushButton(self.central_widget))
            for j in range(0,NUM_LEVEL):
                self.inner_level_button[i].append(QtWidgets.QPushButton(self.central_widget))
                self.inner_level_button[i][j].setStyleSheet(self.level_button_style)
                #4*5的布局
                self.inner_level_button[i][j].setGeometry(
                    QtCore.QRect(self.inner_level_one_button_x[i]+40*(j%4), self.inner_level_one_button_y-40*(int(j/4)), 31, 31))
                self.inner_level_button[i][j].setObjectName(
                    inner_level_button_name + str(i) + "_" + ("0" if len(str(j))==1 else "")+str(j))
                #每个楼层按钮设置触发函数onInnerButtonClicked
                self.inner_level_button[i][j].clicked.connect(MainWindow.onInnerButtonClicked)



        for j in range(0,NUM_LEVEL):
            #添加外部每个楼层的上按钮:命名规则o_ubn_电梯编号
            self.outer_up_button.append(QtWidgets.QPushButton(self.central_widget))
            self.outer_up_button[j].setStyleSheet(self.outer_button_style)
            #2*10布局
            self.outer_up_button[j].setGeometry(
                  QtCore.QRect(self.outer_level_one_button_up_x[int(j / 10)], self.outer_level_one_button_up_y - 40 * (j % 10), 31, 31))
            self.outer_up_button[j].setObjectName(outer_up_button_name + str(j))

            #添加外部每个楼层的下按钮:命名规则o_dbn_电梯编号
            self.outer_down_button.append(QtWidgets.QPushButton(self.central_widget))
            self.outer_down_button[j].setStyleSheet(self.outer_button_style)
            #2*10布局
            self.outer_down_button[j].setGeometry(
                QtCore.QRect(self.outer_level_one_button_down_x[int(j / 10)], self.outer_level_one_button_down_y - 40 * (j % 10), 31, 31))
            self.outer_down_button[j].setObjectName(outer_down_button_name+str(j))
            
            #外部操作按钮设置触发函数onOuterButtonClicked
            self.outer_up_button[j].clicked.connect(MainWindow.onOuterButtonClicked)
            self.outer_down_button[j].clicked.connect(MainWindow.onOuterButtonClicked)

            #添加外部楼层文本:命名规则level_label电梯编号
            self.level_label.append(QtWidgets.QLabel(self.central_widget))
            self.level_label[j].setGeometry(QtCore.QRect(self.level_label_x[int(j / 10)],self.level_label_y - 40 * (j % 10), 66,31))
            self.level_label[j].setObjectName("level_label"+str(j))
            self.level_label[j].setStyleSheet(self.text_style)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        for i in range(0,NUM_ELEVATOR):
            self.inner_open_button[i].setText(_translate("MainWindow", "开"))
            self.inner_close_button[i].setText(_translate("MainWindow", "关"))
            self.inner_warn_button[i].setText(_translate("MainWindow", "✖"))
            self.repair_button[i].setText(_translate("MainWindow","fix"))

            for j in range(0,NUM_LEVEL):
                self.inner_level_button[i][j].setText(_translate("MainWindow",str(j+1)))
        
        for j in range(0,NUM_LEVEL):
            self.outer_up_button[j].setText(_translate("MainWindow","▲"))
            self.outer_down_button[j].setText(_translate("MainWindow","▼"))
            self.level_label[j].setText(_translate("MainWindow","Level "+("0" if j<9 else "")+str(j+1)))
        



    def printMessage(self,text_string):
        """[MainWindow将信息串输出到消息窗口textBrowser中]]

        Args:
            text_string ([str]): [需要打印的信息]
        """        
        self.textBrowser.append(text_string)
        self.cursor=self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)
        QtWidgets.QApplication.processEvents()



    #槽函数设置

    def onInnerButtonClicked(self):
        """[电梯内按钮点击的触发函数:包括开门，关门，警告，楼层按钮]
        """        
        object_name=self.sender().objectName()
        #序号serial number
        elevator_sn=int(object_name[6])
        #按钮性质
        clicked_content=object_name[2:5]
        
        if clicked_content=='lbn': #电梯内部的楼层按钮
            level_number=int(object_name[-2]+object_name[-1])+1
            #设置按钮长按
            self.printMessage("使用者在电梯"+str(elevator_sn+1)+"内部点击了"+str(level_number)+"楼按钮")
            self.inner_level_button[elevator_sn][level_number-1].setStyleSheet(self.level_long_pressed_style)
            self.inner_level_button[elevator_sn][level_number-1].setEnabled(False)
            #触发内调度
            self.dispatcher.innerDispatch(elevator_sn,level_number)
            

        elif clicked_content=="obn": #电梯内部的开门按钮
            self.printMessage("使用者在电梯"+str(elevator_sn+1)+"内部点击了开门按钮")
            #对应的响应函数
            self.dispatcher.responseOBN(elevator_sn)


        elif clicked_content=="cbn": #电梯内部的关门按钮
            self.printMessage("使用者在电梯"+str(elevator_sn+1)+"内部点击了关门按钮")
            self.dispatcher.responseCBN(elevator_sn)

        elif clicked_content=="wbn":  #电梯内部报警按钮           
            self.printMessage("OP:使用者在电梯"+str(elevator_sn+1)+"内部点击了报警按钮")
            #设置按钮长按
            self.inner_warn_button[elevator_sn].setStyleSheet(self.warn_long_pressed_style)
            self.inner_warn_button[elevator_sn].setEnabled(False)
            #对应的响应函数
            self.dispatcher.responseWBN(elevator_sn)


    def onOuterButtonClicked(self):
        """[外按钮点击触发函数：包括上楼，下楼按钮]
        """
        object_name=self.sender().objectName()
        #楼层索引，获取真实楼层时需+1
        level_index=int(object_name[6:])
        #按钮性质
        clicked_content=object_name[2:5]
        if clicked_content=="ubn": #电梯外部的上楼按钮
            self.printMessage("OP:使用者在电梯外部"+str(level_index+1)+"楼点击了上楼按钮")
            #设置按钮长按
            self.outer_up_button[level_index].setStyleSheet(self.outer_long_pressed_style)
            self.outer_up_button[level_index].setEnabled(False)
            #触发外调度
            self.dispatcher.outerDispatch(UP,level_index+1)
            
        
        elif clicked_content=="dbn": #电梯外部的下楼按钮
            self.printMessage("OP:使用者在电梯外部"+str(level_index+1)+"楼点击了下楼按钮")
            #设置按钮长按
            self.outer_down_button[level_index].setStyleSheet(self.outer_long_pressed_style)
            self.outer_down_button[level_index].setEnabled(False)
            #触发外调度
            self.dispatcher.outerDispatch(DOWN,level_index+1)
    
    def onRepairButtonClicked(self):
        """[修理按钮的触发器]
        """        
        object_name=self.sender().objectName()
        elevator_sn=int(object_name[6])
        #修理电梯，恢复电梯运行
        self.dispatcher.responseRBN(elevator_sn)



    #开门动画
    def open_animation_start(self,elevator_sn):
        """[对指定电梯执行开门动作时播放开门动画]

        Args:
            elevator_sn ([int]): [要执行开门动画的电梯序号]
        """     
        #如果当前没有开门动画执行时播放，如果有开门动画则无需重复播放gif   
        if self.dispatcher.elevator_list[elevator_sn].has_open_animation==False:
            self.dispatcher.elevator_list[elevator_sn].has_close_animation=False
            self.close_gif_label[elevator_sn].setVisible(False)
            self.elevator_open_image[elevator_sn].setVisible(False)
            self.elevator_close_image[elevator_sn].setVisible(False)
            self.open_gif_label[elevator_sn].movie().jumpToFrame(0)
            self.open_gif_label[elevator_sn].movie().start()
            self.open_gif_label[elevator_sn].show()
            self.dispatcher.elevator_list[elevator_sn].has_open_animation=True

        thread_op=threading.Timer(0.7,self.open_animation_end,(elevator_sn,))
        thread_op.start()

    def open_animation_end(self,elevator_sn):
        """[依赖开门动画函数，0.7秒后结束动画]

        Args:
            elevator_sn ([int]): [要执行开门动画的电梯序号]
        """        
        self.open_gif_label[elevator_sn].movie().setPaused(True)
        self.open_gif_label[elevator_sn].setVisible(False)
        self.elevator_open_image[elevator_sn].setVisible(True)
        self.elevator_close_image[elevator_sn].setVisible(False)    
        #设置开门等待时间
        self.dispatcher.elevator_list[elevator_sn].state_time=STANDBY_TIME


    def close_animation_start(self,elevator_sn):
        """[对指定电梯执行关门动作时播放开门动画]

        Args:
            elevator_sn ([int]): [电梯索引]
        """     
        #如果当前无关门动画执行才播放，如果有关门动画则无需重复播放gif   
        if self.dispatcher.elevator_list[elevator_sn].has_close_animation==False:
            self.dispatcher.elevator_list[elevator_sn].has_open_animation=False
            self.elevator_open_image[elevator_sn].setVisible(False)
            self.elevator_close_image[elevator_sn].setVisible(False)
            self.close_gif_label[elevator_sn].movie().jumpToFrame(0)
            self.close_gif_label[elevator_sn].movie().start()
            self.close_gif_label[elevator_sn].show()
            self.open_gif_label[elevator_sn].setVisible(False)
            self.dispatcher.elevator_list[elevator_sn].has_close_animation=True

        thread_op=threading.Timer(0.7,self.close_animation_end,(elevator_sn,))
        thread_op.start()

    def close_animation_end(self,elevator_sn):
        """[依赖关门动画函数，0.7秒后结束动画]

        Args:
            elevator_sn ([int]): [电梯索引]
        """        
        self.close_gif_label[elevator_sn].movie().setPaused(True)
        self.close_gif_label[elevator_sn].setVisible(False)
        #如果在关门的过程中又开了门，则开门动画覆盖关门动画，此时无需重写状态时间
        if self.dispatcher.elevator_list[elevator_sn].has_open_animation==False:
            self.elevator_close_image[elevator_sn].setVisible(True)
            self.elevator_open_image[elevator_sn].setVisible(False) 
            self.dispatcher.elevator_list[elevator_sn].state_time=0  
        

    def up_down_animation_show(self,order,elevator_sn):
        """[对指定电梯上下指示图标动画的播放，停止时不播放]]

        Args:
            order ([int]): [向上命令或向下命令]
            elevator_sn ([int]): [电梯的索引]
        """        
        if order==GOING_UP:
            self.up_gif_label[elevator_sn].setVisible(True)
            self.down_gif_label[elevator_sn].setVisible(False)
        elif order==GOING_DOWN:
            self.down_gif_label[elevator_sn].setVisible(True)
            self.up_gif_label[elevator_sn].setVisible(False)
        else:
            self.up_gif_label[elevator_sn].setVisible(False)
            self.down_gif_label[elevator_sn].setVisible(False)


    








