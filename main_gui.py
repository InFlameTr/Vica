import customtkinter as ctk
import threading
from main import process_drive_link
from tkinter import filedialog
from tkintervideo import TkinterVideo
import os
import cv2
from PIL import Image, ImageTk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VidCreatorApp")
        self.geometry("600x600")

        self.label = ctk.CTkLabel(self, text="Google Drive klasör linkini girin:")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, width=500)
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Başlat", command=self.start_process)
        self.button.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.log = ctk.CTkTextbox(self, width=550, height=100)
        self.log.pack(pady=10)

        self.save_button = ctk.CTkButton(self, text="Videoyu Kaydet", command=self.save_video)
        self.save_button.pack(pady=10)
        self.save_button.configure(state="disabled")

        # Video oynatıcı alanı
        self.preview_label = ctk.CTkLabel(self, text="Video Önizlemesi:")
        self.preview_label.pack(pady=5)

        self.videoplayer = TkinterVideo(master=self, scaled=True, pre_load=False)
        self.videoplayer.pack(expand=True, fill="both", pady=10)

    def start_process(self):
        drive_link = self.entry.get()
        self.log.insert("end", "🚀 İşlem başlatılıyor...\n")
        self.progress.set(0)
        self.save_button.configure(state="disabled")
        threading.Thread(target=self.run_process, args=(drive_link,), daemon=True).start()

    def run_process(self, link):
        def logger(msg):
            self.log.insert("end", msg + "\n")
            self.log.see("end")

        def progress_callback(pct):
            self.progress.set(pct)

        try:
            output_path = process_drive_link(link, logger=logger, progress_callback=progress_callback)
            logger("✅ İşlem tamamlandı. Video hazır.")
            self.show_video(output_path)
            self.save_button.configure(state="normal")
        except Exception as e:
            logger(f"❌ Hata: {str(e)}")

    def show_video(self, path):
        self.videoplayer.load(path)
        self.videoplayer.play()

    def save_video(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")],
            title="Videoyu Kaydet"
        )
        if save_path:
            import shutil
            shutil.copy("videos/output_video.mp4", save_path)
            self.log.insert("end", f"💾 Video başarıyla kaydedildi: {save_path}\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
