import cv2
import mediapipe as mp
import numpy as np

mp_hands=mp.solutions.hands
hands=mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw=mp.solutions.drawing_utils
cap=cv2.VideoCapture(0)
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
    success,img=cap.read()
    if not success:
        break
    img=cv2.flip(img,1)
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    if result.multi_hand_landmarks:
        hand=result.multi_hand_landmarks[0]
        mp_draw = draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
        lm=hand.landmark
        fingers=[]
        fingers.append(1 if lm[4].x<lm[3].x else 0)
        fingers.append(1 if finger(lm,8,6,5) else 0)
        fingers.append(1 if finger(lm,12,10,9) else 0)
        fingers.append(1 if finger(lm,16,14,13) else 0)
        fingers.append(1 if finger(lm,20,18,17) else 0)
        if fingers == [1, 0, 0, 0, 0]:
            letter = 'A'
        elif fingers == [0, 1, 1, 1, 1]:
            letter = 'B'
        elif fingers == [1, 1, 1, 1, 1]:
            letter = 'C'
        elif fingers == [0, 1, 0, 0, 0]:
            letter = 'D'
        elif fingers == [0, 0, 0, 0, 0]:
            letter = 'E'
        elif fingers == [0, 0, 1, 1, 1]:
            letter = 'F'
        elif fingers == [1, 1, 0, 0, 0]:
            letter = 'G'
        elif fingers == [1, 1, 1, 0, 0]:
            letter = 'H'
        else:
            letter = "-"
        cv2.putText(img, f'letters: {letter}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img,f'fingers: {fingers}',(10, 90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.putText(img,f'Hands: {len(result.multi_hand_landmarks)}',(10,30),cv2.FONT_ITALIC,1,(0,255,0),2)
    cv2.imshow("Frame",img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()