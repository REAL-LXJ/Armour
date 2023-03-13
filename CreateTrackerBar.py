import cv2
import numpy as np


#滑动条参数改变默认处理函数
def nothing(*arg):
    pass

def CreateHsvTrackerBar(lowHue, lowSat, lowVal, highHue, highSat, highVal):
    cv2.namedWindow('colorTest')
    # Lower range colour sliders.
    cv2.createTrackbar('lowHue', 'colorTest', lowHue, 255, nothing)
    cv2.createTrackbar('lowSat', 'colorTest', lowSat, 255, nothing)
    cv2.createTrackbar('lowVal', 'colorTest', lowVal, 255, nothing)
    # Higher range colour sliders.
    cv2.createTrackbar('highHue', 'colorTest', highHue, 255, nothing)
    cv2.createTrackbar('highSat', 'colorTest', highSat, 255, nothing)
    cv2.createTrackbar('highVal', 'colorTest', highVal, 255, nothing)
    

def CreateGBTrackerBar(GBSize):
    cv2.namedWindow('GBTest')
    cv2.createTrackbar('xsize', 'GBTest', GBSize[0], 25, nothing)
    cv2.createTrackbar('ysize', 'GBTest', GBSize[1], 25, nothing)


def CreateLightBarScreenTrackerBar(maxAngleError, minLongSide, ratioMin):
    cv2.namedWindow('LBTest')
    cv2.createTrackbar('maxAngleError', 'LBTest', maxAngleError, 30, nothing)
    cv2.createTrackbar('minLongSide', 'LBTest', minLongSide, 20, nothing)
    cv2.createTrackbar('ratioMin', 'LBTest', int(ratioMin*10), 30, nothing)


def CreateArmorScreenTrackerBar(yDisMax, xDisMax, angleErrMax, maxRatioXY, minCenterDisRatio, maxCenterDisRatio):
    cv2.namedWindow('armorTest')
    cv2.createTrackbar('yDisMax', 'armorTest', yDisMax, 50, nothing)
    cv2.createTrackbar('xDisMax', 'armorTest', xDisMax, 600, nothing)
    cv2.createTrackbar('angleErrMax', 'armorTest', angleErrMax, 50, nothing)
    cv2.createTrackbar('maxRatioXY', 'armorTest', int(maxRatioXY*10), 40, nothing)
    cv2.createTrackbar('minCenterDisRatio', 'armorTest', minCenterDisRatio*10, 20, nothing)
    cv2.createTrackbar('maxCenterDisRatio', 'armorTest', maxCenterDisRatio*10, 100, nothing)


def CreateRangeTrackerBar(disRatio, epaWidth):
    cv2.namedWindow('RangeTest')
    cv2.createTrackbar('disRatio', 'RangeTest', disRatio, 50000, nothing)
    cv2.createTrackbar('epaWidth', 'RangeTest', int(epaWidth*10), 100, nothing)




def UpDatePara(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug, z, imageprocess):
    if hsvDebug:
        print("distance: ", z)
        lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
        lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
        lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')
        highHue = cv2.getTrackbarPos('highHue', 'colorTest')
        highSat = cv2.getTrackbarPos('highSat', 'colorTest')
        highVal = cv2.getTrackbarPos('highVal', 'colorTest')
        hsvPara = np.array([[lowHue, lowSat, lowVal], [highHue, highSat, highVal]])
        imageprocess.SetHSVPara(hsvPara)    
        
    if GBSizeDebug:
        xsize = cv2.getTrackbarPos('xsize', 'GBTest')
        ysize = cv2.getTrackbarPos('ysize', 'GBTest')
        if xsize % 2 == 0:
            xsize += 1
        if ysize % 2 == 0:
            ysize += 1
        GBSize = [xsize, ysize]
        imageprocess.SetGBPara(GBSize)
        
    if lightBarDebug:
        maxAngleError = cv2.getTrackbarPos('maxAngleError', 'LBTest')
        minLongSide = cv2.getTrackbarPos('minLongSide', 'LBTest')
        ratioMin = float(cv2.getTrackbarPos('ratioMin', 'LBTest'))/10
        imageprocess.SetLightBarPara(maxAngleError, minLongSide, ratioMin)
    
    if armorDebug:
        yDisMax = cv2.getTrackbarPos('yDisMax', 'armorTest')
        xDisMax = cv2.getTrackbarPos('xDisMax', 'armorTest')
        angleErrMax = cv2.getTrackbarPos('angleErrMax', 'armorTest')
        maxRatioXY = float(cv2.getTrackbarPos('maxRatioXY', 'armorTest'))/10
        minCenterDisRatio = float(cv2.getTrackbarPos('minCenterDisRatio', 'armorTest'))/10
        maxCenterDisRatio = float(cv2.getTrackbarPos('maxCenterDisRatio', 'armorTest'))/10
        imageprocess.SetArmorPara(yDisMax, xDisMax, angleErrMax, maxRatioXY, minCenterDisRatio, maxCenterDisRatio)

    if rangeDebug:
        disRatio = cv2.getTrackbarPos('disRatio', 'RangeTest')
        epaWidth = float(cv2.getTrackbarPos('epaWidth', 'RangeTest'))/10
        imageprocess.SetRangingPara(disRatio, epaWidth)
        
def DebugInit(hsvDebug, GBSizeDebug, lightBarDebug, armorDebug, rangeDebug, hsv, GB, lb, ar, ra):
    if hsvDebug:
        CreateHsvTrackerBar(hsv[0][0], hsv[0][1], hsv[0][2], hsv[1][0], hsv[1][1], hsv[1][2])
    if GBSizeDebug:
        CreateGBTrackerBar(GB)
    if lightBarDebug:
        CreateLightBarScreenTrackerBar(lb[0], lb[1], lb[2])
    if armorDebug:
        CreateArmorScreenTrackerBar(ar[0], ar[1], ar[2], ar[3], ar[4], ar[5])
    if rangeDebug:
        CreateRangeTrackerBar(ra[0], ra[1])