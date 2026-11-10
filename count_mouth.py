import time
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Camera is not opened')
    exit()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_face = mp.solutions.face_mesh
faces = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils
mouth_closed = False
mouth_count = 0
last_shot = 0
save_screen = False
current_time = 0
def angle(a,b,c):
    a=np.array([a.x,a.y])
    b=np.array([b.x,b.y])
    c=np.array([c.x,c.y])
    ba=a-b
    bc=c-b
    cos=np.dot(ba,bc)/(np.linalg.norm(ba)*np.linalg.norm(bc)+1e-6)
    return np.degrees(np.arccos(np.clip(cos,-1,1)))
def finger(lm,tip,pip,dip):
    return angle(lm[tip],lm[pip],lm[dip])>160
while True:
    ret,frame=cap.read()
    if not ret:
        print('Camera is empty')
        break
    frame=cv2.flip(frame,1)
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    hand_result=hands.process(rgb_frame)
    face_result=faces.process(rgb_frame)
    if hand_result.multi_hand_landmarks:
        hand=hand_result.multi_hand_landmarks[0]
        lm=hand.landmark
        fingers=[]
        fingers.append(1 if lm[4].x<lm[3].x else 0)
        fingers.append(1 if finger(lm,8,6,5) else 0)
        fingers.append(1 if finger(lm,12,10,9) else 0)
        fingers.append(1 if finger(lm,16,14,13) else 0)
        fingers.append(1 if finger(lm,20,18,17) else 0)
        if fingers==[1,0,0,0,0]:
            current_time=time.time()
            if current_time-last_shot>2:
                save_screen=True
        for hand in hand_result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
        cv2.putText(frame,f'Hands {len(hand_result.multi_hand_landmarks)}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    if face_result.multi_face_landmarks:
        face=face_result.multi_face_landmarks[0]
        mouth_open=abs(face.landmark[13].y-face.landmark[14].y)
        if mouth_open<0.015 and not mouth_closed:
            mouth_closed=True
        elif mouth_open>=0.015 and mouth_closed:
            mouth_count+=1
            mouth_closed=False
        if mouth_open > 0.02:
            cv2.putText(frame, f'mouth open', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        else:
            cv2.putText(frame, f'mouth close', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        for face in face_result.multi_face_landmarks:
            mp_draw.draw_landmarks(frame,face,mp_face.FACEMESH_TESSELATION)
        cv2.putText(frame,f'Faces {len(face_result.multi_face_landmarks)}',(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        cv2.putText(frame,f'Mouth Count {mouth_count}',(10,90),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    if save_screen:
        filename=f"screen_{int(current_time)}.jpg"
        cv2.imwrite(filename,frame)
        print(f"Saved: {filename}")
        last_shot=current_time
        save_screen=False
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()