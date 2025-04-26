from transformers import pipeline
import re
from typing import Tuple
import torch

# Initialize model with better parameters
summarizer = pipeline(
    "summarization", 
    model="facebook/bart-large-cnn",
    device=0 if torch.cuda.is_available() else -1
)

def clean_text(text: str) -> Tuple[str, bool]:
    """Membersihkan teks dan cek kelayakan"""
    if not text or len(text.strip()) < 100:
        return text, False
    
    # Cleanup operations
    text = re.sub(r'\[.*?\]', '', text)  # Remove timestamps
    text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
    return text.strip(), True

def generate_summary(text_chunk: str) -> str:
    """Generate summary for one chunk"""
    try:
        result = summarizer(
            text_chunk,
            max_length=300,
            min_length=150,
            do_sample=False,
            truncation=True
        )
        return result[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing chunk: {str(e)}")
        return ""

def summarize_text(text: str) -> Tuple[str, bool]:
    """Fungsi utama dengan pengecekan error lebih ketat"""
    cleaned_text, is_valid = clean_text(text)
    if not is_valid:
        return "Teks tidak cukup panjang atau kosong", False
    
    chunks = [cleaned_text[i:i+2000] for i in range(0, len(cleaned_text), 2000)]
    summaries = []
    
    for chunk in chunks:
        chunk_summary = generate_summary(chunk)
        if chunk_summary:
            summaries.append(chunk_summary)
    
    if not summaries:
        return "Gagal menghasilkan rangkuman", False
    
    # Gabungkan dengan pemisah yang jelas
    final_summary = "\n\n• ".join(summaries)
    return f"• {final_summary}", True