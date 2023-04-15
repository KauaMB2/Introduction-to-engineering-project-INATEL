import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import copy
import math
def calc_bounding_rect(frame, landmarks):#Função para calcular a borda do retângulo
    frame_width, frame_height = frame.shape[1], frame.shape[0]#It gets the width and height
    landmark_array = np.empty((0, 2), int)#It create a numpy array
    for _, landmark in enumerate(landmarks.landmark):#It pass in each landmark
        landmark_x = min(int(landmark.x * frame_width), frame_width - 1)#It transform the landmark position accordgin the screen width
        landmark_y = min(int(landmark.y * frame_height), frame_height - 1)#It transform the landmark position accordgin the screen height
        landmark_point = [np.array((landmark_x, landmark_y))]#It Puts the point in a numpy array
        landmark_array = np.append(landmark_array, landmark_point, axis=0)#It adds the landmarkArray more one position
    x, y, w, h = cv.boundingRect(landmark_array)#Draw the picture
    return [x, y, x + w, y + h]
class poseDetector():
    def __init__(self,mode=False,smooth=True,detectionConfidence=0.5,trackConfidence=0.5):
        self.mode=mode
        self.smooth=smooth
        self.detectionConfidence=detectionConfidence
        self.trackConfidence=trackConfidence
        self.mpDraw=mp.solutions.drawing_utils#It returns the function position in the memory
        self.mpPose=mp.solutions.pose#It returns the function position in the memory
        self.pose=self.mpPose.Pose(static_image_mode=self.mode,min_detection_confidence=self.detectionConfidence,min_tracking_confidence=self.trackConfidence)
        """INSIDE THE LIBRARY:
        def __init__(self,
               static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        """
    def findPose(self,frame,debug_frame,drawBourding=True,drawBody=True):#Exibe corpo inteiro e borda
        frameRGB=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.results=self.pose.process(frameRGB)
        #print(results.pose_landmarks)#Fala se algo foi ou não rastreado na câmera ou vídeo
        if(self.results.pose_landmarks):#Se algo for detectado...
            if drawBody:
                self.mpDraw.draw_landmarks(frame,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)#Desenha os pontos(landmarks) e as linhas entre eles
            if drawBourding:
                brect = calc_bounding_rect(debug_frame, self.results.pose_landmarks)
                cv.rectangle(frame, (brect[0]-15, brect[1]-130), (brect[2]+10, brect[1]-90),(0, 0, 0), -1)
                cv.putText(frame, "Person", (brect[0]-10, brect[1]-104),cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4, cv.LINE_AA)
                cv.rectangle(frame, (brect[0]-15, brect[1]-90), (brect[2]+10, brect[3]+10),(0, 255, 0), 5)
        return frame

    def findPosition(self,frame,draw=True):#Pega todas os landmarks e coloca dentro de uma lista "lmList" para customizar os landmarks e as ligações entre eles
        self.lmList=[]
        if (self.results.pose_landmarks):
            for id, lm in enumerate(self.results.pose_landmarks.landmark):#Pega os landmarks de cada parte do corpo detectada dentro de "results.pose_landmarks"
                h,w,c=frame.shape
                #print(f"{id}\n{lm}")
                cx,cy=int(lm.x*w),int(lm.y*h)
                self.lmList.append([id,cx,cy])
            if draw:
                cv.circle(frame,(self.lmList[10][1],self.lmList[10][2]),8,(0,255,0),cv.FILLED)
                cv.circle(frame,(self.lmList[9][1],self.lmList[9][2]),8,(0,255,0),cv.FILLED)
        return self.lmList
    
    def findAngle(self,frame,p1,p2,p3,drawPoints=True,drawAngle=True):
        #Get the landmarks
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        x3,y3=self.lmList[p3][1:]

        #Get the angle
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))#Comando para achar o ângulo entre duas retas quaisquer no corpo
        angle=int(angle)#Tira as casas decimais
        if(angle<0):
            angle=angle+360
            
        if drawPoints:
            cv.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
            cv.line(frame,(x3,y3),(x2,y2),(255,0,0),3)
            cv.circle(frame,(x1,y1),10,(0,255,0),cv.FILLED)
            cv.circle(frame,(x1,y1),15,(0,255,0),2)
            cv.circle(frame,(x2,y2),10,(0,255,0),cv.FILLED)
            cv.circle(frame,(x2,y2),15,(0,255,0),2)
            cv.circle(frame,(x3,y3),30,(0,255,0),cv.FILLED)
        if drawAngle:
            cv.putText(frame,f"{angle}",(x2-20,y2-20),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
        return angle
def main():
    cTime=0
    pTime=0
    detector=poseDetector()
    cap=cv.VideoCapture(0,cv.CAP_DSHOW)

    while True:
        _,frame=cap.read()
        debug_frame = copy.deepcopy(frame)#Pega o "frame" e joga no debug_frame
        frame=detector.findPose(frame,debug_frame)
        lmList=detector.findPosition(frame)
        if len(lmList)!=0:
            #Right Arm
            detector.findAngle(frame,12,14,16)
            #Left arm
            detector.findAngle(frame,11,13,15)
        cTime=time.time()
        fps=int(1/(cTime-pTime))
        pTime=cTime
        cv.putText(frame,f"FPS: {(fps)}",(5,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)#putText(frame,text,(positionX,positionY),font,tamanho,(B,G,R),espessura)
        key=cv.waitKey(1)#ESC = 27
        if key==27:#Se apertou o ESC
            break
        cv.imshow("Video",frame)
if __name__=="__main__":
    main()
cv.destroyAllWindows()