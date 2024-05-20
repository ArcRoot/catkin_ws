#!/usr/bin/env python3
#-- coding:utf-8 --
####################################################################
# 프로그램 명 : main.py
# 작  성  자 : (주)자이트론
# 본 프로그램은 상업라이센스에 의해 제공되므로 무단배포 및 상업적 이용을 금합니다.
####################################################################

import simulator
import signal
import sys
import os

def signal_handler(sig, frame):
    os.system('killall -9 roslaunch roscore python')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
simulator.main()
