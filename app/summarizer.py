from transformers import pipeline
import re
from typing import Tuple
import torch

# Initialize model
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

def summarize_text(text: str, mode: str = "bullet_points") -> Tuple[str, bool]:
    """
    Fungsi utama untuk menghasilkan rangkuman
    Parameters:
        mode: "bullet_points" (default) atau "paragraph"
    """
    cleaned_text, is_valid = clean_text(text)
    if not is_valid:
        return "Teks tidak cukup panjang atau kosong", False
    
    chunks = [cleaned_text[i:i+2000] for i in range(0, len(cleaned_text), 2000)]
    summaries = []
    
    for chunk in chunks:
        try:
            summary = summarizer(
                chunk,
                max_length=300,
                min_length=150,
                do_sample=False,
                truncation=True
            )[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing: {str(e)}")
            continue
    
    if not summaries:
        return "Gagal menghasilkan rangkuman", False
    
    # Format output berdasarkan mode
    if mode == "bullet_points":
        final_summary = "\n• ".join(summaries)
        return f"• {final_summary}", True
    else:
        return " ".join(summaries), True