# -*- coding: utf-8 -*-
"""
Created on 1/19 2021

@author: hhx
"""
import cv2
import numpy as np
import math

from functools import singledispatch
 


 


class ImageProcess:
    

    def __init__(self,width,
                        height,
                        hsvParaNear=0,
                        GBSize=0,
                        maxAngleError=0,
                        minLongSide=0,
                        ratioMin=0,
                        yDisMax=0,
                        xDisMax=0,
                        angleErrMax=0,
                        maxRatioXY=0,
                        minCenterDisRatio=0,
                        maxCenterDisRatio=0,
                        hsvParaFar=0,
                        hsvDividingLine=0,
                        disRatio=0,
                        epaWidth=0):
        '''
        变量初始化
        @para variableList(list)
        '''
        self.__xCenter = width/2
        self.__yCenter = height/2
        self.hsvParaNear = hsvParaNear
        self.GBSize = GBSize
        self.maxAngleError = maxAngleError
        self.minLongSide = minLongSide
        self.ratioMin = ratioMin
        self.yDisMax = yDisMax
        self.xDisMax = xDisMax
        self.angleErrMax = angleErrMax
        self.maxRatioXY = maxRatioXY
        self.minCenterDisRatio = minCenterDisRatio
        self.maxCenterDisRatio = maxCenterDisRatio
        self.hsvParaFar = hsvParaFar
        self.hsvDividingLine = hsvDividingLine
        self.disRatio = disRatio
        self.epaWidth = epaWidth
        
        self.hsvPara = hsvParaNear
        


    
    def SwitchDebug(self, hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug):
        '''
        选择debug的对象
        @para all(bool)
        '''
        self.hsvDebug = hsvDebug
        self.GBSizeDebug = GBSizeDebug
        self.lightBarDebug = lightBarDebug
        self.armorDebug = armorDebug
        self.rangeDebug = rangeDebug
        
    def SetHSVPara(self, hsvPara):
        ''' 将hsv参数设置到实例中
        参数定死的程序可以将这个函数放到while(True)前只执行一次

        使用滑动条调参则需要将此函数放到每次获取滑动条参数后重新刷新参数

        @para hsvPara(list): 顺序为hMin, sMin, vMin, hMax, sMax, vMax的列表
        '''
        
        self.hsvPara = hsvPara
        
    def SetGBPara(self, GBSize):
        '''
        修改高斯模糊卷积核大小
        @para GBSize(list): [xsize, ysize]
        '''
        self.GBSize = GBSize
        
    def SetLightBarPara(self, maxAngleError, minLongSide, ratioMin):
        '''
        修改灯条筛选参数
        @para maxAngleError(int)
        @para minLongSide(int)
        @para ratioMin(int)
        '''
        self.maxAngleError = maxAngleError
        self.minLongSide = minLongSide
        self.ratioMin = ratioMin
        
    def SetArmorPara(self, yDisMax, xDisMax, angleErrMax, maxRatioXY, minCenterDisRatio, maxCenterDisRatio):
        '''
        修改装甲板筛选参数
        @para all(int)
        '''
        self.yDisMax = yDisMax
        self.xDisMax = xDisMax
        self.angleErrMax = angleErrMax
        self.maxRatioXY = maxRatioXY
        self.minCenterDisRatio = minCenterDisRatio
        self.maxCenterDisRatio = maxCenterDisRatio
        
    def SetRangingPara(self, disRatio, epaWidth):
        '''
        修改测距参数
        @para all(int)
        '''
        self.disRatio = disRatio
        self.epaWidth = epaWidth
        
    def GetArmor(self,frame):
        ''' 返回x，y，z坐标值
        @return int: 装甲中心X值
        @return int: 装甲中心Y值
        @return int: 装甲中心Z值
        @attention: 如果没有检测到任何合格装甲板，返回值均为-2
                    
        '''
        self.__frame = frame
        
        x, y, z = -1, -1, -1
        
        
        # 进行HSV图像处理
        mask = self.__HSV_Process(frame)
        
        # 进行获取灯条矩形列表
        lightBarList = self.__GetLightBar(mask)
        
        # 将灯条拼凑成装甲板
        x , y, disPara = self.__CombineLightBar(lightBarList)
        
            
        # 计算距离
        rangeFlag = True
        if x == -1 or y == -1:
            rangeFlag = False
        z = self.__GetArmorDistance(disPara, rangeFlag)
        
        
        return x, y, z
    
    def __GetArmorDistance(self, disPara, rangeFlag):
        '''
        测算装甲板距离
        @para disPara(list): 测距所需参数列表
        @para rangeFlag(bool): 检测装甲板标志
        @return z(double): 装甲板距离
        '''
        distance = -1
        if rangeFlag:
            #正对时,距离正比于(x0-x1),angle=pre_angle,y0=y1
            #侧对时,angle！=pre_angle,y0！=y1,此时需要通过angle和灯管中心y坐标对距离的正比关系进行修正
            x0, y0 = disPara[0][:]
            x1, y1 = disPara[1][:]
    
            angle = disPara[4]
            preAngle = disPara[5]
            
            k = self.disRatio #20000
            epa = self.epaWidth#1#椭圆宽
            ac = ((preAngle+angle)/2+90)/100#对ac进行归一化
    
            oriXDis = abs(x0-x1)
            
            realXDis = oriXDis/pow(1-(ac**2/epa**2),0.5)
    
    
            distance = k/(realXDis**2+(y0-y1)**2)**0.5
            
            if type(distance) != complex:
                if not self.hsvDebug:
                    if distance > self.hsvDividingLine:
                        self.SetHSVPara(self.hsvParaFar)
                    else:
                        self.SetHSVPara(self.hsvParaNear)
        
        if self.rangeDebug:
            cv2.putText(self.__frame, str(int(distance)), (123,234), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            cv2.imshow("RangeTest",self.__frame)        
    
        return distance
        
        
        
        
        
    def EuclideanDistance(self,c,c0):
        '''
        计算欧氏距离
        @para c(list):[x, y]
        @para c0(list):[x, y]
        @return double:欧氏距离
        '''
        return pow((c[0]-c0[0])**2+(c[1]-c0[1])**2, 0.5)
    
    def __CombineLightBar(self, lightBarList):
        '''
        将灯条合成装甲板
        @para lightBarList(np.array): 灯条矩阵
        @return x(int): 装甲板中心x坐标
        @return y(int): 装甲板中心y坐标
        @return disPara(list): 测距所需装甲板参数
        '''
        disPara = []
        realCenter = [-1, -1]
        preCenter = [-1, -1]

        # d means draw
        centerMax = -1
        dPreCenter = [-1, -1]
        dCenter = [-1, -1]
        dVertices = []
        dLongside = -1
        dAngle = 999
        dPreAngle = 999
        
        
        fineContoursLength = len(lightBarList)
        armorLength = int(((1 + fineContoursLength) * fineContoursLength) / 2)
        armorList = np.zeros((armorLength,12))
        fineArmorLength = 0
        
        for i in range(0,fineContoursLength-1):
            for j in range(i+1,fineContoursLength):
                x0, y0, l0, s0, a0 = lightBarList[i][0:5]
                x1, y1, l1, s1, a1 = lightBarList[j][0:5]
                centerDis = self.EuclideanDistance([x0,y0],[x1,y1])
                angleErr = abs(a0-a1)
                xCenter = (x0+x1)/2
                yCenter = (y0+y1)/2
                lErr = max(l1,l0)/(min(l1,l0)+0.00001)
                xDis = abs(x0-x1)
                yDis = abs(y0-y1)
                ylength = (l0+l1)/2
                lsRatio = centerDis/ylength
                alpha = math.asin(yDis/centerDis)*180/math.pi
                delta = math.sqrt(((y0-y1)*(y0-y1))/((x0-x1)*(x0-x1)))
                if x0 > x1:
                    delta = delta*180/math.pi
                else:
                    delta = -delta*180/math.pi

                armorList[fineArmorLength][0] = centerDis
                armorList[fineArmorLength][1] = angleErr
                armorList[fineArmorLength][2] = xCenter
                armorList[fineArmorLength][3] = yCenter
                armorList[fineArmorLength][4] = lErr
                armorList[fineArmorLength][5] = max(l0,l1)
                armorList[fineArmorLength][6] = xDis
                armorList[fineArmorLength][7] = yDis
                armorList[fineArmorLength][8] = self.EuclideanDistance([xCenter,yCenter],[self.__xCenter,self.__yCenter])
                armorList[fineArmorLength][9] = centerDis/(max(l0,l1)+0.00001)
                armorList[fineArmorLength][10] = i
                armorList[fineArmorLength][11] = j

                #screen
                nowArmor = True
                if yDis > self.yDisMax:
                    armorList[fineArmorLength] = 0
                    nowArmor = False
                #if xDis > self.xDisMax:
                    #armorList[fineArmorLength] = 0
                    #nowArmor = False
                if angleErr > self.angleErrMax:
                    armorList[fineArmorLength] = 0
                    nowArmor = False
                if lErr > self.maxRatioXY:
                    armorList[fineArmorLength] = 0
                    nowArmor = False
                if centerDis < self.minCenterDisRatio*max(l0,l1):
                    armorList[fineArmorLength] = 0
                    nowArmor = False
                if centerDis > self.maxCenterDisRatio*max(l0,l1):
                    armorList[fineArmorLength] = 0
                    nowArmor = False
                if nowArmor:
                    fineArmorLength+=1
                    
        #sort
        armorExist = False
        sort_key = 8 #按中心距离排序
        armorList[::-1] = armorList[armorList[:,sort_key].argsort()]

        if fineArmorLength > 0:
            if armorList[fineArmorLength-1][0]>0:
                if preCenter[0] == -1: #or self.Euclidean_distance(pre_center,real_center) < 30
                    ii = int(armorList[fineArmorLength-1][10])
                    jj = int(armorList[fineArmorLength-1][11])
                    armorExist = True
                    realCenter = [armorList[fineArmorLength-1][2],armorList[fineArmorLength-1][3]]
                    centerMax = armorList[fineArmorLength-1][0]
                    dPreCenter = [lightBarList[ii][0],lightBarList[ii][1]]
                    dCenter = [lightBarList[jj][0],lightBarList[jj][1]]
                    dLongside = armorList[fineArmorLength-1][5]
                    dAngle = lightBarList[ii][4]
                    dPreAngle = lightBarList[jj][4]
                    preCenter = realCenter
            else:
                armorExist = False
                realCenter = [-1, -1]

                if self.armorDebug:
                    # d means draw
                    centerMax = -1
                    dPreCenter = [-1, -1]
                    dCenter = [-1, -1]
                    dVertices = []
                    dLongside = -1
                    dAngle = 999
                    dPreAngle = 999



        

                           
                           
                          
        if self.armorDebug:
            if armorExist: 
                cv2.line(self.__frame, tuple((int(dPreCenter[0]),int(dPreCenter[1]+dLongside/2))), tuple((int(dCenter[0]),int(dCenter[1]+dLongside/2))), (0, 0, 255), 1)
                cv2.line(self.__frame, tuple((int(dPreCenter[0]),int(dPreCenter[1]-dLongside/2))), tuple((int(dCenter[0]),int(dCenter[1]-dLongside/2))), (0, 0, 255), 1)
                cv2.line(self.__frame, tuple((int(dPreCenter[0]),int(dPreCenter[1]+dLongside/2))), tuple((int(dPreCenter[0]),int(dPreCenter[1]-dLongside/2))), (0, 0, 255), 1)
                cv2.line(self.__frame, tuple((int(dCenter[0]),int(dCenter[1]-dLongside/2))), tuple((int(dCenter[0]),int(dCenter[1]+dLongside/2))), (0, 0, 255), 1)
                #cv2.putText(self.__frame, 'a0:' + str(a0), (20,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'a1:' + str(a1), (20,340), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'agErr:' + str(angleErr), (20,380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'yDis:' + str(yDis), (20,420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'xDis:' + str(xDis), (20,460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'lsRatio:' + str(lsRatio), (20,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'alpha:' + str(alpha), (20,540), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                #cv2.putText(self.__frame, 'delta:' + str(delta), (20,580), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            cv2.imshow("armorTest", self.__frame)
            
        disPara = [dPreCenter, dCenter, dVertices, dLongside, dAngle, dPreAngle, centerMax]

        return realCenter[0], realCenter[1], disPara
        
    def __MorphologicalProcessing(self, frame):
        '''
        User defined morphological processing
        '''
        return frame


    def __HSV_Process(self, frame):
        '''         返回二值蒙版
        @para cv.mat: 原始帧bgr图像
        @return cv.mat: 白色为感兴趣的色彩
        '''                    
        frame = cv2.GaussianBlur(frame, (self.GBSize[0], self.GBSize[1]), 0)
        #channel = cv2.split(frame)
        #blue = cv2.subtract(channel[0], channel[2])
        #red = cv2.subtract(channel[2], channel[0])
        #_, threshold = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY)  
        #mask = threshold
        #cv2.imshow("bgr", threshold)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.hsvPara[0], self.hsvPara[1])
        #cv2.imshow("hsv", mask)
        self.__MorphologicalProcessing(mask)
        
        if self.hsvDebug:
            #result = cv2.bitwise_and(frame, frame, mask=mask)
            cv2.imshow("colorTest", mask)
        if self.GBSizeDebug:
            #result = cv2.bitwise_and(frame, frame, mask=mask)
            cv2.imshow("GBTest", mask)
        return mask

    def __GetLightBar(self, mask):
        '''返回灯条列表
        @para mask(cv.mat): 二值图
        @return lightBarList(np.array): 粗筛过后的灯条及其参数
        '''   
        #influenced by opencv version
        #on our pc retval is (binary, contours, hierarchy)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        contoursLength = len(contours)
        fineContoursLength = 0

        #顺序对比的话，总会出一些问题，并且面对不同大小装甲，确实不太好处理，这边还是拿numpy来归纳，也好改一些
        lightBarList = []
        for c in range(contoursLength):
            center, size, angle = cv2.minAreaRect(contours[c])
            #angle = abs(int(angle)%180)
            vertices = cv2.boxPoints((center, size, angle))
            #得到长边和中心点垂直短边向量
            if size[0]<size[1]:
                vector = center-(vertices[0]+vertices[3])/2
                longSide = size[1]
                shortSide = size[0]
            else:
                vector = center-(vertices[0]+vertices[1])/2
                longSide = size[0]
                shortSide = size[1]
            #计算向量和水平轴夹角
            angleHori = int(math.atan2(vector[1], vector[0]) * 180/math.pi)

            #粗筛,只是为了把画出的一些奇怪的轮廓删掉，意义其实不大，但你想不到后面会发生什么，因此还是做一下比较好
            if abs(angleHori+90) < self.maxAngleError and longSide > self.minLongSide and longSide > self.ratioMin*shortSide:
                lightBarList.append([])
                lightBarList[fineContoursLength].append(center[0])
                lightBarList[fineContoursLength].append(center[1])
                lightBarList[fineContoursLength].append(longSide)
                lightBarList[fineContoursLength].append(shortSide)
                lightBarList[fineContoursLength].append(angleHori)
                fineContoursLength += 1
                
        if self.lightBarDebug:
            if fineContoursLength > 0:  
                #cv2.putText(self.__frame, 'ag:' + str(angle), (20,460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                for i in range(fineContoursLength):
                    centerX = lightBarList[i][0]
                    centerY = lightBarList[i][1]
                    #print(centerX,centerY)
                    cv2.circle(self.__frame, (int(centerX), int(centerY)), 5, (0, 255, 0), -1)
            cv2.imshow("LBTest", self.__frame)
            
        return lightBarList
    