import streamlit as st
import threading
from main import process_drive_link  # Senin ana işlem fonksiyonun
import shutil

st.set_page_config(page_title="VidCreatorApp", layout="centered")

def run_process(link, log_list, log_container, progress_bar):
    def logger(msg):
        log_list.append(msg)
        log_container.text("\n".join(log_list))

    def progress_callback(pct):
        progress_bar.progress(pct)

    try:
        output_path = process_drive_link(link, logger=logger, progress_callback=progress_callback)
        logger("✅ İşlem tamamlandı. Video hazır.")
        return output_path
    except Exception as e:
        logger(f"❌ Hata: {str(e)}")
        return None

def main():
    st.title("VidCreatorApp")

    drive_link = st.text_input("Google Drive klasör linkini girin:")

    if st.button("Başlat") and drive_link:
        log_list = []
        log_container = st.empty()
        progress_bar = st.progress(0)
        video_path_placeholder = st.empty()
        save_button_placeholder = st.empty()

        output_path = run_process(drive_link, log_list, log_container, progress_bar)

        if output_path:
            with open(output_path, "rb") as video_file:
                video_bytes = video_file.read()
                video_path_placeholder.video(video_bytes)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="Videoyu İndir",
                    data=f,
                    file_name="output_video.mp4",
                    mime="video/mp4"
                )

if __name__ == "__main__":
    main()
