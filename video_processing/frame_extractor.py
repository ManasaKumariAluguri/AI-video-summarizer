import cv2
import os

def extract_frames(video_path, output_folder="outputs/frames"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)

    count = 0
    frame_rate = 30  # adjust if needed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save every 30th frame (1 frame per second approx)
        if count % frame_rate == 0:
            frame_name = os.path.join(output_folder, f"frame_{count}.jpg")
            cv2.imwrite(frame_name, frame)

        count += 1

    cap.release()
    return output_folder