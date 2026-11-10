import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Camera is not opened')
    exit()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_draw = mp.solutions.drawing_utils
id_fingers = [4, 8, 12, 16, 20]
while True:
    ret, frame = cap.read()
    if not ret:
        print('Cadr is not')
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for n, i in enumerate(result.multi_hand_landmarks):
            mp_draw.draw_landmarks(frame, i, mp_hands.HAND_CONNECTIONS)
            fingers = []
            for fing in id_fingers:
                if i.landmark[fing].y < i.landmark[fing - 1].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            cv2.putText(frame, f'{sum(fingers)}', (10, 60), cv2.FONT_ITALIC, 1, (255, 255, 0), 2)
        count_hands = len(result.multi_hand_landmarks)
        cv2.putText(frame, f'Hands: {count_hands}', (10, 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)
    cv2.imshow('Frame: ', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
