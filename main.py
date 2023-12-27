import pygame
import subprocess
from Timer import setInterval
from Timer import clearInterval
import dbCommands
import cv2 as cv
import time
import numpy as np
import copy
import PoseEstimationModule as pm
import random

# Define the function to launch the Tkinter window
def showInfoPage():#Function that calls the Info page
    process=subprocess.Popen(["python", "tkinterScreens/tkinterInfo.py"])
    process.wait()
def showAlert1Page():#Function that calls the Info page
    process=subprocess.Popen(["python", "tkinterScreens/tkinterAlert1.py"])
    process.wait()
def showAlert2Page():#Function that calls the Info page
    process=subprocess.Popen(["python", "tkinterScreens/tkinterAlert2.py"])
    process.wait()
pygame.init()#It initializes pygame

# Widths and heights
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
TOP_RECT_HEIGHT=int(SCREEN_HEIGHT * 0.11)

#Colors
TOP_RECT_COLOR=(0, 0, 102)
BLACK=(0,0,0)
PINK=(255, 0, 255)
COLOR_INACTIVE=pygame.Color('lightskyblue3')
COLOR_ACTIVE=pygame.Color('dodgerblue2')
COLOR_INPUT_USER=COLOR_INACTIVE
COLOR_INPUT_PASSWORD=COLOR_INACTIVE

#Inputs content
textInputUser=''
textInputPassword=''
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Set the Width and height of the screen

#Control variables
activeInputUser=False
activeInputPassword=False

#Donts
font1=pygame.font.SysFont('arial', 32, True, False)
font2=pygame.font.Font(None, 32)
font3=pygame.font.SysFont('arial', 25, True, False)
font4=pygame.font.SysFont('arial', 12, True, False)
pygame.time.Clock().tick(120)#Defines the FPS limit

#Set up the input box
inputUser=pygame.Rect(50, 150, 200, 32)
inputPassword=pygame.Rect(50,250,200,32)

initialPage=True
################################################
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
globalIndex=0
def newAttempt():#It creates a new attempt in the game(After complete a cicle)
    global pictures, listPositions, randomValue, lastCorrectPositions, currentRightColumnPosition, currentRightLinePosition, currentLeftColumnPosition, currentLeftLinePosition, globalIndex, firstAttempt, paused, points, varTimer,seconds
    if (firstAttempt==True):#If it is the first attempt...
       listPositions=[['26.png', [(320, 80), (533, 244)], [(0, 1), (1, 2)]]]
       firstAttempt=False
    if (((currentRightLinePosition,currentRightColumnPosition)!=listPositions[globalIndex][2][1])or((currentLeftLinePosition,currentLeftColumnPosition)!=listPositions[globalIndex][2][0])):#If he lost the game...
        print("PERDEU!!!!")
        paused=True
        dbCommands.setNewRecord(points,currentUserName)
        points=0
        globalIndex=0
        seconds=3
        return
    if((globalIndex==len(listPositions)-1)and(paused==False)):#If he completed a cicle...
        points=points+len(listPositions)
        print("GANHOU, PRÓXIMA!!!")
        updateList()
        globalIndex=0
    else:
        globalIndex=globalIndex+1
def updateList():#It put a new position in the list position
    global listPositions, randomValue, lastCorrectPositions,currentRightColumnPosition,currentRightLinePosition,currentLeftColumnPosition,currentLeftLinePosition
    randomValue=random.randint(0, 8)
    while(lastCorrectPositions==pictures[randomValue]):
        randomValue=random.randint(0, 8)
    listPositions.append(pictures[randomValue])
    lastCorrectPositions=pictures[randomValue]
    print(listPositions)
def onMouse(event, x, y, flags, param):#openCV mouse event
    if event == cv.EVENT_LBUTTONDOWN:#IF it was a click
        print("Posição do mouse: x={}, y={}".format(x, y))
seconds=3
def counter():#Function that is called each second
    global seconds
    seconds=seconds-1 if seconds>0 else 0
    if seconds==0:
        seconds=2
        if(paused==False):
            newAttempt()
cap=cv.VideoCapture(0,cv.CAP_DSHOW)
wCam, hCam = 640, 480
detector=pm.poseDetector()
paused=True
currentUserName=None
positionArray=[]
varTimer=setInterval(counter,1)
pygame.display.set_caption("MoveVision")#Pygame window name
while True:
    _,frame=cap.read()
    frame=cv.flip(frame, 1)
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
        detector.findAngle(frame,12,14,18)#Right Arm
        detector.findAngle(frame,11,13,17)#Left arm
        for i in range(0,3,1):#range(start, stop, step)
            #It is responsable to get the current X and Y position in the 3x3 matrix
            if((rightHand[1]<arrayX[i][1])and(rightHand[1]>arrayX[i][0])):
                currentRightColumnPosition=i
            if((rightHand[2]<arrayY[i][1])and(rightHand[2]>arrayY[i][0])):
                currentRightLinePosition=i
            if((leftHand[1]<arrayX[i][1])and(leftHand[1]>arrayX[i][0])):
                currentLeftColumnPosition=i
            if((leftHand[2]<arrayY[i][1])and(leftHand[2]>arrayY[i][0])):
                currentLeftLinePosition=i
    cTime=time.time()
    fps=int(1/(cTime-pTime))#It gets the FPS
    pTime=cTime
    cv.putText(frame,f"FPS: {(fps)}",(5,30),cv.FONT_HERSHEY_PLAIN,2,PINK,3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
    key=cv.waitKey(1)#ESC = 27
    if paused==False:
        frame[320:480,divWidth:426]=blank
        img=cv.imread(f'imgs/positions/{listPositions[globalIndex][0]}')
        img_resized = cv.resize(img, (divWidth, divHeight))  # redimensiona para divWidthxdivHeight pixels
        frame[320:480,divWidth:426]=img_resized  # atualiza a região com a imagem redimensionada
        print(globalIndex)
        cv.circle(frame, listPositions[globalIndex][1][0], 40, (0, 255, 0), -1)
        cv.circle(frame, listPositions[globalIndex][1][1], 40, (0, 255, 0), -1)
        cv.putText(frame,str(seconds)+"s",(5,100),cv.FONT_HERSHEY_PLAIN,2,PINK,3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
        cv.putText(frame,f"Points: {(points)}",(5,70),cv.FONT_HERSHEY_PLAIN,2,PINK,3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
    if key==27:#Se apertou o ESC
        paused=True
        points=0
        globalIndex=0
    if not paused:
        cv.imshow("Video",frame)
        cv.setMouseCallback("Video", onMouse)
    if (paused==True):
        try:
            cv.destroyWindow("Video")
        except:
            pass
    for event in pygame.event.get():#Pass in each event
        if event.type==pygame.QUIT:#If the quit button was clicked...
            pygame.quit()#Go out pygame
            clearInterval(varTimer)
            quit()#Go out aplication
        elif event.type==pygame.MOUSEBUTTONDOWN:#If happened a mouse click...
            xPos, yPos=event.pos#It gets the mouse position
            currentInput=None
            print(f"Mouse position: X={xPos} - Y={yPos}")
            if((xPos>590)and(xPos<640)and(yPos>0)and(yPos<50)):#Info button clicked...
                showInfoPage()
            if(initialPage):
                if((xPos>30)and(xPos<155)and(yPos>385)and(yPos<455)):#Login button clicked...
                    resultQuery=dbCommands.login(textInputUser,textInputPassword)
                    if(resultQuery!=None):
                        initialPage=False
                        currentUserName=textInputUser
                    else:
                        showAlert2Page()
                if((xPos>485)and(xPos<606)and(yPos>385)and(yPos<455)):#Register face button clicked...
                    if((textInputUser!="")and(textInputPassword!="")):  
                        resultQuery=dbCommands.Insert(textInputUser,textInputPassword)
                        if (resultQuery==None):
                            dbCommands.login(textInputUser,textInputPassword)
                            initialPage=False
                            currentUserName=textInputUser
                    else:
                        showAlert1Page()
                if inputUser.collidepoint(event.pos):#Input user clicked...
                    activeInputUser=not activeInputUser#Toggle the var
                else:#Click happened out of Input user
                    activeInputUser=False
                if inputPassword.collidepoint(event.pos):#Input password clicked...
                    activeInputPassword=not activeInputPassword#Toggle the var
                else:#Clicked out of Input user
                    activeInputPassword=False
                # change the color of the input box
                COLOR_INPUT_USER=COLOR_ACTIVE if activeInputUser else COLOR_INACTIVE
                COLOR_INPUT_PASSWORD=COLOR_ACTIVE if activeInputPassword else COLOR_INACTIVE
            else:
                if ((xPos<410)and(xPos>213)and(yPos>298)and(yPos<363)):
                    if paused==True:
                        seconds=3
                        paused=False
                        listPositions=[['26.png', [(320, 80), (533, 244)], [(0, 1), (1, 2)]]]
                        globalIndex=0
        if event.type==pygame.KEYDOWN:
            if (initialPage):#If it is in the initial page
                if event.unicode.isprintable():
                    if(activeInputUser):#If you clicked in the input user field
                        textInputUser+=event.unicode#It gets the caracter clicked in the keyboard
                    if(activeInputPassword):#If YOU clicked in the input password field
                        textInputPassword+=event.unicode#It gets the caracter clicked in the keyboard
                elif event.key==pygame.K_BACKSPACE:#If you clicked in the backspace (<-) 
                    if(activeInputUser):#If you clicked in the input user field
                        textInputUser=textInputUser[:-1]#Delete the last caracter
                    if(activeInputPassword):#If YOU clicked in the input password field
                        textInputPassword=textInputPassword[:-1]#Delete the last caracter
    if (initialPage):#If it is the initial page
        screen.fill((180, 50, 180))
        pygame.draw.rect(screen, TOP_RECT_COLOR, (0, 0, SCREEN_WIDTH, TOP_RECT_HEIGHT))
        #Importing files and adding elements
        logo=pygame.image.load('imgs/logo.png')#Cria objeto para a imagemLogo
        logo=pygame.transform.scale(logo, (230, 40))#Defines the new width and height of the image
        screen.blit(logo,(0, 5))
        infoBtn=pygame.image.load('imgs/info.png')#Cria objeto para a imagemLogo
        infoBtn=pygame.transform.scale(infoBtn, (70, 70))#Defines the new width and height of the image
        screen.blit(infoBtn, (SCREEN_WIDTH*0.90, -10))
        loginBtn=pygame.image.load('imgs/loginBtn.png')#Cria objeto para a imagemLogo
        loginBtn=pygame.transform.scale(loginBtn, (130, 70))#Defines the new width and height of the image
        screen.blit(loginBtn, (30, SCREEN_HEIGHT*0.80))
        registerBtn=pygame.image.load('imgs/registerBtn.png')#Cria objeto para a imagemLogo
        registerBtn=pygame.transform.scale(registerBtn, (130, 70))#Defines the new width and height of the image
        screen.blit(registerBtn, ((SCREEN_WIDTH-160), SCREEN_HEIGHT*0.80))
        
        textFormated1=font3.render("User: ", False, BLACK)
        userLabel=textFormated1.get_rect()
        userLabel.center=(85, 130)
        screen.blit(textFormated1, userLabel)
        textFormated3=font3.render("Password: ", False, BLACK)
        passwordLabel=textFormated3.get_rect()
        passwordLabel.center=(115, 230)
        screen.blit(textFormated3, passwordLabel)
        textFormated2=font3.render("Welcome to MoveVision!!", False, BLACK)
        welcomeText=textFormated2.get_rect()
        welcomeText.center=(SCREEN_WIDTH//2, 70)
        screen.blit(textFormated2, welcomeText)
        # Render the inputUser text
        txtUser=font2.render(textInputUser, True, (0,0,0))
        # Resize the box if the useText is too long
        width=max(200, txtUser.get_width()+10)
        inputUser.w=width
        # Draw the input box and text surface
        pygame.draw.rect(screen, COLOR_INPUT_USER, inputUser, border_radius=5)
        screen.blit(txtUser, inputUser)
        # Render the inputUser text
        txtPassword=font2.render(textInputPassword, True, (0,0,0))
        # Resize the box if the useText is too long
        width=max(200, txtPassword.get_width()+10)
        inputPassword.w=width
        # Draw the input box and text surface
        pygame.draw.rect(screen, COLOR_INPUT_PASSWORD, inputPassword, border_radius=5)
        screen.blit(txtPassword, inputPassword)
    else:
        pygame.draw.rect(screen,(0,0,180),(0,TOP_RECT_HEIGHT,SCREEN_WIDTH,SCREEN_HEIGHT-TOP_RECT_HEIGHT))#Desenha retangulo
        #Importing files and adding elements
        playBTn=pygame.image.load('imgs/playBtn.png')#Cria objeto para a imagemLogo
        playBTn=pygame.transform.scale(playBTn, (230, 100))#Defines the new width and height of the image
        screen.blit(playBTn,(SCREEN_WIDTH//2-120, SCREEN_HEIGHT*0.6))
        userRecord=dbCommands.getUserRecord(currentUserName)
        userRecordSurface = font4.render(f"Your record is {userRecord[0]} points.", True, (255, 255, 255))
        screen.blit(userRecordSurface, (SCREEN_WIDTH//2-73, SCREEN_HEIGHT*0.8))
        recordsList=dbCommands.getRecords()
        labelRecord=font3.render(f"Records: ", False, PINK)
        recordText=labelRecord.get_rect()
        recordText.center=(70, 110)
        screen.blit(labelRecord, recordText)
        for i in range(0,len(recordsList),1):
            itemSurface = font4.render(f"{i+1}. {recordsList[i][1]} - {recordsList[i][3]} points", True, (255, 255, 255))
            screen.blit(itemSurface, (10, (20*i)+140))
        textFormated2=font3.render(f"Welcome to MoveVision, {currentUserName}!!", False, PINK)
        welcomeText=textFormated2.get_rect()
        welcomeText.center=(SCREEN_WIDTH//2, 70)
        screen.blit(textFormated2, welcomeText)
    pygame.display.flip()