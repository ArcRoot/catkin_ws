#!/usr/bin/env python
#-- coding:utf-8 --
####################################################################
# 프로그램이름 : parking.py
# 코드작성팀명 : 슈퍼카
####################################################################

#=============================================
# 함께 사용되는 각종 파이썬 패키지들의 import 선언부
#=============================================
import pygame
import numpy as np
import math
import rospy
from xycar_msgs.msg import xycar_motor

#=============================================
# 모터 토픽을 발행할 것임을 선언
#============================================= 
motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
xycar_msg = xycar_motor()

#=============================================
# 프로그램에서 사용할 변수, 저장공간 선언부
#============================================= 
rx, ry = [], []

#=============================================
# 프로그램에서 사용할 상수 선언부
#=============================================
AR = (1142, 62) # AR 태그의 위치
P_ENTRY = (1036, 162) # 주차라인 진입 시점의 좌표
P_END = (1129, 69) # 주차라인 끝의 좌표

#=============================================
# 모터 토픽을 발행하는 함수
# 입력으로 받은 angle과 speed 값을
# 모터 토픽에 옮겨 담은 후에 토픽을 발행함.
#=============================================
def drive(angle, speed):
    xycar_msg.angle = int(angle)
    xycar_msg.speed = int(speed)
    motor_pub.publish(xycar_msg)

#=============================================
# 경로를 생성하는 함수
# 차량의 시작위치 sx, sy, 시작각도 syaw
# 최대가속도 max_acceleration, 단위시간 dt 를 전달받고
# 경로를 리스트를 생성하여 반환한다.
#=============================================
def planning(sx, sy, syaw, max_acceleration, dt):
    global rx, ry
    rx=[]
    ry=[]
    #car head x, y
    hx=sx+70*math.cos(syaw*math.pi/180+math.pi/2)
    hy=sy+70*math.sin(syaw*math.pi/180+math.pi/2)

    print("Start Planning")

    rx.insert(0,P_ENTRY[0])
    ry.insert(0,P_ENTRY[1])
    print(math.pi)
    rx.insert(1,hx)
    ry.insert(1,hy)

    #=================================================
    #차가 주차공간으로 들어갈 때 유지해야할 각도 dest_yaw
    #planning에 사용할 각도 path_yaw
    #=================================================
    dest_yaw=math.atan((P_ENTRY[0]-P_END[0])/(P_ENTRY[1]-P_END[1]))
    path_yaw=math.atan((hx-rx[0])/(hy-ry[0]))

    #initial path of parking section
    for i in range(0,70):
        rx.insert(0,P_END[0]-200*i*dt*math.cos(dest_yaw))
        ry.insert(0,P_END[1]-200*i*dt*math.sin(dest_yaw))
        print(rx[0]," : ",ry[0])


    print(path_yaw)
    for i in range(0, 550):
        rx.insert(0,rx[0]-dt*100*math.cos(path_yaw))
        ry.insert(0,ry[0]-dt*100*math.sin(path_yaw))
        path_yaw=math.atan((hy-ry[0])/(hx-rx[0]))
        print(rx[0]," : ",ry[0])
        #if (math.sqrt(rx[0]-hx)<(100*dt)):
            #if (math.sqrt(ry[0]-hy)<(100*dt)):
                #break

    return rx, ry

#=============================================
# 생성된 경로를 따라가는 함수
# 파이게임 screen, 현재위치 x,y 현재각도, yaw
# 현재속도 velocity, 최대가속도 max_acceleration 단위시간 dt 를 전달받고
# 각도와 속도를 결정하여 주행한다.
#=============================================
def tracking(screen, x, y, yaw, velocity, max_acceleration, dt):
    global rx, ry
    angle = 50 # -50 ~ 50
    speed = 50 # -50 ~ 50
    
    drive(angle, speed)
