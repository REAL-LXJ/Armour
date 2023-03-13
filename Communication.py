# -*- coding: utf-8 -*-
"""
Created on 1/21 2021

@author: hhx
"""

import serial
import serial.tools.list_ports
from CRC import *
from struct import *

class Communication:
    
    def __init__(self, com, bps, timeout):
        '''串口通信初始化
        @para com: 端口
        @para bps: 波特率
        @para timeout: 最大读取超时
        @attention 
            函数原型默认内容8位，无奇偶校验，1位终止位，此处保持默认
        '''
        self.port = com
        self.bps = bps
        self.timeout = timeout
        
    def OpenEngine(self):
        '''开启串口
        @return bool: 开启是否成功
        '''
        self.myEngine = serial.Serial(self.port, self.bps, timeout = self.timeout)
    
    def SendMessage(self, m):
        '''发送数据
        @para message(bytes)
        '''
        self.myEngine.write(m)
        
    def ReciveData(self):
        data = self.myEngine.readline()
        print(data)
        return -1, -1, -1
        try:
            data = self.myEngine.readline()#方式二print("接收ascii数据：", data)
            #blue/red  打符/自瞄 
            #yawImuPos (float)
            #crcCode (unsigned char)
            #共7位
            crc = getCRC(data, 6)
            if crc == data[-2]:
                myColor = data[0]
                myMode = data[1]
                yawPos = unpack('f',data[2:6])
                #print(yawPos)
                return myColor, myMode, yawPos                

            else:
                return -1, -1, -1
                #print(data)
                #print(crc)
        except:
            print("no message recive")
        
    def CloseEngine(self):
        self.myEngine.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    