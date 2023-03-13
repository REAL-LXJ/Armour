import json




def getInform(jsonFilePath):
    print("Load information from settings.json ···")
    with open(jsonFilePath,'r',encoding = 'utf-8') as load_f:
   
        load_dict = json.load(load_f,strict=False)
        
        uart = load_dict["ModeSwitch"]["uart"]
        camera = load_dict["ModeSwitch"]["camera"]
        video = load_dict["ModeSwitch"]["video"]    
        
        videoPath = load_dict["Path"]["videoPath"]
        
        width = load_dict["CameraSet"]["width"]
        height = load_dict["CameraSet"]["height"]
        exposure = load_dict["CameraSet"]["exposure"]
        hsvDivide = load_dict["CameraSet"]["hsvDivide"]
        showOriC = load_dict["CameraSet"]["showOri"]
        
        speed = load_dict["VideoSet"]["speed"]
        showOriV = load_dict["VideoSet"]["showOri"]
        
        com = load_dict["UARTSet"]["com"]    
        bps = load_dict["UARTSet"]["bps"]      
        timeout = load_dict["UARTSet"]["timeout"] 
        
        hsv = load_dict["DebugSwitch"]["hsv"] 
        GB = load_dict["DebugSwitch"]["GBSize"] 
        lightBar = load_dict["DebugSwitch"]["lightBar"] 
        armor = load_dict["DebugSwitch"]["armor"] 
        rang = load_dict["DebugSwitch"]["range"] 
        
        lowHnear = load_dict["hsvSet"]["hsvNear"]["lowHue"]
        lowSnear = load_dict["hsvSet"]["hsvNear"]["lowSat"]
        lowVnear = load_dict["hsvSet"]["hsvNear"]["lowVal"]
        highHnear = load_dict["hsvSet"]["hsvNear"]["highHue"]
        highSnear = load_dict["hsvSet"]["hsvNear"]["highSat"]
        highVnear = load_dict["hsvSet"]["hsvNear"]["highVal"]

        lowHFar = load_dict["hsvSet"]["hsvFar"]["lowHue"]
        lowSFar = load_dict["hsvSet"]["hsvFar"]["lowSat"]
        lowVFar = load_dict["hsvSet"]["hsvFar"]["lowVal"]
        highHFar = load_dict["hsvSet"]["hsvFar"]["highHue"]
        highSFar = load_dict["hsvSet"]["hsvFar"]["highSat"]
        highVFar = load_dict["hsvSet"]["hsvFar"]["highVal"]
        
        gbx = load_dict["GBSet"]["sizex"]
        gby = load_dict["GBSet"]["sizey"]
        
        maxAngleError = load_dict["lightBarSet"]["maxAngleError"]
        minLongSide = load_dict["lightBarSet"]["minLongSide"]        
        ratioMin = load_dict["lightBarSet"]["ratioMin"]  
        
        yDisMax = load_dict["armorSet"]["yDisMax"]  
        xDisMax = load_dict["armorSet"]["xDisMax"]  
        angleErrMax = load_dict["armorSet"]["angleErrMax"]          
        maxRatioXY = load_dict["armorSet"]["maxRatioXY"]          
        minCenterDisRatio = load_dict["armorSet"]["minCenterDisRatio"]          
        maxCenterDisRatio = load_dict["armorSet"]["maxCenterDisRatio"]          

        disRatio = load_dict["RangeSet"]["disRatio"]
        epaWidth = load_dict["RangeSet"]["epaWidth"]

        
    print("Load finished!")

    return uart, camera, video, videoPath, width, height, exposure, hsvDivide, \
showOriC, speed, showOriV, com, bps, timeout, hsv, GB, lightBar, armor, \
rang, lowHnear, lowSnear, lowVnear, highHnear, highSnear, highVnear, \
lowHFar, lowSFar, lowVFar, highHFar, highSFar, highVFar, gbx, gby, \
maxAngleError, minLongSide, ratioMin, yDisMax, xDisMax, angleErrMax, maxRatioXY, \
minCenterDisRatio, maxCenterDisRatio, disRatio, epaWidth
























