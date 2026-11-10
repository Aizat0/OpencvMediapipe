import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
canvas = None
prev_x = 0
prev_y = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = frame.copy() * 0
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )
            h, w, c = frame.shape
            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y
            cv2.line(canvas,(prev_x, prev_y),(x, y),(255, 0, 255),5)
            prev_x, prev_y = x, y
    else:
        prev_x, prev_y = 0, 0
    frame = cv2.add(frame, canvas)
    cv2.imshow("Draw", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('c'):
        canvas = frame.copy() * 0
cap.release()
cv2.destroyAllWindows()