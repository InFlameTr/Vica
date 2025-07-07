# main.py
from drive_utils import authenticate_drive, get_random_video_from_folder, download_video
from text_generator import generate_quote
from video_editor import add_text_to_video
import os

def process_drive_link(folder_link, logger=print, progress_callback=lambda x: None):
    service = authenticate_drive()

    # Link ise ID'yi ayıkla
    if "folders/" in folder_link:
        folder_id = folder_link.split("folders/")[1].split("?")[0]
    else:
        folder_id = folder_link.strip()

    video = get_random_video_from_folder(service, folder_id)
    if not video:
        logger("Video bulunamadı.")
        return

    logger(f"🎥 Seçilen video: {video['name']}")

    progress_callback(0.2)

    # Dosya adını sabitle
    downloaded_path = download_video(service, video)
    fixed_path = "videos/edit_video.mp4"
    os.rename(downloaded_path, fixed_path)

    logger("📥 Video indirildi.")

    progress_callback(0.5)

    quote = generate_quote()
    logger(f"💬 Üretilen söz: {quote}")

    output_path = "videos/output_video.mp4"
    add_text_to_video(fixed_path, output_path, quote)

    progress_callback(1.0)
    logger("🎬 Video düzenlendi ve kaydedildi.")
    return output_path
