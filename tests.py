import cv2
from datetime import datetime
import os

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print('Camera is not opened')
    exit()
path_images = '../step_3'
path_videos = '../videos'
if not os.path.exists(path_images):
    os.makedirs(path_images)
if not os.path.exists(path_videos):
    os.makedirs(path_videos)
counter_image = 0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = int(cap.get(cv2.CAP_PROP_FPS))
form_time = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
form_video = f'{path_videos}/videos_{form_time}.mp4'
out = cv2.VideoWriter(form_video, fourcc, video_fps, (video_width, video_height))
print('2 - for color grey')
print('3 - for kontur')
print('4 - for muddy')
video_type = 1
while True:
    form_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    ret, frame = cap.read()
    if not ret:
        break
    cv2.putText(frame, f'time: {form_date}', (0, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
    if video_type == 2:
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif video_type == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_frame = cv2.Canny(gray, 100, 150)
    elif video_type == 4:
        new_frame = cv2.GaussianBlur(frame, (35, 35), 0)
    else:
        new_frame = frame
    cv2.imshow('Frame', new_frame)
    out.write(frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        image_form = f'{path_images}/screen_{counter_image}.png'
        cv2.imwrite(image_form, frame)
        cv2.imshow('screen', frame)
        cv2.waitKey(3)
        counter_image += 1
    elif key == ord('2'):
        video_type = 2
    elif key == ord('3'):
        video_type = 3
    elif key == ord('4'):
        video_type = 4
    elif key == ord('1'):
        video_type = 1
cap.release()
out.release()
cv2.destroyAllWindows()