import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera is not opened")
    exit()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
draw = mp.solutions.drawing_utils
id_fingers = [8, 12, 16, 20]
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera is empty")
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    fingers_count = 0
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
            fingers = []
            for finger in id_fingers:
                if hand.landmark[finger].y < hand.landmark[finger - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            fingers_count = sum(fingers)
            cv2.putText(frame,f"Fingers: {fingers_count}",(10, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 0),2)
    if fingers_count == 1:
        new_frame = frame
    elif fingers_count == 2:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif fingers_count == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 150)
        new_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif fingers_count == 4:
        new_frame = cv2.GaussianBlur(frame, (35, 35), 0)
    else:
        new_frame = frame
    cv2.imshow("Frame", new_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()