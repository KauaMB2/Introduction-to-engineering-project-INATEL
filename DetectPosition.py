import cv2 as cv
import time
import numpy as np
import copy
import PoseEstimationModule as pm
import random
from cronometro import setInterval
from cronometro import clearInterval

cTime=0
pTime=0
count=0
dir=0
divWidth=213
divHeight=160

arrayX=[[0,213],[213,426],[426,639]]
arrayY=[[0,160],[160,320],[320,480]]
currentRightColumnPosition=None
currentRightLinePosition=None
currentLeftColumnPosition=None
currentLeftLinePosition=None
blank=np.zeros((divHeight, divWidth, 3), dtype=np.uint8)
pictures=[['13.png',[(107,80),(533,80)],[(0,0),(0,2)]],['22.png',[(320,80),(320,80)],[(0,1),(0,1)]],['26.png',[(320,80),(533,244)],[(0,1),(1,2)]],['29.png',[(320,80),(533,400)],[(0,1),(2,2)]],['42.png',[(107,244),(533,80)],[(1,0),(0,1)]],['46.png',[(107,244),(533,244)],[(1,0),(1,2)]],['49.png',[(107,244),(533,400)],[(1,0),(2,2)]],['72.png',[(107,396),(320,80)],[(2,0),(0,1)]],['76.png',[(107,396),(533,244)],[(2,0),(1,2)]]]#[picture,[posRigh,posLeft]] -> it is to put a point in the position that the player have to put their hands
listPositions=[['26.png', [(320, 80), (533, 244)], [(0, 1), (1, 2)]]]
lastCorrectPositions=None
randomValue=None
result=None
points=0
firstAttempt=True
camOn=True
globalIndex=0
def getResult():
    return result
def newAttempt():
    global pictures, listPositions, randomValue, lastCorrectPositions, currentRightColumnPosition, currentRightLinePosition, currentLeftColumnPosition, currentLeftLinePosition, globalIndex, firstAttempt, camOn, points, varTimer
    if (firstAttempt==True):
       listPositions=[['26.png', [(320, 80), (533, 244)], [(0, 1), (1, 2)]]]
       firstAttempt=False
    print(globalIndex)
    if (((currentRightLinePosition,currentRightColumnPosition)!=listPositions[globalIndex][2][1])or((currentLeftLinePosition,currentLeftColumnPosition)!=listPositions[globalIndex][2][0])):
        result=[points]
        print("PERDEU!!!!")
        camOn=False
        # cap.release() # libera a câmera
        # cv.destroyAllWindows() # fecha todas as janelas
    print(globalIndex)
    if(globalIndex==len(listPositions)-1):
        points=points+len(listPositions)
        print("GANHOU, PRÓXIMA!!!")
        updateList()
        globalIndex=0
    else:
        globalIndex=globalIndex+1
def updateList():
    global listPositions, randomValue, lastCorrectPositions,currentRightColumnPosition,currentRightLinePosition,currentLeftColumnPosition,currentLeftLinePosition
    
    randomValue=random.randint(0, 8)
    while(lastCorrectPositions==pictures[randomValue]):
        randomValue=random.randint(0, 8)
    listPositions.append(pictures[randomValue])
    lastCorrectPositions=pictures[randomValue]
    print(listPositions)
def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("Posição do mouse: x={}, y={}".format(x, y))
segundos=5
def counter():
    global segundos
    segundos=segundos-1 if segundos>0 else 0
    if segundos==0:
        segundos=5
        newAttempt()

cap=cv.VideoCapture(0,cv.CAP_DSHOW)
wCam, hCam = 640, 480
detector=pm.poseDetector()
varTimer=None
positionArray=[]
def turnOnGame():
    global pictures, listPositions, randomValue, lastCorrectPositions, currentRightColumnPosition, currentRightLinePosition, currentLeftColumnPosition, currentLeftLinePosition, globalIndex, firstAttempt, camOn, points, varTimer, cTime, pTime
    varTimer=setInterval(counter,1)
    while True:
        _,frame=cap.read()
        frame=cv.flip(frame, 1)
        print(globalIndex, len(listPositions))
        debug_frame = copy.deepcopy(frame)#Pega o "frame" e joga no debug_frame
        try:
            frame=detector.findPose(frame,debug_frame,True,True)
        except Exception:
            print(Exception)
            _,frame=cap.read()
            frame=cv.flip(frame, 1)
            debug_frame = copy.deepcopy(frame)#Pega o "frame" e joga no debug_frame
        lmList=detector.findPosition(frame,False)
        cv.line(frame, (divWidth, 0), (divWidth, hCam), (0, 0, 0), 3)
        cv.line(frame, (426, 0), (426, hCam), (0, 0, 0), 3)
        cv.line(frame, (0, divHeight), (wCam, divHeight), (0, 0, 0), 3)
        cv.line(frame, (0, 320), (wCam, 320), (0, 0, 0), 3)
        if (camOn==False):
            clearInterval(varTimer)
            firstAttempt=True
            globalIndex=0
            points=0

        if len(lmList)!=0:
            leftHand=lmList[18]
            rightHand=lmList[17]
            #Right Arm
            detector.findAngle(frame,12,14,18)
            #Left arm
            detector.findAngle(frame,11,13,17)
            for i in range(0,3,1):#range(start, stop, step)
                if((rightHand[1]<arrayX[i][1])and(rightHand[1]>arrayX[i][0])):
                    currentRightColumnPosition=i
                if((rightHand[2]<arrayY[i][1])and(rightHand[2]>arrayY[i][0])):
                    currentRightLinePosition=i
                if((leftHand[1]<arrayX[i][1])and(leftHand[1]>arrayX[i][0])):
                    currentLeftColumnPosition=i
                if((leftHand[2]<arrayY[i][1])and(leftHand[2]>arrayY[i][0])):
                    currentLeftLinePosition=i
        cTime=time.time()
        fps=int(1/(cTime-pTime))
        pTime=cTime
        cv.putText(frame,f"FPS: {(fps)}",(5,30),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
        key=cv.waitKey(1)#ESC = 27
        if camOn==True:
            frame[320:480,divWidth:426]=blank
            img=cv.imread(f'imgs/positions/{listPositions[globalIndex][0]}')
            img_resized = cv.resize(img, (divWidth, divHeight))  # redimensiona para divWidthxdivHeight pixels
            frame[320:480,divWidth:426]=img_resized  # atualiza a região com a imagem redimensionada
            cv.circle(frame, listPositions[globalIndex][1][0], 40, (0, 255, 0), -1)
            cv.circle(frame, listPositions[globalIndex][1][1], 40, (0, 255, 0), -1)
            cv.putText(frame,str(segundos)+"s",(400,320),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
            cv.putText(frame,f"Points: {(points)}",(5,70),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
        if key==27:#Se apertou o ESC
            clearInterval(varTimer)
            cap.release() # libera a câmera
            cv.destroyAllWindows() # fecha todas as janelas
            frame=None
            break
        cv.imshow("Video",frame)
        cv.setMouseCallback("Video", onMouse)
