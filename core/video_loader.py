import cv2

def open_video(video_path):
    """
    Ouvre une vidéo et retourne :
    - l'objet VideoCapture
    - le nombre de FPS
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Impossible d'ouvrir la vidéo : {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    return cap, fps