from fpdf import FPDF
import os
from typing import Union

def save_to_pdf(content: Union[str, tuple], filename: str) -> str:
    """
    Menyimpan konten ke PDF dengan penanganan khusus untuk tuple
    Parameters:
        content: String atau tuple (text, success)
    """
    try:
        # Ekstrak teks jika content adalah tuple
        if isinstance(content, tuple):
            actual_content = content[0]  # Ambil elemen pertama (teks)
        else:
            actual_content = content

        # Pastikan direktori ada
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", filename)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Handle bullet points dan paragraf
        if actual_content.startswith("•"):
            items = actual_content.split("•")
            for item in items:
                if item.strip():
                    pdf.multi_cell(0, 10, "• " + item.strip())
                    pdf.ln(5)
        else:
            # Split menjadi paragraf
            paragraphs = actual_content.split('\n')
            for para in paragraphs:
                if para.strip():
                    pdf.multi_cell(0, 10, para.strip())
                    pdf.ln(5)
        
        pdf.output(path)
        return path
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        # Fallback - buat file teks biasa
        txt_path = path + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(str(actual_content))
        return txt_path