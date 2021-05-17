

#################################################常量区###################################################

#电梯数量
NUM_ELEVATOR=5

#楼层数量
NUM_LEVEL=20

#电梯门状态
DOOR_OPEN=0
DOOR_CLOSE=1

#电梯运行状态
GOING_UP=1
GOING_DOWN=2
STANDBY=3
DEAD=4

#停顿时间
STANDBY_TIME=4

#内部按钮大小:
INNER_X=31
INNER_Y=31

#更新时间
UPDATE_GAP=1

#电梯外部按钮
UP=1
DOWN=2
INNER=3

#定义无穷大:
INF=50

##################################################电梯类##################################################
class Elevator(object):
    """[电梯类]
    """    
    def __init__(self):
        self.state=STANDBY
        self.level=1
        self.state_time=0
        self.has_open_animation=False
        self.has_close_animation=False
        self.curr_button=INNER
        
        self.by_task=[]
        self.oppo_task=[]

    #设置状态    
    def setState(self,elestate:int):
        self.state=elestate
    #设置楼层
    def setLevel(self,target_level:int):
        self.level=target_level
    #将对应楼层加入任务队列
    def addByTask(self,target_level:int):
        self.by_task.append(target_level)
    #将对应楼层加入第二队列
    def addOppoTask(self,target_level:int):
        self.oppo_task.append(target_level)
    #任务队列排序
    def arrangeByTask(self):
        if self.state==GOING_UP:
            self.by_task.sort(key=lambda x:x[0])
        elif self.state==GOING_DOWN:
            self.by_task.sort(key=lambda x:x[0])
            self.by_task.reverse()
        else:
            pass    
    #第二任务队列排序
    def arrangeOppoTask(self):
        if self.state==GOING_UP:
            self.oppo_task.sort(key=lambda x:x[0])
            self.oppo_task.reverse()
        elif self.state==GOING_DOWN:
            self.oppo_task.sort(key=lambda x:x[0])
        else:
            pass
    #关闭开门动画
    def endOpenAniState(self):
        self.has_open_animation=False
    #关闭关门动画
    def endCloseAniState(self):
        self.has_close_animation=False
    #获取任务队列首个任务的楼层
    def getFirstByTask(self):
        return self.by_task[0][0]
    
    def setDead(self):
        self.state=DEAD
        self.state_time=0
        self.has_open_animation=False
        self.has_close_animation=False


    #损坏电梯的修复
    def recover(self):
        self.state=STANDBY
        self.state_time=0
        self.has_open_animation=False
        self.has_close_animation=False
        self.by_task.clear()
        self.oppo_task.clear()
        self.curr_button=INNER


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

#对Qt组件的命名，便于列表切片获取信息
open_img_name="i_eoi_"
close_img_name="i_eci_"
mark_img_name="i_emi_"
open_gif_name="i_ogl_"
close_gif_name="i_cgl_"
up_gif_name="i_ugl_"
down_gif_name="i_dgl_"
elevator_lcd_name="i_lcd_"
inner_open_button_name="i_obn_"
inner_close_button_name="i_cbn_"
inner_warn_button_name="i_wbn_"
inner_level_button_name="i_lbn_"
outer_up_button_name="o_ubn_"
outer_down_button_name="o_dbn_"
repair_button_name="o_rbn_"

