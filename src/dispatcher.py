'''
Author: mount_potato
Date: 2021-04-29 00:31:57
LastEditTime: 2021-05-11 11:08:31
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

        self.elevator_list=[]
        for i in range(0,NUM_ELEVATOR):
            self.elevator_list.append(Elevator())

        self.timer=QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    
    def responseOBN(self,elevator_sn):
        if self.elevator_list[elevator_sn].state==STANDBY:
            self.main_window.open_animation_start(elevator_sn)
            self.elevator_list[elevator_sn].state_time=STANDBY_TIME
        elif self.elevator_list[elevator_sn].state==DEAD:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已故障，开门命令无效")       
        else:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯运行中，开门命令无效")
    
    def responseCBN(self,elevator_sn):
        if self.elevator_list[elevator_sn].state==STANDBY and self.elevator_list[elevator_sn].state_time>=1:
            self.elevator_list[elevator_sn].state_time=1
            self.main_window.close_animation_start(elevator_sn)
        elif self.elevator_list[elevator_sn].state==DEAD:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已故障，关门命令无效") 
        elif self.elevator_list[elevator_sn].state==GOING_DOWN or self.elevator_list[elevator_sn].state==GOING_UP:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯运行中，关门命令无效")
            
    def responseWBN(self,elevator_sn):
        by_task_len=len(self.elevator_list[elevator_sn].by_task)
        oppo_task_len=len(self.elevator_list[elevator_sn].oppo_task)
        if self.elevator_list[elevator_sn].state==STANDBY and by_task_len==0 and oppo_task_len==0 :
            self.elevator_list[elevator_sn].state=DEAD
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯报告损坏，已停用")

            

            for level_button in self.main_window.inner_level_button[elevator_sn]:
                level_button.setStyleSheet(self.main_window.warn_long_pressed_style)
                level_button.setEnabled(False)

            all_down=True
            for elevator in self.elevator_list:
                if elevator.state!=DEAD:
                    all_down=False
            if all_down==True:
                self.main_window.printMessage("所有电梯全部停用")
                #停用全部外调度按钮
                for up_button in self.main_window.outer_up_button:
                    up_button.setStyleSheet(self.main_window.outer_long_pressed_style)
                    up_button.setEnabled(False)
                for down_button in self.main_window.outer_down_button:
                    down_button.setStyleSheet(self.main_window.outer_long_pressed_style)
                    down_button.setEnabled(False)

        elif self.elevator_list[elevator_sn].state==DEAD:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已报告损坏，无需重复报警")
            self.main_window.inner_warn_button[elevator_sn].setStyleSheet(self.main_window.warn_button_style)
            self.main_window.inner_warn_button[elevator_sn].setEnabled(True)
        else:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯仍运行中，报警无效")
            self.main_window.inner_warn_button[elevator_sn].setStyleSheet(self.main_window.warn_button_style)
            self.main_window.inner_warn_button[elevator_sn].setEnabled(True)
        




    def innerDispatch(self,elevator_sn,target_level):
        current_state=self.elevator_list[elevator_sn].state
        curr_level=self.elevator_list[elevator_sn].level
        if current_state==DEAD:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已损坏，操作无效")
        elif current_state==STANDBY:
            if target_level==curr_level:
                #恢复按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)
                
                self.main_window.open_animation_start(elevator_sn)
                self.elevator_list[elevator_sn].state_time=STANDBY_TIME
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")
            else:
                self.elevator_list[elevator_sn].addByTask(target_level)
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
                print(self.elevator_list[elevator_sn].by_task)
            
        elif current_state==GOING_UP:
            if target_level==curr_level:
                #恢复按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)

                self.main_window.open_animation_start(elevator_sn)
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")
            elif target_level>curr_level:
                self.elevator_list[elevator_sn].addByTask(target_level)
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
            else: #target_level<curr_level
                self.elevator_list[elevator_sn].addOppoTask(target_level)
                self.elevator_list[elevator_sn].arrangeOppoTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
        
        elif current_state==GOING_DOWN:
            if target_level==curr_level:
                #恢复按钮
                self.main_window.inner_level_button[elevator_sn][target_level-1].setStyleSheet(self.main_window.level_button_style)
                self.main_window.inner_level_button[elevator_sn][target_level-1].setEnabled(True)

                self.main_window.open_animation_start(elevator_sn)   
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")  
            elif target_level<curr_level:
                self.elevator_list[elevator_sn].addByTask(target_level)
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
            else: #target_level>curr_level
                self.elevator_list[elevator_sn].addOppoTask(target_level)
                self.elevator_list[elevator_sn].arrangeOppoTask() 
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往") 
        else:
            pass
            


    def outerDispatch(self,order,level):

        distance=NUM_ELEVATOR*[INF]



        for i in range(0,NUM_ELEVATOR):
            #对所有可用的电梯
            if self.elevator_list[i].state!=DEAD:
                #对上行电梯
                if self.elevator_list[i].state==GOING_UP and order==UP and level>self.elevator_list[i].level:
                    distance[i]=level-self.elevator_list[i].level
                #对下行电梯
                elif self.elevator_list[i].state==GOING_UP and order==UP and level>self.elevator_list[i].level:
                    distance[i]=level-self.elevator_list[i].level
                #对静止电梯
                elif self.elevator_list[i].state==STANDBY:
                    distance[i]=abs(level-self.elevator_list[i].level)

        #获得最优调度的电梯序号0-4
        i=distance.index(min(distance))
        self.main_window.printMessage("电梯"+str(i+1)+"号离当前用户最近，正在前往")
        if distance[i]==0:
            self.main_window.outer_up_button[level-1].setStyleSheet(self.main_window.outer_button_style)
            self.main_window.outer_down_button[level-1].setStyleSheet(self.main_window.outer_button_style)
            self.main_window.outer_up_button[level-1].setEnabled(True)
            self.main_window.outer_down_button[level-1].setEnabled(True)

            self.main_window.open_animation_start(i)
            self.elevator_list[i].state_time=STANDBY_TIME
            #TODO:按钮美化
        else:
            self.elevator_list[i].addByTask(level)
            #TODO:按钮美化
            


    def update(self):
        for i,elevator in enumerate(self.elevator_list):
            #电梯上下楼标识动画
            self.main_window.up_down_animation_show(elevator.state,i)

            #电梯静止时的状态更新
            if elevator.state==STANDBY and elevator.state_time!=0:
                if elevator.state_time==1:
                    self.main_window.close_animation_start(i)
                elevator.state_time-=1
                continue    
            
            if elevator.state==STANDBY and elevator.state_time==0:
                elevator.has_close_animation=False
                elevator.has_open_animation=False

            #对含有任务的电梯进行状态更新
            if len(elevator.by_task)!=0:
                if elevator.state==STANDBY and elevator.state_time==0:
                        if elevator.level<elevator.getFirstByTask():
                            elevator.setState(GOING_UP)
                        else:
                            elevator.setState(GOING_DOWN)
                else:
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
                        #恢复按钮
                        if elevator.state==GOING_UP:
                            self.main_window.outer_up_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_up_button[elevator.level-1].setEnabled(True)
                        if elevator.state==GOING_DOWN:
                            self.main_window.outer_down_button[elevator.level-1].setStyleSheet(self.main_window.outer_button_style)
                            self.main_window.outer_down_button[elevator.level-1].setEnabled(True)
                        self.main_window.inner_level_button[i][target_level-1].setStyleSheet(self.main_window.level_button_style)
                        self.main_window.inner_level_button[i][target_level-1].setEnabled(True)                           
                        self.main_window.open_animation_start(i)
                        elevator.setState(STANDBY)
                        elevator.state_time=STANDBY_TIME
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                        elevator.by_task.pop(0)
                        #TODO:按钮设置
            elif elevator.oppo_task:
                elevator.by_task=elevator.oppo_task.copy()
                elevator.oppo_task.clear()
            else:
                pass
        
        #TODO:报警按钮

                
