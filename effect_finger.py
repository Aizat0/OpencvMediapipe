import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera is not opened")
    exit()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)
mp_draw = mp.solutions.drawing_utils
draw_frame = np.zeros((480, 640, 3), dtype=np.uint8)
video_type = 1
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera is empty")
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    colors = [
        ((192, 192, 192), 50),
        ((128, 128, 128), 200),
        ((64, 64, 64), 350),
        ((0, 0, 0), 500)]
    for color, color_x in colors:
        cv2.rectangle(frame,(color_x, 20),(color_x + 100, 100),color,cv2.FILLED)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
            h, w, c = frame.shape
            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)
            cv2.circle(frame, (x, y), 15, (255, 0, 255), cv2.FILLED)
            if 20 < y < 100:
                if 50 < x < 150:
                    video_type = 1
                elif 200 < x < 300:
                    video_type = 2
                elif 350 < x < 450:
                    video_type = 3
                elif 500 < x < 600:
                    video_type = 4
    if video_type == 1:
        new_frame = frame.copy()
    elif video_type == 2:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif video_type == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 150)
        new_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif video_type == 4:
        new_frame = cv2.GaussianBlur(frame, (35, 35), 0)
    image = cv2.add(new_frame, draw_frame)
    cv2.imshow("Frame", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()