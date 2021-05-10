'''
Author: mount_potato
Date: 2021-04-29 00:31:57
LastEditTime: 2021-05-10 19:50:50
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
        pass
    

    def innerDispatch(self,elevator_sn,target_level):
        current_state=self.elevator_list[elevator_sn].state
        curr_level=self.elevator_list[elevator_sn].level
        if current_state==DEAD:
            self.main_window.printMessage(str(elevator_sn+1)+"号电梯已损坏，操作无效")
        elif current_state==STANDBY:
            if target_level==curr_level:
                self.elevator_list[elevator_sn].setDoor(DOOR_OPEN)
                self.main_window.open_animation_start(elevator_sn)
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯已经到达")
            else:
                self.elevator_list[elevator_sn].addByTask(target_level)
                self.elevator_list[elevator_sn].arrangeByTask()
                self.main_window.printMessage(str(elevator_sn+1)+"号电梯正在前往")
                print(self.elevator_list[elevator_sn].by_task)
            
        elif current_state==GOING_UP:
            if target_level==curr_level:
                self.elevator_list[elevator_sn].setDoor(DOOR_OPEN)
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
                self.elevator_list[elevator_sn].setDoor(DOOR_OPEN)
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
            self.door=DOOR_OPEN
            self.main_window.open_animation_start(i)
            #TODO:按钮美化
        else:
            self.elevator_list[i].addByTask(level)
            #TODO:按钮美化
            print("test")


    def update(self):
        for i,elevator in enumerate(self.elevator_list):
            #电梯上下楼标识动画
            self.main_window.up_down_animation_show(elevator.state,i)

            #电梯静止时的状态更新
            if elevator.state==STANDBY and elevator.state_time!=0:
                elevator.state_time-=1
                if elevator.state_time==1:
                    self.main_window.close_animation_start(i)
                continue    
            
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
                        #TODO:按钮设置
                        elevator.level+=1
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                    elif elevator.level>target_level:
                        elevator.setState(GOING_DOWN)
                        #TODO:按钮设置
                        elevator.level-=1
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                    
                    else:#电梯到达
                        self.main_window.open_animation_start(i)
                        elevator.setState(STANDBY)
                        elevator.state_time=4
                        self.main_window.elevator_lcd[i].setProperty("value",elevator.level)
                        elevator.by_task.pop(0)
                        #TODO:按钮设置
            elif elevator.oppo_task:
                elevator.by_task=elevator.oppo_task.copy()
                elevator.oppo_task.clear()
            else:
                pass
        
        #TODO:报警按钮

                
