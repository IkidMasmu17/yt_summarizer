from fpdf import FPDF
import os

def save_to_pdf(text: str, filename: str = "output.pdf") -> str:
    """Menyimpan teks ke PDF dengan format yang baik"""
    # Buat direktori jika belum ada
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Handle teks kosong
    if not text.strip():
        text = "Tidak ada konten yang tersedia"
    
    # Normalisasi line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split paragraphs
    paragraphs = text.split('\n')
    
    for para in paragraphs:
        if para.strip():  # Skip empty lines
            pdf.multi_cell(0, 10, para.strip())
            pdf.ln(5)  # Add spacing between paragraphs
    
    pdf.output(filepath)
    return filepath