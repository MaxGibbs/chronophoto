import tkinter as tk
from tkinter import filedialog, simpledialog

from PIL import Image, ImageTk

from core.exporter import export_image
from core.processor import process_video


def run_gui():
    root = tk.Tk()
    root.geometry("960x540+480+270")  # 960x540, positionné à (480,270) pour centrer sur 1920x1080
    app = ChronoPhotoApp(root)
    root.mainloop()

class ChronoPhotoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chronophotographie")
        self.result_img = None
        self.video_path = None

        self.container = tk.Frame(master)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.container, width=200, bg="#ddd")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.image_frame = tk.Frame(self.container, bg="black")
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bouton Charger vidéo
        tk.Button(self.sidebar, text="📂 Charger vidéo", command=self.load_video).pack(fill=tk.X, pady=5, padx=10)

        # Label affichant le nom du fichier
        self.video_label = tk.Label(self.sidebar, text="Aucune vidéo chargée", bg="#ddd", wraplength=180)
        self.video_label.pack(fill=tk.X, padx=10)

        # Bouton Supprimer la vidéo chargée
        self.delete_btn = tk.Button(self.sidebar, text="🗑️ Supprimer vidéo", command=self.delete_video, state=tk.DISABLED)
        self.delete_btn.pack(fill=tk.X, pady=5, padx=10)

        # Boutons générer, exporter, quitter
        tk.Button(self.sidebar, text="▶️ Générer", command=self.generate_chronophoto).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(self.sidebar, text="💾 Exporter", command=self.export).pack(fill=tk.X, pady=5, padx=10)
        tk.Button(self.sidebar, text="❌ Quitter", command=self.master.quit).pack(fill=tk.X, pady=5, padx=10)

        self.canvas = tk.Label(self.image_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_video(self):
        path = filedialog.askopenfilename(title="Choisir une vidéo")
        if path:
            self.video_path = path
            filename = path.split("/")[-1]  # ou os.path.basename(path)
            self.video_label.config(text=filename)
            self.delete_btn.config(state=tk.NORMAL)

    def delete_video(self):
        self.video_path = None
        self.video_label.config(text="Aucune vidéo chargée")
        self.delete_btn.config(state=tk.DISABLED)
        self.result_img = None
        self.canvas.config(image="")  # efface l'image affichée
        self.canvas.image = None

    def generate_chronophoto(self):
        interval = simpledialog.askfloat("Intervalle", "Secondes entre images :", minvalue=0.1, maxvalue=10)
        if not interval or not self.video_path:
            return
        self.result_img = process_video(self.video_path, interval)
        if self.result_img is not None:
            imtk = ImageTk.PhotoImage(Image.fromarray(self.result_img))
            self.canvas.configure(image=imtk)
            self.canvas.image = imtk

    def export(self):
        if self.result_img is not None:
            export_image(self.result_img)
