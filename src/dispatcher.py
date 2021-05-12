'''
Author: mount_potato
Date: 2021-04-29 00:31:57
LastEditTime: 2021-05-12 16:48:44
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Elevator-Dispatching\dispatcher.py
'''

from PyQt5.QtCore import *
from elevator_ui import *
from utils import *


class Dispatcher(object):
    def __init__(self,main_window):
        #主窗口
        self.main_window=main_window

        #utils中的电梯类列表
        self.elevator_list=[]
        for i in range(0,NUM_ELEVATOR):
            self.elevator_list.append(Elevator())

        #计时器，间隔时间1000*UPDATE_GAP更新，此处设为1秒
        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000*UPDATE_GAP)

    #################################################对非核心调度按钮的响应#######################################
    def responseOBN(self,elevator_sn):
        """[对指定电梯按下开门按钮的响应]

        Args:
            elevator_sn ([int]): [电梯索引]
        """      
        
        if self.elevator_list[elevator_sn].state==STANDBY:
            #对停止的电梯，播放开门动画并设定开门等待时间
            self.main_window.open_animation_start(elevator_sn)
            self.elevator_list[elevator_sn].state_time=STANDBY_TIME
        elif self.elevator_list[elevator_sn].state==DEAD:
            #对故障电梯，提示无法开门
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已故障，开门命令无效")       
        else:
            #对运行中电梯，提示无法开门
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯运行中，开门命令无效")
    
    def responseCBN(self,elevator_sn):
        """[对指定电梯按下关门按钮的响应]

        Args:
            elevator_sn ([int]): [电梯索引]
        """        
        
        if self.elevator_list[elevator_sn].state==STANDBY and self.elevator_list[elevator_sn].state_time>=1:
            #对还处于开门等待状态的电梯提前关门，关门时间1秒
            self.elevator_list[elevator_sn].state_time=1
            self.main_window.close_animation_start(elevator_sn)
        elif self.elevator_list[elevator_sn].state==DEAD:
            #对故障电梯提示无法开门
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已故障，关门命令无效") 
        elif self.elevator_list[elevator_sn].state==GOING_DOWN or self.elevator_list[elevator_sn].state==GOING_UP:
            #对运行中电梯提示无法开门
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯运行中，关门命令无效")
        else:
            pass
            
    def responseWBN(self,elevator_sn):
        """[对指定电梯点击故障按钮的响应]

        Args:
            elevator_sn ([int]): [电梯索引]
        """        
        by_task_len=len(self.elevator_list[elevator_sn].by_task)
        oppo_task_len=len(self.elevator_list[elevator_sn].oppo_task)
        if self.elevator_list[elevator_sn].state==STANDBY and by_task_len==0 and oppo_task_len==0 :
            #可以被报警的电梯：无任务执行，处于停止状态
            self.elevator_list[elevator_sn].state=DEAD
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯报告损坏，已停用")

            #电梯内所有的楼层按钮停用
            for level_button in self.main_window.inner_level_button[elevator_sn]:
                level_button.setStyleSheet(self.main_window.warn_long_pressed_style)
                level_button.setEnabled(False)

            #检查一遍所有电梯的状态
            all_down=True
            for elevator in self.elevator_list:
                if elevator.state!=DEAD:
                    all_down=False
            if all_down==True:
                self.main_window.printMessage("所有电梯全部停用")
                #所有电梯全部停用时，停用全部电梯外部上下楼按钮
                for up_button in self.main_window.outer_up_button:
                    up_button.setStyleSheet(self.main_window.outer_long_pressed_style)
                    up_button.setEnabled(False)
                for down_button in self.main_window.outer_down_button:
                    down_button.setStyleSheet(self.main_window.outer_long_pressed_style)
                    down_button.setEnabled(False)

        elif self.elevator_list[elevator_sn].state==DEAD:
            #对已经处于报警状态的电梯，提示无需重复报警，恢复按钮状态
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已报告损坏，无需重复报警")
            self.main_window.inner_warn_button[elevator_sn].setStyleSheet(self.main_window.warn_button_style)
            self.main_window.inner_warn_button[elevator_sn].setEnabled(True)
        else:
            #对在运行的电梯，提示报警无效，恢复按钮状态
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯仍运行中，报警无效")
            self.main_window.inner_warn_button[elevator_sn].setStyleSheet(self.main_window.warn_button_style)
            self.main_window.inner_warn_button[elevator_sn].setEnabled(True)
        
    def responseRBN(self,elevator_sn):
        """[对指定电梯点击修理按钮的响应]

        Args:
            elevator_sn ([int]): [电梯索引]
        """        
        if self.elevator_list[elevator_sn].state!=DEAD:
            #正常电梯无需修理
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯运行正常，无需修理")
        else:
            #恢复电梯运行状态
            self.elevator_list[elevator_sn].recover()
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯成功修复，恢复运行")
            #警告按钮恢复
            self.main_window.inner_warn_button[elevator_sn].setStyleSheet(self.main_window.warn_button_style)
            self.main_window.inner_warn_button[elevator_sn].setEnabled(True)
            #楼层按钮恢复
            for level_button in self.main_window.inner_level_button[elevator_sn]:
                level_button.setStyleSheet(self.main_window.level_button_style)
                level_button.setEnabled(True)       
            #有一个电梯能运行，就可以将外部上下楼按钮恢复
            for up_button in self.main_window.outer_up_button:
                up_button.setStyleSheet(self.main_window.outer_button_style)
                up_button.setEnabled(True)
            for down_button in self.main_window.outer_down_button:
                down_button.setStyleSheet(self.main_window.outer_button_style)
                down_button.setEnabled(True)



    ################################################内外调度的方法#####################################################
    def innerDispatch(self,elevator_sn,target_level):
        """[指定电梯楼层按钮的内调度]

        Args:
            elevator_sn ([int]): [电梯索引]
            target_level ([int]): [点击按钮的目标楼层]
        """        
        current_state=self.elevator_list[elevator_sn].state
        curr_level=self.elevator_list[elevator_sn].level
        if current_state==DEAD:
            #报警电梯无法使用
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已损坏，操作无效")
        elif current_state==STANDBY:
            if target_level==curr_level:
                #如果已到达，此时恢复楼层按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)
                #开门动画播放与状态更新
                self.main_window.open_animation_start(elevator_sn)
                self.elevator_list[elevator_sn].state_time=STANDBY_TIME
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")
            else:
                #添加到电梯任务队列中，并根据电梯运行状态进行任务s排序
                self.elevator_list[elevator_sn].addByTask([target_level,INNER])
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
                
            
        elif current_state==GOING_UP:
            if target_level==curr_level:
                #如果已到达，此时恢复楼层按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)

                self.main_window.open_animation_start(elevator_sn)
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")
            elif target_level>curr_level:
                #加入任务队列
                self.elevator_list[elevator_sn].addByTask([target_level,INNER])
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
            else: #target_level<curr_level
                #加入第二任务队列
                self.elevator_list[elevator_sn].addOppoTask([target_level,INNER])
                self.elevator_list[elevator_sn].arrangeOppoTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
        
        elif current_state==GOING_DOWN:
            if target_level==curr_level:
                #如果已到达，此时恢复楼层按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)

                self.main_window.open_animation_start(elevator_sn)   
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")  
            elif target_level<curr_level:
                #加入任务队列
                self.elevator_list[elevator_sn].addByTask((target_level,INNER))
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
            else: #target_level>curr_level
                #加入反s任务队列
                self.elevator_list[elevator_sn].addOppoTask((target_level,INNER))
                self.elevator_list[elevator_sn].arrangeOppoTask() 
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往") 
        else:
            pass
            


    def outerDispatch(self,order,level):
        """[外部楼层上下楼按钮的外调度]

        Args:
            order ([int]): [上下楼按钮的命令，区分按钮性质]
            level ([type]): [所点击的楼层s]
        """        
        distance=NUM_ELEVATOR*[INF]

        #计算五部电梯离指定楼层的距离:方法为楼层距离*更新间隔+状态时间（目的是考虑开门电梯等待的间隔时间）
        for i in range(0,NUM_ELEVATOR):
            #对所有可用的电梯
            if self.elevator_list[i].state!=DEAD:
                #对上行电梯
                if self.elevator_list[i].state==GOING_UP and order==UP and level>self.elevator_list[i].level:
                    distance[i]=(level-self.elevator_list[i].level)*UPDATE_GAP
                #对下行电梯
                elif self.elevator_list[i].state==GOING_DOWN and order==DOWN and level<self.elevator_list[i].level:
                    distance[i]=(self.elevator_list[i].level-level)*UPDATE_GAP
                #对静止电梯
                elif self.elevator_list[i].state==STANDBY:
                    distance[i]=UPDATE_GAP*(abs(level-self.elevator_list[i].level))+self.elevator_list[i].state_time

        #获得最优调度的电梯序号0-4
        i=distance.index(min(distance))
        #无可用电梯
        if self.elevator_list[i].state==DEAD:
            self.main_window.printMessage("抱歉，当前无可用电梯")
            #恢复按钮
            if order==UP:
                self.main_window.outer_up_button[level-1].setStyleSheet(self.main_window.outer_button_style)
                self.main_window.outer_up_button[level-1].setEnabled(True)
            if order==DOWN:
                self.main_window.outer_down_button[level-1].setStyleSheet(self.main_window.outer_button_style)
                self.main_window.outer_down_button[level-1].setEnabled(True)

        self.main_window.printMessage("电梯"+str(i+1)+"号离当前用户最近，正在前往")
        if distance[i]==0:
            #电梯已到达，开门并恢复按钮
            self.main_window.outer_up_button[level-1].setStyleSheet(self.main_window.outer_button_style)
            self.main_window.outer_down_button[level-1].setStyleSheet(self.main_window.outer_button_style)
            self.main_window.outer_up_button[level-1].setEnabled(True)
            self.main_window.outer_down_button[level-1].setEnabled(True)
            #播放动画设置开门状态
            self.main_window.open_animation_start(i)
            self.elevator_list[i].state_time=STANDBY_TIME
            
        else:
            #未到达，最优电梯加入任务队列，任务队列内容包括(楼层，对应的外调度按钮(为了后续按钮状态恢复))
            self.elevator_list[i].addByTask([level,order])
            self.elevator_list[i].curr_button=UP if order==UP else DOWN
            
            

    ####################################################刷新方法###############################################
    def update(self):
        """[每隔UPDATE_GAP对所有电梯的状态进行更新]
        """        
        for i,elevator in enumerate(self.elevator_list):
            #电梯上下楼标识动画播放
            self.main_window.up_down_animation_show(elevator.state,i)

            #电梯静止时的状态更新
            if elevator.state==STANDBY and elevator.state_time!=0:
                #开门等待状态只剩1s时开始关门
                if elevator.state_time==1:
                    self.main_window.close_animation_start(i)
                #静止状态下，对状态时间计时
                elevator.state_time-=1
                continue    
            
            if elevator.state==STANDBY and elevator.state_time==0:
                #电梯停止且无开门关门动作时，设置动画停止
                elevator.has_close_animation=False
                elevator.has_open_animation=False

            #对含有任务的电梯进行状态更新
            if len(elevator.by_task)!=0:
                if elevator.state==STANDBY and elevator.state_time==0:
                    #根据首任务楼层判断是上楼还是下楼
                    if elevator.level<elevator.getFirstByTask():
                        elevator.setState(GOING_UP)
                    else:
                        elevator.setState(GOING_DOWN)
                else:
                    #运行时，每次更新下变更一个楼层
                    target_level=elevator.getFirstByTask()
                    if elevator.level<target_level:
                        elevator.setState(GOING_UP)                        
                        elevator.level+=1
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                    elif elevator.level>target_level:
                        elevator.setState(GOING_DOWN)                        
                        elevator.level-=1
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                    
                    else:#电梯到达
                        #对队列任务中对应按钮进行恢复
                        if elevator.by_task[0][1]==UP:
                            elevator.curr_button=INNER
                            self.main_window.outer_up_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_up_button[elevator.level-1].setEnabled(True)
                        elif elevator.by_task[0][1]==DOWN:
                            elevator.curr_button=INNER
                            self.main_window.outer_down_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_down_button[elevator.level-1].setEnabled(True)
                        else:
                            self.main_window.outer_up_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_up_button[elevator.level-1].setEnabled(True)       
                            self.main_window.outer_down_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_down_button[elevator.level-1].setEnabled(True)                                                 
                        self.main_window.inner_level_button[i][target_level-1].setStyleSheet(self.main_window.level_button_style)
                        self.main_window.inner_level_button[i][target_level-1].setEnabled(True)                           
                        self.main_window.open_animation_start(i)
                        #电梯状态设为停止
                        elevator.setState(STANDBY)
                        elevator.state_time=STANDBY_TIME
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                        elevator.by_task.pop(0)
                        
            elif elevator.oppo_task:
                #电梯执行完任务队列中的任务时，将第二队列中任务迁移到任务队列中
                elevator.by_task=elevator.oppo_task.copy()
                elevator.oppo_task.clear()
            else:
                pass
        
        

                
