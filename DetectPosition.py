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
pictures=[['13.png',[(107,80),(533,80)]],['22.png',[(320,80),(320,80)]],['26.png',[(320,80),(533,244)]],['29.png',[(320,80),(533,400)]],['42.png',[(107,244),(533,80)]],['46.png',[(107,244),(533,244)]],['49.png',[(107,244),(533,400)]],['72.png',[(107,396),(320,80)]],['76.png',[(107,396),(533,244)]]]#[picture,[posRigh,posLeft]] -> it is to put a point in the position that the player have to put their hands
listPositions=[]
randomValue=None
def newAttempt():
    global listPositions, randomValue
    randomValue = random.randint(0, 8)
    listPositions.append(pictures[randomValue])
def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("Posição do mouse: x={}, y={}".format(x, y))
segundos=4
def counter():
    global segundos
    segundos=segundos-1 if segundos>0 else 0
    newAttempt()

cap=cv.VideoCapture(0,cv.CAP_DSHOW)
wCam, hCam = 640, 480
detector=pm.poseDetector()
varTimer=setInterval(counter,1)
positionArray=[]
while True:
    _,frame=cap.read()
    frame[320:480,divWidth:426]=blank
    frame=cv.flip(frame, 1)
    frameRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    debug_frame = copy.deepcopy(frame)#Pega o "frame" e joga no debug_frame
    frame=detector.findPose(frame,debug_frame,True,True)
    lmList=detector.findPosition(frame,False)
    cv.line(frame, (divWidth, 0), (divWidth, hCam), (0, 0, 0), 3)
    cv.line(frame, (426, 0), (426, hCam), (0, 0, 0), 3)
    cv.line(frame, (0, divHeight), (wCam, divHeight), (0, 0, 0), 3)
    cv.line(frame, (0, 320), (wCam, 320), (0, 0, 0), 3)
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
        print(currentLeftColumnPosition, currentLeftLinePosition)
    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime
    
    cv.putText(frame,str(segundos)+"s",(400,320),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
    cv.putText(frame,f"FPS: {(fps)}",(5,30),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
    key=cv.waitKey(1)#ESC = 27
    if (randomValue != None):
        img=cv.imread(f'imgs/positions/{pictures[randomValue][0]}')
        img_resized = cv.resize(img, (divWidth, divHeight))  # redimensiona para divWidthxdivHeight pixels
        frame[320:480,divWidth:426]=img_resized  # atualiza a região com a imagem redimensionada
        cv.circle(frame, pictures[randomValue][1][0], 40, (0, 255, 0), -1)
        cv.circle(frame, pictures[randomValue][1][1], 40, (0, 255, 0), -1)
    if key==27:#Se apertou o ESC
        clearInterval(varTimer)
        break
    cv.imshow("Video",frame)
    cv.setMouseCallback("Video", onMouse)