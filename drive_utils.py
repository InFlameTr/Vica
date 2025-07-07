# drive_utils.py
import os
import random
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Yalnızca bu erişim yeterli
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def get_random_video_from_folder(service, folder_id):
    # Belirli klasördeki mp4 dosyaları
    query = f"'{folder_id}' in parents and mimeType='video/mp4'"
    
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name)"
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print("Belirtilen klasörde video bulunamadı.")
        return None
    
    video = random.choice(items)
    print(f"Seçilen video: {video['name']}")
    return video


def download_video(service, file):
    file_id = file['id']
    request = service.files().get_media(fileId=file_id)
    os.makedirs("videos", exist_ok=True)

    # İsmi sabitle: edit_video.mp4
    file_path = os.path.join("videos", "edit_video.mp4")

    with open(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"İndirme % {int(status.progress() * 100)}")

    return file_path

