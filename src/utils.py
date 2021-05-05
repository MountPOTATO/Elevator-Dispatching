'''
Author: your name
Date: 2021-04-28 12:58:29
LastEditTime: 2021-05-04 11:27:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Elevator-Dispatching\src\utils.py
'''

################################################常量区###################################################

#电梯数量
NUM_ELEVATOR=5

#楼层数量
NUM_LEVEL=20

#电梯门状态
DOOR_OPEN=0
DOOR_CLOSE=1

#电梯运行状态
OPEN_STANDBY=0
CLOSE_STANDBY=1
GO_UP=2
GO_DOWN=3
DEAD=4

#用户运动状态
USER_UPSTAIR=1
USER_DOWNSTAIR=2

#内部按钮大小:
INNER_X=31
INNER_Y=31

#更新时间
UPDATE_GAP=1

class State(object):
    def __init__(self,num):
        
        self.door=num*[DOOR_CLOSE]
        self.elevator=num*[CLOSE_STANDBY]
        self.level=num*[1]
        self.time=num*[0]
    
    
    def setElevator(i,state:int):
        self.elevator[i]=state
    
    def setDoor(i,state:int):
        self.door[i]=state
    
    def setLevel(i,state:int):
        self.level[i]=state
    

##############################################工具######################################################
class QSS_READER:
    def __init__(self):
        pass

    def read(style):
        """[读入qss文件并以str形式存储]

        Args:
            style ([str]): [qss文件的相对路径地址]

        Returns:
            [str]: [qss文件的str形式，以在setStyleSheet中调用]
        """        
        with open(style,'r') as f:
            return f.read()

###########################################组件命名#####################################################

open_img_name="i_eoi_"
close_img_name="i_eci_"
open_gif_name="i_ogl_"
close_gif_name="i_cgl_"
elevator_lcd_name="i_lcd_"
inner_open_button_name="i_obn_"
inner_close_button_name="i_cbn_"
inner_warn_button_name="i_wbn_"
inner_level_button_name="i_lbn_"
outer_up_button_name="o_ubn_"
outer_down_button_name="o_dbn_"

