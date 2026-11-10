import cv2
import mediapipe as mp
import numpy as np

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print('Camera is not opened')
    exit()
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)
mp_draw=mp.solutions.drawing_utils
draw_frame=np.zeros((480,640,3),dtype=np.uint8)
old_x=None
old_y=None
draw_color=(0,255,0)
while True:
    ret,frame=cap.read()
    if not ret:
        print('Camera is empty')
        break
    frame=cv2.flip(frame,1)
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb_frame)
    colors=[льл
        ((255,0,0),50),
        ((0,255,0),200),
        ((0,0,255),350),
        ((0,255,255),500)
    ]
    for color,color_x in colors:
        cv2.rectangle(frame,(color_x,20),(color_x+100,100),color,cv2.FILLED)
    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,i,mp_hands.HAND_CONNECTIONS)
            h,w,c=frame.shape
            x=int(i.landmark[8].x*w)
            y=int(i.landmark[8].y*h)
            cv2.circle(frame,(x,y),15,(255,0,255),cv2.FILLED)
            if 20<y<100:
                if 50<x<150:
                    draw_color=(255,0,0)
                elif 200<x<300:
                    draw_color=(0,255,0)
                elif 350<x<450:
                    draw_color=(0,0,255)
                elif 500<x<600:
                    draw_color=(0,255,255)
            index_up=i.landmark[8].y<i.landmark[6].y
            middle_up=i.landmark[12].y<i.landmark[10].y
            if index_up and middle_up:
                cv2.putText(frame,'ERASER',(450,200),cv2.FONT_ITALIC,1,(0,0,255),3)
                cv2.circle(frame,(x,y),30,(0,0,255),3)
                if old_x is not None:
                    cv2.line(draw_frame,(old_x,old_y),(x,y),(0,0,0),20)
                old_x=x
                old_y=y
            elif index_up:
                cv2.putText(frame,'DRAW',(450,200),cv2.FONT_ITALIC,1,(0,255,0),3)
                if old_x is not None:
                    cv2.line(draw_frame,(old_x,old_y),(x,y),draw_color,5)
                old_x=x
                old_y=y
            else:
                cv2.putText(frame,'PAUSE',(450,200),cv2.FONT_ITALIC,1,(255,255,255),3)
                old_x=None
                old_y=None
    else:
        old_x=None
        old_y=None
    image=cv2.add(frame,draw_frame)
    cv2.imshow('Frame:',image)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()