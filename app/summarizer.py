from transformers import pipeline
import re
from typing import List

# Gunakan model yang lebih baik untuk summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text: str) -> str:
    """Membersihkan teks dari karakter tidak perlu dan format paragraf"""
    # Hapus timestamps seperti [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    # Hapus karakter khusus kecuali tanda baca dasar
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    # Format paragraf
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return ' '.join(sentences).strip()

def split_text(text: str, max_length: int = 1024) -> List[str]:
    """Membagi teks menjadi chunk dengan batasan panjang"""
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 <= max_length:
            current_chunk += para + "\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_bullet_points(summary: str) -> str:
    """Mengubah summary menjadi poin-poin penting"""
    sentences = re.split(r'(?<=[.!?])\s+', summary)
    bullet_points = [f"• {s.strip()}" for s in sentences if s.strip()]
    return "\n".join(bullet_points)

def summarize_text(text: str, mode: str = "bullet_points") -> str:
    """Fungsi utama untuk menghasilkan rangkuman"""
    if not text or len(text.split()) < 50:
        return "⚠️ Teks terlalu pendek untuk dirangkum"
    
    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text)
    
    full_summary = []
    for chunk in chunks:
        try:
            summary = summarizer(
                chunk,
                max_length=300,
                min_length=100,
                do_sample=False,
                truncation=True
            )[0]['summary_text']
            full_summary.append(summary)
        except Exception as e:
            continue
    
    combined_summary = "\n\n".join(full_summary)
    
    if mode == "bullet_points":
        return generate_bullet_points(combined_summary)
    else:
        return combined_summary