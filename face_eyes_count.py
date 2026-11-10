import cv2
import mediapipe as mp

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print('Camera is not opened')
    exit()
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_face=mp.solutions.face_mesh
faces=mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw=mp.solutions.drawing_utils
blink_count=0
eye_closed=False
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
        for hand in hand_result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
        count_hands=len(hand_result.multi_hand_landmarks)
        cv2.putText(frame,f'Hands: {count_hands}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    if face_result.multi_face_landmarks:
        face=face_result.multi_face_landmarks[0]
        left_eye=abs(face.landmark[159].y-face.landmark[145].y)
        right_eye=abs(face.landmark[386].y-face.landmark[374].y)
        eye_height=(left_eye+right_eye)/2
        if eye_height<0.015 and not eye_closed:
            eye_closed=True
        elif eye_height>=0.015 and eye_closed:
            blink_count+=1
            eye_closed=False
        for face in face_result.multi_face_landmarks:
            mp_draw.draw_landmarks(frame,face,mp_face.FACEMESH_TESSELATION)
        count_faces=len(face_result.multi_face_landmarks)
        cv2.putText(frame,f'Face: {count_faces}',(10,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.putText(frame,f'Blinks: {blink_count}',(10,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()