import cv2
import numpy as np
from core.video_loader import open_video

def process_video(video_path, interval):
    cap, fps = open_video(video_path)
    if not cap or fps <= 0:
        return None

    frame_interval = int(fps * interval)

    # Lecture de la première frame et conversion HSV
    ret, first_frame = cap.read()
    if not ret:
        cap.release()
        return None

    first_hsv = cv2.cvtColor(first_frame, cv2.COLOR_BGR2HSV)
    first_s = first_hsv[:, :, 1]  # Canal saturation

    height, width = first_s.shape
    result = np.zeros((height, width), dtype=np.float32)

    count = 1
    frames_used = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            s = hsv[:, :, 1]

            # Différence de saturation
            diff = cv2.absdiff(first_s, s)

            # Seuil ajusté pour mouvements légers (tu peux tester avec 10 ou 20 aussi)
            _, mask = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)

            # Appliquer le masque à l’image en niveaux de gris (ou saturation directement)
            moving = cv2.bitwise_and(s, mask)

            # Accumuler le résultat
            result += moving.astype(np.float32)
            frames_used += 1

        count += 1

    cap.release()

    if frames_used == 0:
        return None

    # Normalisation finale
    result = np.clip(result / frames_used, 0, 255).astype(np.uint8)
    return result
