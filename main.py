# -*- coding: utf-8 -*-
"""
Created on 1/19 2021

@author: hhx
"""
from ImageProcess import *
from GetFrame import *
#from Communication import *
import numpy as np
import time
from CRC import *
from CreateTrackerBar import *
from getInform import *
#from predict import *

#在实际比赛中，需要先开启串口，再选择json文件去读
#串口在json中的开放，仅为了用户调试时可以使用不同端口
#而机器人的端口是固定的，因此，先保持这个框架，定死在程序运行前

jsonFilePath = 'C:/Users/LXJ/Desktop/infantry/debug_settings.json'
useUART = False
with open(jsonFilePath,'r',encoding = 'utf-8') as load_f:
    load_dict = json.load(load_f,strict=False)
    com = load_dict["UARTSet"]["com"]    
    bps = load_dict["UARTSet"]["bps"]      
    timeout = load_dict["UARTSet"]["timeout"] 
    useUART = load_dict["ModeSwitch"]["uart"]
if __name__ == "__main__":
    
    
    #Windows
    #MySerial = Communication(com, bps, timeout)
    #Linux
    #MySerial = Communication('/dev/ttyUSB0', 115200, timeout=1)
    
    #通过串口接收到红蓝方，决定读哪个json文件
    if useUART:
        MySerial.OpenEngine()
        myColor, myMode, yawPos = MySerial.ReciveData()
        if myColor == 1:
            jsonFilePath = 'c:/Users/10336/Desktop/infantry-py1.0/blue_settings.json'
        else:
            if myColor == 0:
                jsonFilePath = 'c:/Users/10336/Desktop/infantry-py1.0/red_settings.json'
            else:
                if myColor == 1:
                    jsonFilePath = 'c:/Users/10336/Desktop/infantry-py1.0/debug_settings.json' 

    useUART, useCamera, useVideo, videoPath, frameWidth, frameHeight, exposuretime, \
hsvDividingLine, showOriC, videoSpeed, showOriV, com, bps, timeout, hsvDebug, \
GBSizeDebug, lightBarDebug,armorDebug, rangeDebug, lowHnear, lowSnear, lowVnear,  \
highHnear, highSnear, highVnear,lowHFar, lowSFar, lowVFar, highHFar, highSFar, highVFar, \
gbx, gby, maxAngleError, minLongSide, ratioMin, yDisMax, xDisMax, angleErrMax, maxRatioXY, \
minCenterDisRatio, maxCenterDisRatio, disRatio, epaWidth = getInform(jsonFilePath)

    hsvParaNear = np.array([[lowHnear, lowSnear, lowVnear], [highHnear, highSnear, highVnear]])
    hsvParaFar = np.array([[lowHFar, lowSFar, lowVFar], [highHFar, highSFar, highVFar]])    
    GBSize = [gbx, gby]    
    
    DebugInit(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug, hsvParaNear,\
              GBSize, [maxAngleError, minLongSide, ratioMin], [yDisMax, xDisMax, angleErrMax, maxRatioXY, \
              minCenterDisRatio, maxCenterDisRatio], [disRatio, epaWidth])


    
    if useCamera:
        camera = GetFrame()
        #imageprocess = ImageProcess(frameWidth, frameHeight)
        imageprocess = ImageProcess(frameWidth, 
                        frameHeight,
                        hsvParaNear,
                        GBSize,
                        maxAngleError,
                        minLongSide,
                        ratioMin,
                        yDisMax,
                        xDisMax,
                        angleErrMax,
                        maxRatioXY,
                        minCenterDisRatio,
                        maxCenterDisRatio,
                        hsvParaFar,
                        hsvDividingLine,
                        disRatio,
                        epaWidth)
        
        camera.StartCamera()
        camera.SetCamera(frameWidth,frameHeight,exposuretime)
        
        imageprocess.SwitchDebug(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug)
    
        
        while True:
            frame = camera.GetOneFrame()
            
            '''
            @attention 开启hsv debug模式下,远近hsv的不同参数会被滑动条覆盖,请对远近状态分开调试
            '''
            x, y, z = imageprocess.GetArmor(frame)
            if useUART:
                message = PackData(x, y, z, 14)
                MySerial.SendMessage(message)
                myColor, myMode, yawPos = MySerial.ReciveData()
            
            
            
            UpDatePara(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug, z, imageprocess)
            if showOriC:
                cv2.imshow("ori", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                camera.EndCamera()
                break
            
    else:
        if useVideo:
            cap = cv2.VideoCapture(videoPath)   
            #imageprocess = ImageProcess(cap.get(3), cap.get(4))
            imageprocess = ImageProcess(cap.get(3), 
                        cap.get(4),
                        hsvParaNear,
                        GBSize,
                        maxAngleError,  
                        minLongSide,
                        ratioMin,
                        yDisMax,
                        xDisMax,
                        angleErrMax,
                        maxRatioXY,
                        minCenterDisRatio,
                        maxCenterDisRatio,
                        hsvParaFar,
                        hsvDividingLine,
                        disRatio,
                        epaWidth)
            
            imageprocess.SwitchDebug(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug)
        
            t0 = time.time()
            fps = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("No frame")
                    break
                
                '''
                @attention 开启hsv debug模式下,远近hsv的不同参数会被滑动条覆盖,请对远近状态分开调试
                '''
                
                x, y, z = imageprocess.GetArmor(frame)
                if useUART:
                    message = PackData(x, y, z, 14)
                    MySerial.SendMessage(message)                
                    myColor, myMode, yawPos = MySerial.ReciveData()
                    
                
                UpDatePara(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug, z, imageprocess)
                if showOriV:
                    cv2.imshow("colorTest",frame)
                key = cv2.waitKey(int(1000/videoSpeed))
                if key == ord('q'):
                    break
                fps+=1
                t1 = time.time()
                if t1-t0 > 1:
                    #print("fps: ",fps)
                    t0 = time.time()
                    fps = 0
            
            cap.release()
    if useUART:
        MySerial.CloseEngine()
    cv2.destroyAllWindows()