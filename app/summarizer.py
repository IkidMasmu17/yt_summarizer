from transformers import pipeline
import re

# Gunakan model yang lebih kecil jika resource terbatas
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    """Bersihkan teks dari karakter tidak standar dan spasi berlebihan"""
    text = re.sub(r'\s+', ' ', text)  # Hapus spasi berlebih
    text = re.sub(r'[^\w\s.,?!]', '', text)  # Hapus simbol aneh
    return text.strip()

def split_text(text, max_tokens=512):  # Diperkecil untuk model BART
    """Split teks menjadi chunk dengan batasan token"""
    sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_tokens:
            current_chunk += " " + sentence
        else:
            if current_chunk.strip():
                chunks.append(clean_text(current_chunk))
            current_chunk = sentence
    
    if current_chunk.strip():
        chunks.append(clean_text(current_chunk))
    
    return chunks

def summarize_text(text):
    if not text or len(text.split()) < 30:  # Minimal 30 kata
        return "⚠️ Teks terlalu pendek untuk dirangkum"
    
    chunks = split_text(text)
    summaries = []
    
    for i, chunk in enumerate(chunks):
        try:
            if len(chunk.split()) < 10:  # Skip chunk terlalu pendek
                continue
                
            summary = summarizer(
                chunk,
                max_length=150,  # Diperkecil
                min_length=30,
                do_sample=False,
                truncation=True  # Penting untuk teks panjang
            )[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"❌ Gagal merangkum chunk {i+1}: {str(e)}")
            continue
    
    return "\n\n".join(summaries) if summaries else "Tidak ada rangkuman yang dihasilkan."