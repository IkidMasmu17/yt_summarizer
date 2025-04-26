import yt_dlp
import os
import uuid

def download_audio(url: str) -> str:
    # Buat direktori output
    output_dir = "temp"
    os.makedirs(output_dir, exist_ok=True)

    # Generate nama file unik
    file_id = str(uuid.uuid4())
    output_path = os.path.join(output_dir, f"{file_id}.%(ext)s")

    # Set opsi yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return os.path.join(output_dir, f"{file_id}.mp3")
