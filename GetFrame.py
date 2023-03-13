# -*- coding: utf-8 -*-
"""
Created on 1/19 2021

@author: hhx
"""

import sys
import json

jsonFilePath = "C:/Users/LXJ/Desktop/infantry/debug_settings.json"
MSVPath = ""
with open(jsonFilePath,'r',encoding = 'utf-8') as load_f:
   
    load_dict = json.load(load_f,strict=False)    
    MVSPath = load_dict["Path"]["MVSPath"]
    
sys.path.append(MVSPath)
#sys.path.append("/opt/MVS/Samples/64/Python/MvImport")
from ctypes import *
from MvCameraControl_class import *
import numpy as np




class GetFrame:
    
    def StartCamera(self):
        SDKVersion = MvCamera.MV_CC_GetSDKVersion(self)
        print ("SDKVersion[0x%x]" % SDKVersion)

        deviceList = MV_CC_DEVICE_INFO_LIST()
        self.deviceList = deviceList
        tlayerType = MV_USB_DEVICE

        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            print ("enum devices fail! ret[0x%x]" % ret)
            sys.exit()

        if deviceList.nDeviceNum == 0:
            print ("find no device!")
            sys.exit()

        print ("Find %d devices!" % deviceList.nDeviceNum)

        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            print ("\nu3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
            strModeName = strModeName + chr(per)
            print ("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
                print ("user serial number: %s" % strSerialNumber)

        #取我们唯一的设备号
        nConnectionNum = "0"
        if int(nConnectionNum) >= deviceList.nDeviceNum:
            print ("intput error!")
            sys.exit()
        cam = MvCamera() 
        self.cam = cam
        
    def SetCamera(self,Width,Height,ExposureTime):        
        # ch:创建相机实例 | en:Creat Camera Object   
        deviceList = self.deviceList
        cam = self.cam
        ret = cam.MV_CC_SetFloatValue("ExposureTime", ExposureTime)
        ret = cam.MV_CC_SetFloatValue("Width", Width)
        ret = cam.MV_CC_SetFloatValue("Height", Height)
        nConnectionNum = "0"


        # ch:选择设备并创建句柄| en:Select device and create handle
        stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
        
        ret = cam.MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
            print ("create handle fail! ret[0x%x]" % ret)
            sys.exit()
            

        # ch:打开设备 | en:Open device
        ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print ("open device fail! ret[0x%x]" % ret)
            sys.exit()
            

        # ch:设置触发模式为off | en:Set trigger mode as off
        ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print ("set trigger mode fail! ret[0x%x]" % ret)
            sys.exit()
            

        # ch:获取数据包大小 | en:Get payload size
        stParam =  MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
        ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != 0:
            print ("get payload size fail! ret[0x%x]" % ret)
            sys.exit()
        nPayloadSize = stParam.nCurValue

        # ch:开始取流 | en:Start grab image

        ret = cam.MV_CC_StartGrabbing()

        if ret != 0:
            print ("start grabbing fail! ret[0x%x]" % ret)
            self.EndCamera()
            sys.exit()

        data_buf = (c_ubyte * nPayloadSize)()
        pData,nDataSize = data_buf, nPayloadSize
        self.pData = pData
        self.nDataSize = nDataSize

        
    def GetOneFrame(self):
        pData = self.pData
        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
        temp = np.array(pData)
        ret = self.cam.MV_CC_GetOneFrameTimeout(byref(pData), self.nDataSize, stFrameInfo, 1000)
        temp = temp.reshape((480,1440,3))
        return temp
    
    def EndCamera(self):
        cam = self.cam
        # ch:停止取流 | en:Stop grab image
        ret = cam.MV_CC_StopGrabbing()
        if ret != 0:
            print ("stop grabbing fail! ret[0x%x]" % ret)
            del data_buf
            sys.exit()
                
        # ch:关闭设备 | Close device
        ret = cam.MV_CC_CloseDevice()
        if ret != 0:
            print ("close deivce fail! ret[0x%x]" % ret)
            del data_buf
            sys.exit()

        # ch:销毁句柄 | Destroy handle
        ret = cam.MV_CC_DestroyHandle()
        if ret != 0:
            print ("destroy handle fail! ret[0x%x]" % ret)
            del data_buf
            sys.exit()
                
        
            
