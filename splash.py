import tkinter as tk
from PIL import Image, ImageTk

def show_splash(image_path="assets/splash.jpg"):
    splash = tk.Tk()
    splash.overrideredirect(True)

    # Charger image
    image = Image.open(image_path)
    width, height = image.size

    # Récupérer la taille écran avec Tkinter (écran principal)
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    # Calculer position pour centrer la fenêtre splash
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")

    # Afficher image dans un label
    img = ImageTk.PhotoImage(image)
    label = tk.Label(splash, image=img)
    label.image = img  # garder une référence
    label.pack()

    # Fermer après 2 secondes (2000ms)
    splash.after(2000, splash.destroy)
    splash.mainloop()

# Test
if __name__ == "__main__":
    show_splash()
