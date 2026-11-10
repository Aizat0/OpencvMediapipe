import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera is not opened")
    exit()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils
fingers = [4, 8, 12, 16, 20]
while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame error")
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for n, hand in enumerate(result.multi_hand_landmarks):
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )
            h, w, c = frame.shape
            x, y = int(hand.landmark[0].x * w), int(hand.landmark[0].y * h)
            for finger in fingers:
                fx = int(hand.landmark[finger].x * w)
                fy = int(hand.landmark[finger].y * h)
                cv2.circle(
                    frame,(fx, fy),15,(0, 255, 255), -1)
            cv2.putText(frame,f'{n + 1}',(x, y), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
        count_hands = len(result.multi_hand_landmarks)
        cv2.putText(frame,f'Hands: {count_hands}',(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()