import cv2
from tkinter import filedialog

def export_image(image):
    filename = filedialog.asksaveasfilename(defaultextension=".png", title="Enregistrer l'image")
    if filename:
        cv2.imwrite(filename, image)