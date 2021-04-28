'''
Author: mount_potato
Date: 2021-04-26 16:13:46
LastEditTime: 2021-04-28 12:58:06
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \os_elevator\const.py
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
STANDBY=0
GO_UP=1
GO_DOWN=2

#用户运动状态
USER_UPSTAIR=1
USER_DOWNSTAIR=2

#内部按钮大小:
INNER_X=31
INNER_Y=31

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