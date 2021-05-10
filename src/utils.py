

#################################################常量区###################################################

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
GOING_UP=2
GOING_DOWN=3
STANDBY=4
DEAD=5

#停顿时间
STANDBY_TIME=4

#内部按钮大小:
INNER_X=31
INNER_Y=31

#更新时间
UPDATE_GAP=1

#电梯外部按钮命令
UP=1
DOWN=2

#定义无穷大:
INF=50



class Elevator(object):
    def __init__(self):
        self.door=DOOR_CLOSE
        self.state=STANDBY
        self.level=1
        self.state_time=0

        
        self.by_task=[]
        self.oppo_task=[]
    
    def setDoor(self,doorstate:int):
        self.door=doorstate
    
    def setState(self,elestate:int):
        self.state=elestate

    def setLevel(self,target_level:int):
        self.level=target_level
    
    def addByTask(self,target_level:int):
        self.by_task.append(target_level)
    
    def addOppoTask(self,target_level:int):
        self.oppo_task.append(target_level)

    def arrangeByTask(self):
        if self.state==GOING_UP:
            self.by_task.sort()
        elif self.state==GOING_DOWN:
            self.by_task.sort()
            self.by_task.reverse()
        else:
            pass    
    def arrangeOppoTask(self):
        if self.state==GOING_UP:
            self.oppo_task.sort()
            self.oppo_task.reverse()
        elif self.state==GOING_DOWN:
            self.oppo_task.sort()
        else:
            pass
    

    def getFirstByTask(self)->int:
        return self.by_task[0]



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

